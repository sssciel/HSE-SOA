from datetime import datetime

import grpc
from google.protobuf import empty_pb2, timestamp_pb2

from clickhouse_driver import Client
from proto import stat_pb2, stat_pb2_grpc
from statService.app.config import get_clickhouse_url


class StatsServiceServicer(stat_pb2_grpc.StatsServiceServicer):
    def __init__(self) -> None:
        self.client = Client.from_url(get_clickhouse_url())

    async def GetPostStats(self, request, context):
        views = self.client.execute(
            "SELECT count() FROM views WHERE post_id=%(pid)s",
            {"pid": request.post_id},
        )[0][0]
        likes = self.client.execute(
            "SELECT count() FROM likes WHERE post_id=%(pid)s",
            {"pid": request.post_id},
        )[0][0]
        comments = self.client.execute(
            "SELECT count() FROM comments WHERE post_id=%(pid)s",
            {"pid": request.post_id},
        )[0][0]
        return stat_pb2.StatsResponse(views=views, likes=likes, comments=comments)

    async def _dynamic(self, table: str, request):
        records = self.client.execute(
            f"SELECT toDate(time) as day, count() FROM {table} WHERE post_id=%(pid)s GROUP BY day ORDER BY day",
            {"pid": request.post_id},
        )
        res = []
        for day, count in records:
            ts = timestamp_pb2.Timestamp()
            ts.FromDatetime(datetime.combine(day, datetime.min.time()))
            res.append(stat_pb2.DayCount(day=ts, count=count))
        return stat_pb2.DynamicResponse(items=res)

    async def GetPostViewsDynamic(self, request, context):
        return await self._dynamic("views", request)

    async def GetPostLikesDynamic(self, request, context):
        return await self._dynamic("likes", request)

    async def GetPostCommentsDynamic(self, request, context):
        return await self._dynamic("comments", request)

    async def GetTopPosts(self, request, context):
        table = {0: "views", 1: "likes", 2: "comments"}[request.type]
        records = self.client.execute(
            f"SELECT post_id, count() as c FROM {table} GROUP BY post_id ORDER BY c DESC LIMIT 10"
        )
        posts = [stat_pb2.PostItem(post_id=pid, count=c) for pid, c in records]
        return stat_pb2.TopPostsResponse(posts=posts)

    async def GetTopUsers(self, request, context):
        table = {0: "views", 1: "likes", 2: "comments"}[request.type]
        records = self.client.execute(
            f"SELECT user_id, count() as c FROM {table} GROUP BY user_id ORDER BY c DESC LIMIT 10"
        )
        users = [stat_pb2.UserItem(user_id=uid, count=c) for uid, c in records]
        return stat_pb2.TopUsersResponse(users=users)
