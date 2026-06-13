from fastapi import APIRouter,Depends, HTTPException,Query 

from sqlalchemy.orm import Session
from sqlalchemy import or_,desc,asc

from schemas import(
    PostCreate,
    PostResponse,
    PostWithUserResponse,
    PostUpdate,
    PostDetailResponse
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

#========================GET ALL POSTS(PAGINATION, SEARCH)============================================
@router.get('',response_model=list[PostResponse])
def get_posts(
    skip:int = 0,
    limit:int = 10,
    search:str = "",
    order:str = "desc",
    db:Session = Depends(get_db)
):
    return (
        db.query(Post)
        .filter(
            or_(
                Post.title.contains(search),
                Post.content.contains(search)
                )
            )
            .order_by(
            desc(Post.created_at)
            if order == "desc"
            else asc(Post.created_at)
        )
        .offset(skip)
        .limit(limit)
        .all()
    )

#=======================GET POSTS BY POST ID========================================
@router.get('/{post_id}',response_model=PostWithUserResponse)
def get_posts_by_id(post_id:int,db:Session=Depends(get_db)):
    
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    return post


#==================GET POST WITH LIKES & COMMENTS=====================
@router.get('/{id}/details',response_model=PostDetailResponse)
def get_posts_with_like_comments(id:int,db:Session=Depends(get_db)):
    
    post = db.query(Post).filter(Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    return {
        "id":post.id,
        "title":post.title,
        "content":post.content,
        "owner":post.owner,
        "likes_count":len(post.likes),
        "comments_count":len(post.comments)
    }
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
