from fastapi import Depends, HTTPException, APIRouter

from sqlalchemy.orm import Session

from database import get_db
from schemas import(CommentCreate,
                    CommentResponse,
                    UpdateComment
                )

from models import Post, User, Comment

from utils import get_current_user

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)

#===================COMMENT ON A POST====================================

@router.post("/posts/{post_id}",response_model=CommentResponse)
def create_comment(post_id:int,
                   create_comment:CommentCreate,
                   current_user:User = Depends(get_current_user),
                   db:Session = Depends(get_db)
                ):
    
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )
    new_comment = Comment(
        text = create_comment.text,
        post_id = post_id,
        user_id = current_user.id
    )

    db.add(new_comment)

    db.commit()

    db.refresh(new_comment)

    return new_comment

#======================GET ALL COMMENTS=================================
@router.get('',response_model=list[CommentResponse])
def get_all_comments(db:Session=Depends(get_db)):

    comments = db.query(Comment).all()

    return comments

#=================UPDATE COMMENT=====================================

@router.put("/{comment_id}",response_model=CommentResponse)
def update_comment(comment_id:int,
                   update_comment:UpdateComment,
                   current_user:User = Depends(get_current_user),
                   db:Session = Depends(get_db)
                ):
    
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(
            status_code=404,
            detail="comment not found"
        )
    
    if current_user.id != comment.user_id:
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )
    
    comment.text = update_comment.text
    
    db.commit()
    db.refresh(comment)

    return comment

#==================DELETE COMMENT=====================================

@router.delete('/{comment_id}')
def delete_comment(comment_id:int,
                   current_user:User = Depends(get_current_user),
                   db:Session=Depends(get_db)
                ):
    
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )
    
    if current_user.id != comment.user_id:
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )
    
    db.delete(comment)

    db.commit()

    return {
        "message":"Comment Deleted Successful"
    }