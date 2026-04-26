from fastapi import APIRouter, Depends, HTTPException
from services.auth import get_current_user
from services.database import (
    add_crop,
    delete_crop,
    get_crops_by_user,
    record_harvest,
    record_price_history,
)

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
def create_crop(
    name: str,
    planting_date: str = None,
    field_size: float = None,
    planted_quantity: int = None,
    region: str = None,
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["user_id"]
    add_crop(user_id, name, planting_date, field_size, planted_quantity, region=region)
    return {"message": "Crop added", "name": name}


@router.post("/harvest")
def record_harvest_endpoint(
    crop_id: int,
    harvest_quantity: float,
    harvest_date: str,
    selling_price: float,
    current_user: dict = Depends(get_current_user),
):

    user_id = current_user["user_id"]

    user_crops = get_crops_by_user(user_id)
    crop_ids = [crop[0] for crop in user_crops]

    if crop_id not in crop_ids:
        raise HTTPException(status_code=403, detail="Not your crop")

    # Get crop name for price history
    crop = next((c for c in user_crops if c[0] == crop_id), None)
    crop_name = crop[1] if crop else "unknown"

    record_harvest(crop_id, harvest_quantity, harvest_date, selling_price)
    record_price_history(crop_name, selling_price)

    return {"message": "Harvest recorded"}


@router.delete("/{crop_id}")
def delete_crop_endpoint(crop_id: int, current_user: dict = Depends(get_current_user)):

    user_id = current_user["user_id"]

    user_crops = get_crops_by_user(user_id)
    crop_ids = [crop[0] for crop in user_crops]

    if crop_id not in crop_ids:
        raise HTTPException(status_code=403, detail="Not your crop")

    delete_crop(crop_id)
    return {"message": "Crop deleted"}
