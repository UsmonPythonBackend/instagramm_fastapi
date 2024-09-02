from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder

from database import Session, ENGINE
from models import Follows
from fastapi.exceptions import HTTPException

from schemas import FollowsCreateModel, FollowsListModel

follows_router = APIRouter(prefix="/follows", tags=["Follows"])
session = Session(bind=ENGINE)


@follows_router.get("/")
async def get_follows():
    follows = session.query(Follows).all()
    return jsonable_encoder(follows)

@follows_router.post("/")
async def create_follows(follows: FollowsCreateModel):
    new_follows = Follows(
        id=follows.id,
        follower_id=follows.follwer_id,
        following_id=follows.follwing_id,

    )

    session.add(new_follows)
    session.commit()
    data = {
        "status": 201,
        "message": "Follows created successfully",
        "object": {
            "id": follows.id,
            "follower_id": follows.follwer_id,
            "following_id": follows.follwing_id,
        }
    }

    return jsonable_encoder(data)



@follows_router.get("/{id}")
async def follows_detail(id: int, FollowsListModel, following=None, follower=None):
    follows = session.query(Follows).filter(Follows.id == id).first()
    if follows is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Follows not found')


    data = {

            "follower_id": follower.id,
            "following_id": following.id

        }
    return jsonable_encoder(data)






@follows_router.delete("/{id}")
async def follows_delete(id: int):
    follows = session.query(Follows).filter(Follows.id == id).first()
    if follows:
        session.delete(follows)
        session.commit()
        data = {
            "code": 200,
            "message": "Follows deleted"
        }

        return jsonable_encoder(data)

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="follows not found")