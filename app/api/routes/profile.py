from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from services.auth import get_current_user, hash_password, verify_password
from services.database import get_user_by_id, update_user_name, update_user_password

router = APIRouter()


class UpdateNameRequest(BaseModel):
    name: str


class UpdatePasswordRequest(BaseModel):
    current_password: str
    new_password: str


@router.get("/")
def get_profile(current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user[0], "name": user[1], "email": user[2], "created_at": user[3]}


@router.put("/name")
def update_name(
    request: UpdateNameRequest, current_user: dict = Depends(get_current_user)
):
    user_id = current_user["user_id"]
    update_user_name = (user_id, request.name)
    return {"message": "Name updated successfully"}


@router.put("/password")
def update_password(
    request: UpdatePasswordRequest, current_user: dict = Depends(get_current_user)
):
    from services.database import get_user_by_id

    user_id = current_user["user_id"]
    user = get_user_by_id(user_id)

    if not verify_password(request.current_password, user[3]):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    hashed = hash_password(request.new_password)
    update_user_password(user_id, hashed)
    return {"message": "Password updated successfully"}
