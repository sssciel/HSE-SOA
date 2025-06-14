import grpc
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from google.protobuf.json_format import MessageToDict

from apiGateway.app.auth.utils import get_current_user
from apiGateway.app.grpc.posts import get_stub
from proto import post_pb2

stub = get_stub()

router = APIRouter(prefix="/posts/actions", tags=["Posts Actions"])


@router.post("/like/{post_id}")
async def like_post(post_id: int, user_id=Depends(get_current_user)):
    try:
        result = await stub.LikePost(
            post_pb2.PostLikeRequest(post_id=post_id, caller_id=int(user_id))
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


@router.post("/unlike/{post_id}")
async def unlike_post(post_id: int, user_id=Depends(get_current_user)):
    try:
        result = await stub.UnLikePost(
            post_pb2.PostUnLikeRequest(post_id=post_id, caller_id=int(user_id))
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


@router.post("/comment/{post_id}")
async def comment_post(post_id: int, content: str, user_id=Depends(get_current_user)):
    try:
        result = await stub.CommentPost(
            post_pb2.PostCommentRequest(
                post_id=post_id, caller_id=int(user_id), content=content
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
                detail="You do not have permission to access this post",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )

    return MessageToDict(result, preserving_proto_field_name=True)
