from http.client import HTTPException

from fastapi import APIRouter
from rest_framework import status

from database import ENGINE , Session
from models import Comment
from fastapi.encoders import jsonable_encoder
from schemas import CommentCreateModel, CommentUpdateModel

session = Session(bind=ENGINE)

comment_router = APIRouter(prefix="/comment", tags=["Comment"])

@comment_router.get("/")
async def get_comment():
    comment = session.query(Comment).all()
    return jsonable_encoder(comment)

@comment_router.post("/")
async def create_comment(comment: CommentCreateModel):
    new_comment = Comment(
        user_id=comment.user_id,
        post_id=comment.image_path,
        status=comment.status
    )

    session.add(new_comment)
    session.commit()
    data = {
        "status": 201,
        "message": "Comment created successfully",
        "object": {
            "user_id": comment.user_id,
            "post_id": comment.image_path,
            "status": comment.status
        }
    }

    return jsonable_encoder(data)



@comment_router.put("/{id}")
async def comment_update(id: int, comment: CommentUpdateModel):
    check_comment = session.query().filter(Comment.id == id).first()
    if check_comment:
        for key, value in comment.dict(exclude_unset=True).items():
            setattr(check_comment, key, value)
        data = {
            "status": 201,
            "message": "Post update successfully",
            "object": {
                "user_id": comment.user_id,
                "post_id": comment.image_path,
                "status": comment.status
            }
        }
        session.commit()
        return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="comment not found")




@comment_router.delete("/{id}")
async def comment_delete(id: int):
    comment = session.query(Comment).filter(Comment.id == id).first()
    if comment:
        session.delete(comment)
        session.commit()
        data = {
            "code": 200,
            "message": "Comment deleted"
        }

        return jsonable_encoder(data)

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="comment not found")
