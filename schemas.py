from pydantic import BaseModel, EmailStr
from datetime import datetime



class UserCreate(BaseModel):
    name:str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id:int
    name: str
    email:EmailStr
    created_at :datetime

    class config:
        from_attributes= True

class UserLogin(BaseModel):
    email: EmailStr
    password : str


class PostCreate(BaseModel):
    title: str
    content:str

class PostResponse(BaseModel):
    id:int
    title:str
    content:str
    user_id:int
    created_at: datetime
    updated_at:datetime

    class config:
        from_attributes=True


class PostWithUserResponse(BaseModel):
    id:int
    title:str
    content:str

    owner : UserResponse

    class config:
        from_attributes=True

class PostUpdate(BaseModel):
    title: str | None = None
    content:str | None = None