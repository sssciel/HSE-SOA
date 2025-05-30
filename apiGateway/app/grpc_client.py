import grpc
import os
from app.post_schemas import postOut, postList
import app.service_pb2 as service_pb2
import app.service_pb2_grpc as service_pb2_grpc

from google.protobuf.timestamp_pb2 import Timestamp

GRPC_SERVICE_ADDRESS = os.getenv("GRPC_SERVICE_ADDRESS", "postservice:50051")

def get_grpc_channel():
    return grpc.insecure_channel(GRPC_SERVICE_ADDRESS)

def grpc_create_post(post, user_id: int):
    channel = get_grpc_channel()
    stub = service_pb2_grpc.PostsServiceStub(channel)
    request = service_pb2.CreatePostRequest(
        title=post.title,
        description=post.description,
        creator_id=user_id,
        is_private=post.is_private,
        tags=post.tags
    )
    response = stub.CreatePost(request)
    return postOut(
        id=response.id,
        title=response.title,
        description=response.description,
        creator_id=response.creator_id,
        is_private=response.is_private,
        tags=list(response.tags),
        created_at=response.created_at.ToDatetime(),
        updated_at=response.updated_at.ToDatetime(),
    )

def grpc_delete_post(post_id: int, user_id: int):
    channel = get_grpc_channel()
    stub = service_pb2_grpc.PostsServiceStub(channel)
    request = service_pb2.DeletePostRequest(id=post_id, user_id=user_id)
    stub.DeletePost(request)

def grpc_update_post(post_id: int, post, user_id: int):
    channel = get_grpc_channel()
    stub = service_pb2_grpc.PostsServiceStub(channel)
    request = service_pb2.UpdatePostRequest(
        id=post_id,
        title=post.title or "",
        description=post.description or "",
        is_private=post.is_private if post.is_private is not None else False,
        tags=post.tags or [],
        user_id=user_id
    )
    response = stub.UpdatePost(request)
    return postOut(
        id=response.id,
        title=response.title,
        description=response.description,
        creator_id=response.creator_id,
        is_private=response.is_private,
        tags=list(response.tags),
        created_at=response.created_at,
        updated_at=response.updated_at,
    )

def grpc_get_post(post_id: int, user_id: int):
    channel = get_grpc_channel()
    stub = service_pb2_grpc.PostsServiceStub(channel)
    request = service_pb2.GetPostRequest(id=post_id, user_id=user_id)
    response = stub.GetPost(request)
    if not response:
        return None
    return postOut(
        id=response.id,
        title=response.title,
        description=response.description,
        creator_id=response.creator_id,
        is_private=response.is_private,
        tags=list(response.tags),
        created_at=response.created_at,
        updated_at=response.updated_at,
    )

def grpc_list_posts(page: int, limit: int, user_id: int):
    channel = get_grpc_channel()
    stub = service_pb2_grpc.PostsServiceStub(channel)
    request = service_pb2.ListPostsRequest(page=page, limit=limit, user_id=user_id)
    response = stub.ListPosts(request)
    posts = []
    for p in response.posts:
        posts.append(postOut(
            id=p.id,
            title=p.title,
            description=p.description,
            creator_id=p.creator_id,
            is_private=p.is_private,
            tags=list(p.tags),
            created_at=p.created_at,
            updated_at=p.updated_at,
        ))
    return postList(posts=posts, total=response.total)