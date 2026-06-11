from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import(
    UserCreate,
    UserResponse,
    UserLogin
)
from utils import (hash_password,
                   verify_password,
                   create_access_token,
                   get_current_user)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post('', response_model=UserResponse)
def create_user(user:UserCreate,
                db:Session=Depends(get_db)):
    
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )

    
    hashed_password = hash_password(user.password)

    new_user = User(
        name = user.name,
        email = user.email,
        password = hashed_password
    )

    db.add(new_user)

    db.commit()
    db.refresh(new_user)

    return new_user

#=======================LOGIN=================================
@router.post('/login')
def login(user_data:UserLogin,
          db:Session=Depends(get_db)):
    
    user = db.query(User).filter(User.email == user_data.email).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Credintials"
        )
    
    is_valid = verify_password(
        user_data.password,
        user.password
    )

    if not is_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid Credintials"
        )
    
    token = create_access_token(
       { "user_id":user.id}
    )

    return {
        "access_token": token
    }


@router.get('/me',response_model=UserResponse)
def get_me(current_user:User = Depends(get_current_user)):

    return current_user