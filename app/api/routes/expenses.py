from fastapi import APIRouter
from services.database import get_expenses_with_crops, add_expense

router = APIRouter()


@router.get("/")
def list_expenses():
    expenses = get_expenses_with_crops()
    return [
        {"id": exp[0], "crop": exp[1], "item": exp[2], "amount": exp[3]}
        for exp in expenses
    ]


@router.post("/")
def create_expense(crop_id: int, item: str, amount: float):
    add_expense(item, amount, crop_id)
    return {"message": "Expense recorded", "item": item, "amount": amount}
