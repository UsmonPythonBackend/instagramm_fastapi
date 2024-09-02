from http.client import HTTPException

from fastapi import APIRouter
from rest_framework import status

from database import ENGINE , Session
from models import User
from fastapi.encoders import jsonable_encoder
from schemas import UserModel

session = Session(bind=ENGINE)

user_router = APIRouter(prefix="/user", tags=["User"])

@user_router.get("/")
async def get_user():
    user = session.query(User).all()
    return jsonable_encoder(user)

@user_router.post("/")
async def create_user(user: UserModel):
    new_user = User(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        password=user.password,
        bio=user.bio,
        profile_picture=user.profile_picture

    )

    session.add(new_user)
    session.commit()
    data = {
        "status": 201,
        "message": "Comment created successfully",
        "object": {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "email": user.email,
            "password": user.password,
            "bio": user.bio,
            "profile_picture": user.profile_picture
        }
    }

    return jsonable_encoder(data)



@user_router.put("/{id}")
async def user_update(id: int, user: UserModel):
    check_user = session.query().filter(User.id == id).first()
    if check_user:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(check_user, key, value)
        data = {
            "status": 201,
            "message": "User update successfully",
            "object": {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "email": user.email,
                "password": user.password,
                "bio": user.bio,
                "profile_picture": user.profile_picture
            }
        }
        session.commit()
        return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")




@user_router.delete("/{id}")
async def user_delete(id: int):
    user = session.query(User).filter(User.id == id).first()
    if user:
        session.delete(user)
        session.commit()
        data = {
            "code": 200,
            "message": "User deleted"
        }

        return jsonable_encoder(data)

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
