import grpc
from google.protobuf import empty_pb2, timestamp_pb2

from postService.app.kafka.producer import producer
from proto import post_pb2, post_pb2_grpc


async def view_post(self, request, context):
    event = {
        "post_id": request.post_id,
    }
    producer.send(
        topic="views",
        value=event,
    )
    producer.flush()
    return empty_pb2.Empty()
