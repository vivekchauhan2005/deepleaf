
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

from config.database import db
from utils.auth import (
    hash_password,
    verify_password,
    create_access_token,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# Request models
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


@router.post("/register")
async def register(user: UserCreate):
    existing_user = db["users"].find_one({
        "email": user.email
    })

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    hashed_password = hash_password(user.password)

    user_data = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
    }

    db["users"].insert_one(user_data)

    # Use the same JWT implementation as protected routes.
    token = create_access_token({
        "sub": user.email
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "message": "User created successfully",
    }


@router.post("/login")
async def login(user: UserLogin):
    existing_user = db["users"].find_one({
        "email": user.email
    })

    if (
        not existing_user
        or not verify_password(
            user.password,
            existing_user["password"],
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    # Generate a token using the shared authentication helper.
    token = create_access_token({
        "sub": existing_user["email"]
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "message": "Login successful",
    }
