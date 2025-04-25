from fastapi import APIRouter, HTTPException, HTTPException, status, Response, Depends, Request
from typing import List

from app.auth_service import get_current_user
from app.post_schemas import postCreate, postUpdate, postOut, postDelete, postList

from app.grpc_client import (
    grpc_create_post, grpc_delete_post,
    grpc_update_post, grpc_get_post, grpc_list_posts
)

router = APIRouter(prefix='/post')

@router.post("/", response_model=postOut, status_code=status.HTTP_201_CREATED)
async def create_post(post: postCreate, user=Depends(get_current_user)):
    user_id = user.get("id")
    return grpc_create_post(post, user_id)

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, user=Depends(get_current_user)):
    user_id = user.get("id")
    existing_post = grpc_get_post(post_id, user_id)
    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found or access denied")
    grpc_delete_post(post_id, user_id)
    return

@router.put("/{post_id}", response_model=postOut)
async def update_post(post_id: int, post: postUpdate, user=Depends(get_current_user)):
    user_id = user.get("id")
    existing_post = grpc_get_post(post_id, user_id)
    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found or access denied")
    return grpc_update_post(post_id, post, user_id)

@router.get("/{post_id}", response_model=postOut)
async def get_post(post_id: int, user=Depends(get_current_user)):
    user_id = user.get("id")
    result = grpc_get_post(post_id, user_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found or access denied")
    return result

@router.get("/", response_model=postList)
async def list_posts(page: int = 1, limit: int = 10, user=Depends(get_current_user)):
    user_id = user.get("id")
    return grpc_list_posts(page, limit, user_id)