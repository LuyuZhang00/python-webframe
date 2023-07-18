from fastapi import APIRouter
from fastapi import Form
from ..utils.user_auth import create_access_token,get_wechat_openid
from datetime import timedelta
from ..models.crud import get_user,create_user,get_total_level


ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

@router.post('/wx_login/')
def wx_login(code: str = Form(...),nickname: str = Form(...),avatar: str = Form(...)):
    if not code or len( code ) < 1:
        result = {
            "code": -1,
            "msg": "需要微信授权code",
            "data": {}
        }
        return {'result': result}
    # 获取openid
    openid = get_wechat_openid(code)
    if openid is None:
        result = {
            "code": -1,
            "msg": "调用微信出错",
            "data": {}
        }
        return {'result': result}

    user = get_user(openid) # 根据opendi查找user表信息
    # 如果user信息不存在，写入user表
    if not user:
        create_user(openid,nickname,avatar)
        level = 0           # 用户等级设置为0
    else:
        level = user.level  # 获取当前用户等级
    # 创建Token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"openid": openid}, expires_delta=access_token_expires
    )
    # 拼接result
    result = {
        "code":1,
        "msg":"登录成功",
        "data":
            {"user_info":
                 {
                     "nickName": nickname,
                     "avatar": avatar,
                     "level": level,
                 },
            "total_level": get_total_level(),
            "token": access_token,
            }
    }
    return {'result': result}