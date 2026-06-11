from fastapi import FastAPI

from database import Base,engine
#Base.metadata.create_all(bind=engine)

from routes.users import router as user_router
from routes.posts import router as post_router

app = FastAPI()

app.include_router(user_router)
app.include_router(post_router)