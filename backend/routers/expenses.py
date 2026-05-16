from fastapi import APIRouter, Depends, HTTPException, Query
from ..models import Expense
from ..database import get_database
from ..auth import get_current_user
from bson import ObjectId
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/expenses", tags=["expenses"])
db = get_database()

@router.get("/", response_model=List[Expense])
async def list_expenses(
    current_user: str = Depends(get_current_user),
    category_id: Optional[str] = None,
    month: Optional[int] = None,
    year: Optional[int] = None
):
    query = {"user_id": current_user}
    if category_id:
        query["category_id"] = category_id
    
    if month and year:
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        query["date"] = {"$gte": start_date, "$lt": end_date}

    expenses = await db.expenses.find(query).sort("date", -1).to_list(length=1000)
    for exp in expenses:
        exp["_id"] = str(exp["_id"])
        # Fetch category info
        cat = await db.categories.find_one({"_id": ObjectId(exp["category_id"])})
        if cat:
            exp["category_name"] = cat["name"]
            exp["category_icon"] = cat.get("icon", "💰")
    return expenses

@router.post("/", response_model=Expense)
async def create_expense(expense: Expense, current_user: str = Depends(get_current_user)):
    expense.user_id = current_user
    new_exp = await db.expenses.insert_one(expense.model_dump(exclude={"id"}))
    created_exp = await db.expenses.find_one({"_id": new_exp.inserted_id})
    created_exp["_id"] = str(created_exp["_id"])
    return created_exp

@router.delete("/{expense_id}")
async def delete_expense(expense_id: str, current_user: str = Depends(get_current_user)):
    delete_result = await db.expenses.delete_one({"_id": ObjectId(expense_id), "user_id": current_user})
    if delete_result.deleted_count == 1:
        return {"message": "Expense deleted"}
    raise HTTPException(status_code=404, detail="Expense not found")

@router.get("/stats")
async def get_stats(current_user: str = Depends(get_current_user)):
    # Total this month
    now = datetime.utcnow()
    start_month = datetime(now.year, now.month, 1)
    
    pipeline = [
        {"$match": {"user_id": current_user, "date": {"$gte": start_month}}},
        {"$group": {"_id": "$currency", "total": {"$sum": "$amount"}}}
    ]
    totals_res = await db.expenses.aggregate(pipeline).to_list(100)
    month_totals = {res["_id"] or "USD": res["total"] for res in totals_res}

    # Recent 5
    recent = await db.expenses.find({"user_id": current_user}).sort("date", -1).limit(5).to_list(5)
    for r in recent:
        r["_id"] = str(r["_id"])
        # Fetch category info
        cat = await db.categories.find_one({"_id": ObjectId(r["category_id"])})
        if cat:
            r["category_name"] = cat["name"]
            r["category_icon"] = cat.get("icon", "💰")

    return {
        "month_totals": month_totals,
        "recent_expenses": recent
    }

@router.get("/reports/category")
async def report_by_category(current_user: str = Depends(get_current_user)):
    pipeline = [
        {"$match": {"user_id": current_user}},
        {"$group": {"_id": "$category_id", "total": {"$sum": "$amount"}}}
    ]
    results = await db.expenses.aggregate(pipeline).to_list(100)
    
    # Get category names
    report = []
    for res in results:
        cat = await db.categories.find_one({"_id": ObjectId(res["_id"])})
        report.append({
            "category": cat["name"] if cat else "Unknown",
            "total": res["total"]
        })
    return report
