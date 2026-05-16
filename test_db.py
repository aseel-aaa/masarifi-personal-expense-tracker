import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load from .env
load_dotenv(".env")

async def test_connection():
    url = os.getenv("MONGODB_URL")
    print(f"Testing connection to: {url}")
    
    if not url:
        print("ERROR: MONGODB_URL is not set in .env.example")
        return

    try:
        # Check for malformed URL
        if url.startswith("mongodb+srv:mongodb+srv://"):
            print("WARNING: Malformed URL detected (double prefix). Fixing...")
            url = url.replace("mongodb+srv:mongodb+srv://", "mongodb+srv://")
            print(f"Fixed URL: {url}")

        client = AsyncIOMotorClient(url, serverSelectionTimeoutMS=5000, tls=True, tlsAllowInvalidCertificates=True)
        await client.admin.command('ping')
        print("SUCCESS: Connection Successful!")
    except Exception as e:
        print(f"FAILURE: Connection Failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_connection())
