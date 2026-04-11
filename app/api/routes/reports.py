from fastapi import APIRouter, Depends
from services.database import get_profit_report_by_user
from services.auth import get_current_user

router = APIRouter()


@router.get("/profit")
def profit_report(current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    data = get_profit_report_by_user(user_id)
    return [
        {
            "crop": row[1],
            "harvest_quantity": row[2],
            "selling_price": row[3],
            "total_expenses": row[4],
            "revenue": row[5],
            "profit": row[6],
        }
        for row in data
    ]
