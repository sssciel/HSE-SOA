import grpc
from fastapi import APIRouter, Depends, HTTPException, status
from google.protobuf.json_format import MessageToDict

from apiGateway.app.auth.utils import get_current_user
from apiGateway.app.config import LIST_ON_PAGE
from apiGateway.app.grpc.posts import get_stub
from apiGateway.app.posts.schemas import postCreate, postUpdate
from proto import post_pb2

router = APIRouter(prefix="/post/crud", tags=["Posts CRUD"])


stub = get_stub()


@router.get("/{post_id}")
async def get_post(post_id: int, user_id=Depends(get_current_user)):
    try:
        result = await stub.GetPost(
            post_pb2.PostRequest(post_id=post_id, creator_id=int(user_id))
        )
    except grpc.aio.AioRpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found or access denied",
            )
        if e.code() == grpc.StatusCode.PERMISSION_DENIED:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this post",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )

    return MessageToDict(result, preserving_proto_field_name=True)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(post: postCreate, user_id=Depends(get_current_user)):
    result = await stub.CreatePost(
        post_pb2.CreatePostRequest(
            title=post.title,
            description=post.description,
            is_private=post.is_private,
            creator_id=int(user_id),
            tags=post.tags,
        )
    )

    return MessageToDict(result, preserving_proto_field_name=True)


@router.delete("/{post_id}")
async def delete_post(post_id: int, user_id=Depends(get_current_user)):
    try:
        await stub.DeletePost(
            post_pb2.DeletePostRequest(post_id=post_id, creator_id=int(user_id))
        )
    except grpc.aio.AioRpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found or access denied",
            )
        if e.code() == grpc.StatusCode.PERMISSION_DENIED:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to delete this post",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )

    return True


@router.put("/{post_id}")
async def update_post(
    post_id: int, post: postUpdate, user_id=Depends(get_current_user)
):
    try:
        result = await stub.UpdatePost(
            post_pb2.UpdatePostRequest(
                post_id=post_id,
                title=post.title,
                description=post.description,
                is_private=post.is_private,
                tags=post.tags,
                creator_id=int(user_id),
            )
        )
    except grpc.aio.AioRpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found or access denied",
            )
        if e.code() == grpc.StatusCode.PERMISSION_DENIED:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to update this post",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )

    return MessageToDict(result, preserving_proto_field_name=True)


@router.get("/list/{page}")
async def list_posts(page: int = 1):
    try:
        result = await stub.ListPosts(
            post_pb2.ListPostsRequest(
                limit=LIST_ON_PAGE, offset=(page - 1) * LIST_ON_PAGE
            )
        )
    except grpc.aio.AioRpcError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

    return MessageToDict(result, preserving_proto_field_name=True)
