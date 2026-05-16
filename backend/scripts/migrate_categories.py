import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def migrate_categories():
    client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    db = client.expense_tracker
    
    translations = {
        "Food": "طعام",
        "Transport": "مواصلات",
        "Rent": "إيجار",
        "Entertainment": "ترفيه",
        "Shopping": "تسوق"
    }
    
    for en_name, ar_name in translations.items():
        result = await db.categories.update_many(
            {"name": en_name},
            {"$set": {"name": ar_name}}
        )
        print(f"Updated {result.modified_count} categories from {en_name} to {ar_name}")

    # Also add "أخرى" for existing users if it doesn't exist
    users = await db.categories.distinct("user_id")
    for user_id in users:
        exists = await db.categories.find_one({"name": "أخرى", "user_id": user_id})
        if not exists:
            await db.categories.insert_one({"name": "أخرى", "icon": "🏷️", "user_id": user_id})
            print(f"Added 'أخرى' category for user {user_id}")

if __name__ == "__main__":
    asyncio.run(migrate_categories())
