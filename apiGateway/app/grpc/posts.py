import grpc

from apiGateway.app.config import config
from proto import post_pb2_grpc

channel = grpc.aio.insecure_channel(config.POST_SERVICE_URL)
stub = post_pb2_grpc.PostsServiceStub(channel)


def get_stub():
    return stub
