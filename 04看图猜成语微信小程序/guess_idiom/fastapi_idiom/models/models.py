from sqlalchemy import Column, Integer, String, DateTime
from fastapi_idiom.models.database import Base
from datetime import datetime

# 会员数据模型
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)  # 编号
    openid = Column(String(80))     # 微信用户id
    nickname = Column(String(100))  # 用户名
    avatar = Column(String(255))    # 头像
    level = Column(Integer)        # 通过关卡
    addtime = Column(DateTime, index=True, default=datetime.now)  # 注册时间

    def __repr__(self):
        return '<User %r>' % self.nickname

# 考题数据模型
class Game(Base):
    __tablename__ = "game"
    id = Column(Integer, primary_key=True)  # 编号
    picture_url = Column(String(255))       # 图片url
    answer = Column(String(20))             # 答案
    options = Column(String(100))           # 备选项
    addtime = Column(DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return '<Game %r>' % self.answer
