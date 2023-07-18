from fastapi import APIRouter,Form, Header

from ..models.crud import get_game_info,get_rank,update_level
from ..utils.user_auth import auth_token

router = APIRouter()

@router.post('/guess')
def guess(level:str = Form(...)):
    try:
        game_info = get_game_info(level)
        result = {
            "code": 1,
            "data": {
                    "answer": game_info.answer,
                    "options": game_info.options.split(","),
                    "image": game_info.picture_url
                },
            "message": "请求成功"
        }
    except:
        result = {
            "code": 0,
            "data": {},
            "message": "请求失败"
        }
    return {'result': result}


@router.post('/rank')
def rank():
    users = get_rank()
    data = []
    for item in users:
        userInfo = {
            "userId": item.id,
            "nickname": item.nickname,
            "avatar": item.avatar,
            "level": item.level,
        }
        data.append(userInfo)
    # 返回结果
    result = {
        "code":1,
        "msg":"请求成功",
        "data": data
    }
    return {'result': result}

@router.post('/update_level')
def update(level:str = Form(...),authorization: str = Header(...)):
    try:
        token = authorization.split(' ')[-1]
        openid = auth_token(token)['openid']
        print(f'openid is {openid}')
        update_level(openid,level)
        result = {
            "code": 1,
            "msg": "请求成功",
            "data": {
                "level": level
            }
        }
    except:
        result = {
                "code": 0,
                "msg": "更新失败",
                "data": {}
            }
    return {'result': result}



