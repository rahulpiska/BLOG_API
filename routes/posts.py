from fastapi import APIRouter,Depends, HTTPException

from sqlalchemy.orm import Session

from schemas import(
    PostCreate,
    PostResponse,
    PostWithUserResponse,
    PostUpdate
)
from database import get_db

from models import Post, User

from utils import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

#=====================CREATE POST==============================================

@router.post('',response_model=PostResponse)
def create_post(post:PostCreate,
                current_user:User = Depends(get_current_user),
                db:Session=Depends(get_db)):
    
    new_post = Post(
        title = post.title,
        content = post.content,
        user_id = current_user.id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

#========================GET ALL POSTS============================================

@router.get('',response_model=list[PostResponse])
def get_posts(db:Session=Depends(get_db)):

    posts = db.query(Post).all()

    return posts

#=======================GET POSTS BY POST ID========================================
@router.get('/{id}',response_model=PostWithUserResponse)
def get_posts_by_id(id:int,db:Session=Depends(get_db)):
    
    post = db.query(Post).filter(Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    return post


#=======================UPDATE POST===================================
@router.put("/{id}",response_model=PostResponse)
def update_post(id:int,
                update_post:PostUpdate,
                current_user:User= Depends(get_current_user),
                db:Session= Depends(get_db)
            ):
    
    post = db.query(Post).filter(Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )
    
    if current_user.id != post.user_id:
        raise HTTPException(
            status_code=403,
            detail= "Forbidden , You are not allowed "
        )
    
    if update_post.title is not None:
        post.title = update_post.title

    if update_post.content is not None:
        post.content = update_post.content

    db.commit()

    db.refresh(post)

    return post

#=====================DELETE POST======================================

@router.delete("/{id}")
def delete_post(id:int,
                current_user:User = Depends(get_current_user),
                db:Session= Depends(get_db)
            ):
    
    post = db.query(Post).filter(Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )
    
    if current_user.id != post.user_id:
        raise HTTPException(
            status_code=403,
            detail="Forbidden, You are not allowed "
        )
    
    db.delete(post)

    db.commit()

    return {
        "message":"Post Deleted Successful"
    }