from fastapi import APIRouter, Depends
from services.auth import get_current_user
from services.database import add_crop, get_crops_by_user

router = APIRouter()


@router.get("/")
def list_crops(current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    crops = get_crops_by_user(user_id)
    return [
        {
            "id": crop[0],
            "name": crop[1],
            "planting_date": crop[2],
            "field_size": crop[3],
            "planted_quantity": crop[4],
            "harvest_date": crop[5],
            "harvest_quantity": crop[6],
            "selling_price": crop[7],
        }
        for crop in crops
    ]


@router.post("/")
def create_crop(name: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    add_crop(user_id, name)
    return {"message": "Crop added", "name": name}
