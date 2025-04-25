from concurrent import futures
import grpc
import time
import service_pb2 as service_pb2
import service_pb2_grpc as service_pb2_grpc
from crud import (
    create_post, delete_post, update_post, get_post, list_posts
)
from database import engine, Base
from models import Post

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class PostsService(service_pb2_grpc.PostsServiceServicer):
    def CreatePost(self, request, context):
        return create_post(request)

    def DeletePost(self, request, context):
        delete_post(request.id, request.user_id)
        from google.protobuf import empty_pb2
        return empty_pb2.Empty()

    def UpdatePost(self, request, context):
        return update_post(request)

    def GetPost(self, request, context):
        post = get_post(request.id, request.user_id)
        if not post:
            context.abort(grpc.StatusCode.NOT_FOUND, "Post not found")
        return post

    def ListPosts(self, request, context):
        return list_posts(request.page, request.limit, request.user_id)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_PostsServiceServicer_to_server(PostsService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    serve()