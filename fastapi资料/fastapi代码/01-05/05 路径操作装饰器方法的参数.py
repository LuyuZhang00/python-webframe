from typing import Union

from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.post("/items", tags=["这是items测试接口"],
          summary="this is items测试 summary",
          description="this is items测试 description...",
          response_description="this is items测试 response_description...",
          deprecated=True,
          )
def test():
    return {"items": "items数据"}


if __name__ == '__main__':
    uvicorn.run("05 路径操作装饰器方法的参数:app", port=8080, debug=True, reload=True)
