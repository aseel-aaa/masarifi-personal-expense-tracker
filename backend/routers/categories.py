from fastapi import APIRouter, Depends, HTTPException
from ..models import Category
from ..database import get_database
from ..auth import get_current_user
from bson import ObjectId
from typing import List

router = APIRouter(prefix="/categories", tags=["categories"])
db = get_database()

@router.get("/", response_model=List[Category])
async def list_categories(current_user: str = Depends(get_current_user)):
    categories = await db.categories.find({"user_id": current_user}).to_list(length=100)
    # Also include some default categories if user has none
    if not categories:
        defaults = [
            {"name": "طعام", "icon": "🍔", "user_id": current_user},
            {"name": "مواصلات", "icon": "🚗", "user_id": current_user},
            {"name": "إيجار", "icon": "🏠", "user_id": current_user},
            {"name": "ترفيه", "icon": "🎬", "user_id": current_user},
            {"name": "تسوق", "icon": "🛍️", "user_id": current_user},
            {"name": "أخرى", "icon": "🏷️", "user_id": current_user},
        ]
        await db.categories.insert_many(defaults)
        categories = await db.categories.find({"user_id": current_user}).to_list(length=100)
    else:
        # For existing users: ensure "أخرى" category exists
        has_other = any(cat.get("name") == "أخرى" for cat in categories)
        if not has_other:
            new_cat = {"name": "أخرى", "icon": "🏷️", "user_id": current_user}
            await db.categories.insert_one(new_cat)
            categories = await db.categories.find({"user_id": current_user}).to_list(length=100)
    
    for cat in categories:
        cat["_id"] = str(cat["_id"])
    return categories

@router.post("/", response_model=Category)
async def create_category(category: Category, current_user: str = Depends(get_current_user)):
    category.user_id = current_user
    new_cat = await db.categories.insert_one(category.model_dump(exclude={"id"}))
    created_cat = await db.categories.find_one({"_id": new_cat.inserted_id})
    created_cat["_id"] = str(created_cat["_id"])
    return created_cat

@router.delete("/{category_id}")
async def delete_category(category_id: str, current_user: str = Depends(get_current_user)):
    delete_result = await db.categories.delete_one({"_id": ObjectId(category_id), "user_id": current_user})
    if delete_result.deleted_count == 1:
        return {"message": "Category deleted"}
    raise HTTPException(status_code=404, detail="Category not found")
