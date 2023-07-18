from fastapi import APIRouter
from typing import List

from fastapi import Request

import os

app06 = APIRouter()


@app06.post("/items")
async def items(request: Request):
    # 适合小文件上传
    print("URL:", request.url)
    print("客户端IP地址:", request.client.host)
    print("客户端宿主", request.headers.get("user-agent"))
    print("cookies", request.cookies)
    return {
        "URL": request.url,
        "客户端IP地址:": request.client.host,
        "客户端宿主": request.headers.get("user-agent"),
        "cookies": request.cookies.get("a"),
    }
