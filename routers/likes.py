from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder

from database import Session, ENGINE
from models import Likes
from fastapi.exceptions import HTTPException

from schemas import LikesListModel, LikesCreateModel

likes_router = APIRouter(prefix="/likes", tags=["Likes"])
session = Session(bind=ENGINE)


@likes_router.get("/")
async def get_likes():
    likes = session.query(Likes).all()
    return jsonable_encoder(likes)

@likes_router.post("/")
async def create_likes(likes: LikesCreateModel):
    new_likes = likes(
        user_id=likes.user_id,
        post_id=likes.post_id,
        status=likes.status,

    )

    session.add(new_likes)
    session.commit()
    data = {
        "status": 201,
        "message": "Follows created successfully",
        "object": {
            "user_id": likes.user_id,
            "post_id": likes.post_id,
            "status": likes.status,
        }
        }

    return jsonable_encoder(data)



@likes_router.get("/{id}")
async def likes_detail(id: int):
    likes = session.query(Likes).filter(Likes.id == id).first()
    if likes is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Likes not found')


    data = {

            "user_id": likes.user_id,
            "post_id": likes.post_id,
            "status": likes.status

        }
    return jsonable_encoder(data)






@likes_router.delete("/{id}")
async def likes_delete(id: int):
    likes = session.query(Likes).filter(Likes.id == id).first()
    if likes:
        session.delete(likes)
        session.commit()
        data = {
            "code": 200,
            "message": "Likes deleted"
        }

        return jsonable_encoder(data)

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="likes not found")