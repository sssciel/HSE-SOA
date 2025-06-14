class StatsServiceServicer:
    def GetPostStats(self, request, context):
        raise NotImplementedError()

    def GetPostViewsDynamic(self, request, context):
        raise NotImplementedError()

    def GetPostLikesDynamic(self, request, context):
        raise NotImplementedError()

    def GetPostCommentsDynamic(self, request, context):
        raise NotImplementedError()

    def GetTopPosts(self, request, context):
        raise NotImplementedError()

    def GetTopUsers(self, request, context):
        raise NotImplementedError()


def add_StatsServiceServicer_to_server(servicer, server):
    pass
