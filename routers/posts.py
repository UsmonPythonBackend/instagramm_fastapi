from http.client import HTTPException

from fastapi import APIRouter
from rest_framework import status

from database import ENGINE , Session
from models import Post
from fastapi.encoders import jsonable_encoder
from schemas import PostUpdateModel, CreatePost, PostListModel

session = Session(bind=ENGINE)

post_router = APIRouter(prefix="/posts", tags=["Posts"])

@post_router.get("/")
async def get_posts():
    posts = session.query(Post).all()
    return jsonable_encoder(posts)

@post_router.post("/")
async def create_post(post: CreatePost):
    new_post = Post(
        user_id=post.user_id,
        image_path=post.image_path,
        caption=post.caption
    )

    session.add(new_post)
    session.commit()
    data = {
        "status": 201,
        "message": "Post created successfully",
        "object": {
            "user_id": post.user_id,
            "image_path": post.image_path,
            "caption": post.caption
        }
    }

    return jsonable_encoder(data)



@post_router.put("/{id}")
async def post_update(id: int, post: PostUpdateModel):
    check_post = session.query(Post).filter(Post.id == id).first()
    if check_post:
        for key, value in post.dict(exclude_unset=True).items():
            setattr(check_post, key, value)
        data = {
            "status": 201,
            "message": "Post update successfully",
            "object": {
                "user_id": post.user_id,
                "image_path": post.image_path,
                "caption": post.caption
            }
        }
        session.commit()
        return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")




@post_router.delete("/{id}")
async def post_delete(id: int):
    post = session.query(Post).filter(Post.id == id).first()
    if post:
        session.delete(post)
        session.commit()
        data = {
            "code": 200,
            "message": "Post deleted"
        }

        return jsonable_encoder(data)

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
