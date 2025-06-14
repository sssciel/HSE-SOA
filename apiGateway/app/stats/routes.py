from fastapi import APIRouter
from google.protobuf.json_format import MessageToDict

from apiGateway.app.grpc.stats import get_stub
from proto import stat_pb2

router = APIRouter(prefix="/stats", tags=["Statistics"])

stub = get_stub()


@router.get("/post/{post_id}")
async def post_stats(post_id: int):
    result = await stub.GetPostStats(stat_pb2.PostStatsRequest(post_id=post_id))
    return MessageToDict(result, preserving_proto_field_name=True)


@router.get("/top/posts/{stat_type}")
async def top_posts(stat_type: int):
    result = await stub.GetTopPosts(stat_pb2.TopRequest(type=stat_type))
    return MessageToDict(result, preserving_proto_field_name=True)
