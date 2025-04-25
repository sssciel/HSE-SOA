from sqlalchemy.orm import Session
from database import SessionLocal
from models import Post
import service_pb2 as service_pb2
from google.protobuf.timestamp_pb2 import Timestamp

def convert_datetime_to_timestamp(dt):
    ts = Timestamp()
    ts.FromDatetime(dt)
    return ts

def convert_post(post: Post) -> service_pb2.Post:
    created_at = convert_datetime_to_timestamp(post.created_at) if post.created_at else None
    updated_at = convert_datetime_to_timestamp(post.updated_at) if post.updated_at else None
    return service_pb2.Post(
        id=post.id,
        title=post.title,
        description=post.description,
        creator_id=post.creator_id,
        is_private=post.is_private,
        tags=post.tags if post.tags else [],
        created_at=created_at,
        updated_at=updated_at
    )

def create_post(request) -> service_pb2.Post:
    db: Session = SessionLocal()
    try:
        new_post = Post(
            title=request.title,
            description=request.description,
            creator_id=request.creator_id,
            is_private=request.is_private,
            tags=request.tags
        )
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return convert_post(new_post)
    finally:
        db.close()

def delete_post(post_id: int, user_id: int):
    db: Session = SessionLocal()
    try:
        post = db.query(Post).filter(Post.id == post_id, Post.creator_id == user_id).first()
        if post:
            db.delete(post)
            db.commit()
    finally:
        db.close()

def update_post(request) -> service_pb2.Post:
    db: Session = SessionLocal()
    try:
        post = db.query(Post).filter(Post.id == request.id, Post.creator_id == request.user_id).first()
        if not post:
            raise Exception("Post not found")
        if request.title:
            post.title = request.title
        if request.description:
            post.description = request.description
        post.is_private = request.is_private
        if request.tags:
            post.tags = request.tags
        db.commit()
        db.refresh(post)
        return convert_post(post)
    finally:
        db.close()

def get_post(post_id: int, user_id: int) -> service_pb2.Post:
    db: Session = SessionLocal()
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        if post and post.is_private and post.creator_id != user_id:
            return None
        return convert_post(post) if post else None
    finally:
        db.close()

def list_posts(page: int, limit: int, user_id: int) -> service_pb2.ListPostsResponse:
    db: Session = SessionLocal()
    try:
        query = db.query(Post)
        total = query.count()
        posts = query.offset((page - 1) * limit).limit(limit).all()
        posts_proto = [convert_post(p) for p in posts if (not p.is_private or p.creator_id == user_id)]
        return service_pb2.ListPostsResponse(posts=posts_proto, total=total)
    finally:
        db.close()
