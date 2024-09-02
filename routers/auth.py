from fastapi import APIRouter, HTTPException, status

from database import Session, ENGINE
from models import User
from schemas import RegisterModel
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder

session = Session(bind=ENGINE)
auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/register")
async def register(user: RegisterModel):
    check_user = session.query(User).filter(User.username == user.username).first()
    if check_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password)
    )
    session.add(new_user)
    session.commit()
    data = {
        "status": 201,
        "message": "User created successfully",
        "object": {
            "username": user.username,
            "email": user.email,
            "password": generate_password_hash(user.password)
        }
    }
    return jsonable_encoder(data)