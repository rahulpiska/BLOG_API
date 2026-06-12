from fastapi import Depends ,HTTPException, APIRouter
from sqlalchemy.orm import Session
from models import User, Post,Like
from database import get_db
from utils import get_current_user

router = APIRouter(
    prefix="/likes",
    tags=["Likes"]
)

@router.post('/posts/{post_id}')
def like_post(post_id:int,
              current_user:User= Depends(get_current_user),
              db:Session=Depends(get_db)
            ):
    
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )
    
    existing_like = db.query(Like).filter(
        Like.user_id == current_user.id,
        Like.post_id == post_id).first()
    
    if existing_like:
        db.delete(existing_like)

        db.commit()

        return {
            "message":"Post Unliked"
        }
    
    new_like = Like(
        user_id = current_user.id,
        post_id = post_id
    )

    db.add(new_like)

    db.commit()

    return{
        "message":"Post Liked"
    }
