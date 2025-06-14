from postService.app.actions.comments import comment_post, list_comments_post
from postService.app.actions.likes import like_post, unlike_post
from postService.app.actions.views import view_post
from postService.app.posts.crud import (
    create_post,
    delete_post,
    get_post,
    list_posts,
    update_post,
)
from proto import post_pb2_grpc


class PostServiceServicer(post_pb2_grpc.PostsServiceServicer):
    # CRUD operations for posts
    CreatePost = create_post
    GetPost = get_post
    UpdatePost = update_post
    DeletePost = delete_post
    ListPosts = list_posts

    # Actions for posts
    LikePost = like_post
    UnLikePost = unlike_post
    CommentPost = comment_post
    ListCommentsPost = list_comments_post
    ViewPost = view_post
