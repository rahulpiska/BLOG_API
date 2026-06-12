from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from utils import get_current_user, verify_password, create_access_token
from models import User


from schemas import(
    UserLogin,
    UserResponse
)

router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)

#=======================USER LOGIN==================================

@router.post('')
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

#============================================================

@router.get('/me',response_model=UserResponse)
def get_me(current_user:User = Depends(get_current_user)):

    return current_user