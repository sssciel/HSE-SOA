from google.protobuf import empty_pb2

from postService.app.kafka.producer import producer


async def like_post(self, request, context):
    event = {
        "post_id": request.post_id,
        "caller_id": request.caller_id,
    }
    producer.send(
        topic="likes",
        value=event,
    )
    producer.flush()
    return empty_pb2.Empty()


async def unlike_post(self, request, context):
    event = {
        "post_id": request.post_id,
        "creator_id": request.creator_id,
        "caller_id": request.caller_id,
    }
    producer.send(
        topic="unlikes",
        value=event,
    )
    producer.flush()
    return empty_pb2.Empty()
