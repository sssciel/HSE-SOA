import grpc
from google.protobuf import empty_pb2, timestamp_pb2

from postService.app.kafka.producer import producer
from postService.app.posts.models import PostDAO
from proto import post_pb2


async def create_post(self, request, context):
    ts = timestamp_pb2.Timestamp()
    res = await PostDAO().add(
        **{
            "title": request.title,
            "description": request.description,
            "is_private": request.is_private,
            "creator_id": request.creator_id,
            "tags": request.tags,
        }
    )
    post = post_pb2.Post(
        post_id=res.post_id,
        creator_id=res.creator_id,
        title=res.title,
        description=res.description,
        is_private=res.is_private,
        tags=res.tags,
        created_at=ts.FromDatetime(res.created_at),
        updated_at=ts.FromDatetime(res.updated_at),
    )
    print(f"Created new post {post}")
    return post_pb2.PostResponse(post=post)


async def get_post(self, request, context):
    ts = timestamp_pb2.Timestamp()
    res = await PostDAO().find_one(post_id=request.post_id)
    if not res:
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Post not found")
        return post_pb2.PostResponse()
    post = post_pb2.Post(
        post_id=res.post_id,
        creator_id=res.creator_id,
        title=res.title,
        description=res.description,
        is_private=res.is_private,
        tags=res.tags,
        created_at=ts.FromDatetime(res.created_at),
        updated_at=ts.FromDatetime(res.updated_at),
    )

    event = {
        "post_id": request.post_id,
        "creator_id": request.creator_id,
    }
    producer.send(
        topic="views",
        value=event,
    )
    producer.flush()

    return post_pb2.PostResponse(post=post)


async def update_post(self, request, context):
    exists = await PostDAO().find_one(post_id=request.post_id)
    if not exists:
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Post not found")
        return post_pb2.PostResponse()
    if exists.creator_id != request.creator_id:
        context.set_code(grpc.StatusCode.PERMISSION_DENIED)
        context.set_details("You do not have permission to update this post")
        return post_pb2.PostResponse()
    res = await PostDAO().update(
        {"post_id": request.post_id},
        **{
            "title": request.title if request.title else exists.title,
            "description": (
                request.description if request.description else exists.description
            ),
            "is_private": (
                request.is_private
                if request.is_private is not None
                else exists.is_private
            ),
            "tags": request.tags if request.tags else exists.tags,
        },
    )
    if res == 0:
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Post not found")
        return empty_pb2.Empty()
    return empty_pb2.Empty()


async def delete_post(self, request, context):
    exists = await PostDAO().find_one(post_id=request.post_id)
    if not exists:
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Post not found")
        return empty_pb2.Empty()
    res = await PostDAO().delete(post_id=request.post_id)
    if exists.creator_id != request.creator_id:
        context.set_code(grpc.StatusCode.PERMISSION_DENIED)
        context.set_details("You do not have permission to delete this post")
        return empty_pb2.Empty()
    if res == 0:
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Post not found")
        return empty_pb2.Empty()
    return empty_pb2.Empty()


async def list_posts(self, request, context):
    limit = request.limit or 10
    offset = request.offset or 0
    posts = await PostDAO().find_paginated(limit=limit, offset=offset)
    post_list = []
    for res in posts:
        created_ts = timestamp_pb2.Timestamp()
        created_ts.FromDatetime(res.created_at)
        updated_ts = timestamp_pb2.Timestamp()
        updated_ts.FromDatetime(res.updated_at)
        post = post_pb2.Post(
            post_id=res.post_id,
            creator_id=res.creator_id,
            title=res.title,
            description=res.description,
            is_private=res.is_private,
            tags=res.tags,
            created_at=created_ts,
            updated_at=updated_ts,
        )
        post_list.append(post)
    return post_pb2.ListPostsResponse(posts=post_list)
