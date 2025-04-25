import asyncio
import json
from aiokafka import AIOKafkaProducer
from google.protobuf import empty_pb2
from google.protobuf.timestamp_pb2 import Timestamp
import service_pb2 as service_pb2
import service_pb2_grpc as service_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class PostsService(service_pb2_grpc.PostsServiceServicer):
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.producer = AIOKafkaProducer(
            bootstrap_servers='kafka:9092',
            loop=self.loop
        )
        self.loop.run_until_complete(self.producer.start())

    def CreatePost(self, request, context):
        return create_post(request)

    def DeletePost(self, request, context):
        return delete_post(request)

    def UpdatePost(self, request, context):
        return update_post(request)

    def GetPost(self, request, context):
        return get_post(request)

    def ListPosts(self, request, context):
        return list_posts(request.page, request.limit, request.user_id)

    def ViewPost(self, request, context):
        event = {
            'client_id': request.user_id,
            'post_id': request.post_id,
            'timestamp': Timestamp().GetCurrentTime().ToJsonString()
        }
        self.loop.run_until_complete(
            self.producer.send_and_wait('post_views', json.dumps(event).encode('utf-8'))
        )
        return empty_pb2.Empty()

    def LikePost(self, request, context):
        event = {
            'client_id': request.user_id,
            'post_id': request.post_id,
            'timestamp': Timestamp().GetCurrentTime().ToJsonString()
        }
        self.loop.run_until_complete(
            self.producer.send_and_wait('post_likes', json.dumps(event).encode('utf-8'))
        )
        return empty_pb2.Empty()

    def CommentPost(self, request, context):
        ts = Timestamp()
        ts.GetCurrentTime()
        event = {
            'client_id': request.user_id,
            'post_id': request.post_id,
            'text': request.text,
            'timestamp': ts.ToJsonString()
        }
        self.loop.run_until_complete(
            self.producer.send_and_wait('post_comments', json.dumps(event).encode('utf-8'))
        )
        return service_pb2.Comment(
            post_id=request.post_id,
            user_id=request.user_id,
            text=request.text,
            created_at=ts
        )

    def ListComments(self, request, context):
        return service_pb2.ListCommentsResponse(comments=[], total=0)


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