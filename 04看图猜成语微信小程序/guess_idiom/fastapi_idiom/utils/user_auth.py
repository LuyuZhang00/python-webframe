from datetime import datetime, timedelta
import json

import jwt
from jwt import PyJWTError
from fastapi import  HTTPException, status
import requests

from ..config import Config


SECRET_KEY = "mrsoft"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_wechat_openid(code):
    url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code".format(
        Config.AppID, Config.AppSecret, code)
    r = requests.get(url)
    result = json.loads(r.text)
    openid = None
    if 'openid' in result:
        openid = result['openid']
    return openid

def create_access_token(*, data: dict, expires_delta: timedelta = None):
    """
    创建Token
    :param data: 字典类型数据
    :param expires_delta: 过期时间
    :return: 包含access_token和token_type的字典
    """
    to_encode = data.copy() # 复制data副本
    # 设置过期时间
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire}) # 更新过期时间
    # Token编码
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def auth_token(token: str ):
    """
    验证Token
    :param token: 提交的Token
    :return: openid
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Token解码
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        openid: str = payload.get("openid")
        if openid is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    return {"openid": openid}




