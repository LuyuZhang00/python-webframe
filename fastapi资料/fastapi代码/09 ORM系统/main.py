import uvicorn
from fastapi import FastAPI

from tortoise.contrib.fastapi import register_tortoise
from settings import TORTOISE_ORM
from api.student import student_api

app = FastAPI()

app.include_router(student_api, prefix="/student", tags=["选课系统的学生接口"])

# fastapi一旦运行，register_tortoise已经执行，实现监控
register_tortoise(
    app=app,
    config=TORTOISE_ORM,
)

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8010, reload=True,
                debug=True, workers=1)
