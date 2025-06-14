from google.protobuf import empty_pb2

from postService.app.kafka.producer import producer


async def comment_post(self, request, context):
    comment = {
        "post_id": request.post_id,
        "comment": request.content,
    }

    producer.send(
        topic="comments",
        value=comment,
    )
    producer.flush()

    return empty_pb2.Empty()


async def list_comments_post(self, request, context):
    return super().ListCommentsPost(request, context)
