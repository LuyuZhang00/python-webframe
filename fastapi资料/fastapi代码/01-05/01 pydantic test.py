from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class User(BaseModel):
    id: int  # id 需要是一个整型，必须字段
    name = 'John Doe'  # 默认值
    signup_ts: Optional[datetime] = None
    friends: List[int] = []


external_data = {
    'id': '12',
    'signup_ts': '2019-06-01 12:22',
    'friends': [1, 2, '3'],
}

user = User(**external_data)
print(user.id)
# > 123
print(repr(user.signup_ts))
# > datetime.datetime(2019, 6, 1, 12, 22)
print(user.friends)
# > [1, 2, 3]
print("user", user)
print(user.dict())

