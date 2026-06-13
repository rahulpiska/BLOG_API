from pydantic import BaseModel, EmailStr, ConfigDict
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

class CommentCreate(BaseModel):
    text:str

class CommentResponse(BaseModel):
    id: int
    text: str
    post_id :int
    user_id: int
    created_at: datetime

    class config:
        from_attributes = True


class UpdateComment(BaseModel):
    text:str

class UserInfo(BaseModel):
    id:int
    name:str

    model_config = ConfigDict(
        from_attributes= True
    )

class PostDetailResponse(BaseModel):
    id:int
    title:str
    content: str
    
    owner: UserInfo
    
    likes_count:int
    comments_count: int

    model_config = ConfigDict(
        from_attributes=True
    )

