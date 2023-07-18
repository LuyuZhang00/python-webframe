from fastapi import APIRouter

app01 = APIRouter()


# 路由匹配顺序
# root用户
@app01.get("/user/1")
def get_user():
    return {
        "user_id": "root user"
    }


@app01.get("/user/{id}")
def get_user(id):
    # id = 1
    print("id", id, type(id))
    return {
        "user_id": id
    }


@app01.get("/articles/{id}")
def get_article(id: int):
    # id = 1
    print("id", id, type(id))
    return {
        "article_id": id
    }
