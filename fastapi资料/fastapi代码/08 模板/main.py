from fastapi import FastAPI
import uvicorn
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

from fastapi import Request


@app.get("/index")
def index(request: Request):
    name = "yuan"
    age = 14

    books = [{"title": "金瓶梅", "price": 400},
             {"title": "聊斋", "price": 199},
             {"title": "剪灯新话", "price": 200},
             {"title": "国色天香", "price": 399},
             ]
    info = {"name": "rain", "age": 32, "gender": "male"}
    pai = 3.1415926

    movies = {"chengnian": ["日韩", "欧美", "国产", "非洲"], "qingshaonian": ["黑猫警长", "熊大熊二", "大头儿子"]}

    return templates.TemplateResponse(
        "index.html",  # 模板文件
        {
            "request": request,
            "user": name,
            "age": age,
            "books": books,
            "info": info,
            "pai": pai,
            "movies": movies
        },  # context上下文对象，一个字典
    )


if __name__ == '__main__':
    uvicorn.run("main:app", port=8090, debug=True, reload=True)
