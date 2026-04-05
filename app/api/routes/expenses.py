from fastapi import APIRouter, Depends
from services.auth import get_current_user
from services.database import add_expense, get_expenses_with_crops_by_user

router = APIRouter()


@router.get("/")
def list_expenses(current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    expenses = get_expenses_with_crops_by_user(user_id)
    return [
        {"id": exp[0], "crop": exp[1], "item": exp[2], "amount": exp[3]}
        for exp in expenses
    ]


@router.post("/")
def create_expense(
    crop_id: int,
    item: str,
    amount: float,
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["user_id"]
    add_expense(user_id, item, amount, crop_id)
    return {"message": "Expense recorded", "item": item, "amount": amount}
