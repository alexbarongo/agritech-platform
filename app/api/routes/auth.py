from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.database import create_user, get_user_by_email
from services.auth import hash_password, verify_password, create_access_token

router = APIRouter()


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(request: RegisterRequest):
    existing = get_user_by_email(request.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hased = hash_password(request.password)
    success = create_user(request.name, request.email, hased)

    if not success:
        raise HTTPException(status_code=500, detail="Registration failed")

    return {"message": "Account created successfully"}


@router.post("/login")
def login(request: LoginRequest):
    user = get_user_by_email(request.email)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(request.password, user[3]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": user[2], "user_id": user[0]})

    return {"access_token": token, "token_type": "bearer"}
