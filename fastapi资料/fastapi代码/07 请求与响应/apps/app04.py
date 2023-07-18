from fastapi import APIRouter

from fastapi import Form

app04 = APIRouter()


@app04.post("/regin")
async def reg(username: str = Form(), password: str = Form()):
    print(f"username: {username},password:{password}")
    # 注册，实现数据库的添加操作
    return {
        "username": username
    }
