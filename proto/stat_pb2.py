class PostStatsRequest:
    def __init__(self, post_id: int = 0):
        self.post_id = post_id


class StatsResponse:
    def __init__(self, views: int = 0, likes: int = 0, comments: int = 0):
        self.views = views
        self.likes = likes
        self.comments = comments


class DynamicRequest:
    def __init__(self, post_id: int = 0):
        self.post_id = post_id


class DayCount:
    def __init__(self, day=None, count: int = 0):
        self.day = day
        self.count = count


class DynamicResponse:
    def __init__(self, items=None):
        self.items = items or []


class TopRequest:
    class StatType:
        VIEWS = 0
        LIKES = 1
        COMMENTS = 2

    def __init__(self, type: int = 0):
        self.type = type


class PostItem:
    def __init__(self, post_id: int = 0, count: int = 0):
        self.post_id = post_id
        self.count = count


class UserItem:
    def __init__(self, user_id: int = 0, count: int = 0):
        self.user_id = user_id
        self.count = count


class TopPostsResponse:
    def __init__(self, posts=None):
        self.posts = posts or []


class TopUsersResponse:
    def __init__(self, users=None):
        self.users = users or []
