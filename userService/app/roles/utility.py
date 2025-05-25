import enum

"""
Уровни доступа к сервису:

Banned - не может создавать посты и комментировать
User - обычный пользователь
Admin - может удалять посты и банить пользователей
"""


class AccessLevel(int, enum.Enum):
    banned = 0
    user = 1
    admin = 2
