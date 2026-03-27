from fastapi import APIRouter
from services.database import get_crops, add_crop

router = APIRouter()


@router.get("/")
def list_crops():
    crops = get_crops()
    return [{"id": crop[0], "name": crop[1]} for crop in crops]


@router.post("/")
def create_crop(name: str):
    add_crop(name)
    return {"message": "Crop added", "name": name}
