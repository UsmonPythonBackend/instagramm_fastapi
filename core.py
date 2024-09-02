from fastapi import FastAPI
from routers.posts import post_router
from routers.auth import auth_router
from routers.likes import likes_router
from routers.comments import comment_router
from routers.followers import follows_router
from routers.user import user_router

app = FastAPI()
app.include_router(post_router)
app.include_router(auth_router)
app.include_router(likes_router)
app.include_router(comment_router)
app.include_router(follows_router)
app.include_router(user_router)

@app.get("/")
def root():
    return {"msg": "welcome"}