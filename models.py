from sqlalchemy import Column,String,Integer,ForeignKey,DateTime,Text

from sqlalchemy.orm import relationship

from datetime import datetime

from database import Base


#===========================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True, index=True)

    name = Column(String(100),nullable=False)

    email= Column(String(100),unique=True,nullable=False)

    password= Column(String(225),nullable=False)

    created_at = Column(DateTime,default=datetime.utcnow)

    posts = relationship(
        "Post",
        back_populates= "owner"
    )

    comments = relationship(
        "Comment",
        back_populates="user"
    )

    likes = relationship(
        "Like",
        back_populates="user"
    )

#===============================================================

class Post(Base):
    __tablename__ ="posts"

    id = Column(Integer,primary_key=True,index=True)

    title = Column(String(100),nullable=False)

    content = Column(Text, nullable=False)

    user_id = Column(Integer,ForeignKey("users.id"))

    created_at= Column(DateTime,default=datetime.utcnow)
    
    updated_at= Column(DateTime,
                       default=datetime.utcnow,
                       onupdate=datetime.utcnow
    )

    owner = relationship(
        "User",
        back_populates="posts"
    )

    comments = relationship(
        "Comment",
        back_populates="post"
    )

    likes= relationship(
        "Like",
        back_populates="post"
    )
#=========================================================

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer,primary_key=True)

    text = Column(String(200),nullable=False)
    
    post_id = Column(Integer,ForeignKey("posts.id"))

    user_id = Column(Integer,ForeignKey("users.id"))

    created_at = Column(DateTime,default=datetime.utcnow)

    user = relationship(
        "User",
        back_populates="comments"
    )

    post = relationship(
        "Post",
        back_populates="comments"
    )

#============================================================

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer,primary_key=True)

    post_id = Column(Integer, ForeignKey("posts.id"))

    user_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime,default=datetime.utcnow)

    user = relationship(
        "User",
        back_populates="likes"
    )
    post = relationship(
        "Post",
        back_populates= "likes"
    )