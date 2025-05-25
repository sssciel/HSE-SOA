import grpc

from proto import post_pb2, post_pb2_grpc

posts = {}
next_id = 1


class PostServiceServicer(post_pb2_grpc.PostsServiceServicer):
    def CreatePost(self, request, context):
        global next_id

        post = post_pb2.Post(
            post_id=next_id,
            title=request.title,
            description=request.description,
            is_private=request.is_private,
            creator_id=request.creator_id,
            tags=request.tags,
        )

        posts[next_id] = post
        next_id += 1
        print(f"Created new post {post}")

        return post_pb2.PostResponse(post=post)

    def GetPost(self, request, context):
        post = posts.get(request.post_id)
        if not post:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Post not found")
            return post_pb2.PostResponse()

        return post_pb2.PostResponse(post=post)

    def UpdatePost(self, request, context):
        post = posts.get(request.id)
        if not post:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Post not found")
            return post_pb2.PostResponse()
        return super().CreatePost(request, context)
