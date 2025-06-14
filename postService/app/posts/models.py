from postService.app.db.base_dao import BaseDAO
from postService.app.posts.schemas import Post


class PostDAO(BaseDAO):
    model = Post
