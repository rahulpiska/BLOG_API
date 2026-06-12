from fastapi import FastAPI

from database import Base,engine
#Base.metadata.create_all(bind=engine)

from routes.users import router as user_router
from routes.posts import router as post_router
from routes.comments import router as comment_router
from routes.likes import router as like_router
from routes.auth import router as auth_router

app = FastAPI()

app.include_router(user_router)
app.include_router(post_router)
app.include_router(comment_router)
app.include_router(like_router)
app.include_router(auth_router)