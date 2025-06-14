import grpc

from apiGateway.app.config import config
from proto import stat_pb2_grpc

channel = grpc.aio.insecure_channel(config.STATS_SERVICE_URL)
stub = stat_pb2_grpc.StatsServiceStub(channel)


def get_stub():
    return stub
