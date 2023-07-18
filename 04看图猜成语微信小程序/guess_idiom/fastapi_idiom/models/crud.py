from datetime import datetime

import sqlalchemy
from fastapi_idiom.models.database import SessionLocal

from .models import User,Game

db = SessionLocal() # 数据库会话


def get_user(openid: str):
    """
    根据openid获取用户信息
    :param openid: 用户openid
    :return: 用户信息
    """
    return db.query(User).filter(User.openid == openid).first()

def create_user(openid , nickname, avatar):
    """
    创建用户
    :param openid: 用户openid
    :param nickname: 用户昵称
    :param avatar: 用户头像
    :return: User类对象
    """
    db_user = User(
        openid=openid,
        nickname=nickname,
        avatar=avatar,
        level=0,
        addtime=datetime.now()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_total_level():
    """
    所有关卡
    :return:
    """
    return db.query(sqlalchemy.func.count(Game.id)).scalar()

def get_game_info(level: str):
    """
    获取本关游戏信息
    :param level: 关卡名
    :return: 本关游戏信息
    """
    return db.query(Game).filter_by(id=level).first()

def get_rank():
    """
    获取用户排名
    :return: 排名用户信息
    """
    return db.query(User).order_by(User.level.desc()).limit(10).all()

def update_level(openid,level):
    """
    更新用户通过的关卡
    :param openid: 用户openid
    :param level: 关卡
    :return: 用户信息
    """
    user = get_user(openid)
    user.level = level
    db.commit()
    return user
