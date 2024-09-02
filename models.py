from datetime import datetime
import sqlalchemy_utils
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from database import Base, Session, ENGINE
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType



class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    bio = Column(Text, nullable=True)
    status = Column(Boolean, default=True)
    profile_picture = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    post = relationship('Post', back_populates='user')  # one to many
    comments = relationship('Comment', back_populates='user')  # one to many
    likes = relationship('Likes', back_populates='user')  # one to many
    follower = relationship('Followers', back_populates='user')  # one to many
    following = relationship('Followers', back_populates='user')  # one to many


class Post(Base):
    post_choises = (
        ("reels", "Reels"),
        ("post", "Post"),
        ("story", "Story")
    )
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    image_path = Column(Text, nullable=False)
    caption = Column(Text, nullable=False)
    post_status = Column(ChoiceType(post_choises), default='post')
    rewies = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    user = relationship("User", back_populates="post")
    likes = relationship("Likes", back_populates="post")
    comments = relationship("Comment", back_populates="post")
    tags = relationship("PostTags", back_populates="post")


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

class Likes(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")





class Follows(Base):
    __tablename__ = 'follows'
    id = Column(Integer, primary_key=True, autoincrement=True)
    follower_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    following_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    follower = relationship("User", back_populates="follower")
    following = relationship("User", back_populates="following")



class Tags(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tag_name = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    post = relationship("PostTags", back_populates="tags")


class PostTags(Base):
    __tablename__ = 'posttags'
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    post = relationship("Post", back_populates="tags")
    tag = relationship("Tags", back_populates="posts")


class Stories(Base):
    __tablename__ = 'stories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    image_url = Column(Text, nullable=False)
    caption = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    expires_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class Messages(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column()



