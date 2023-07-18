from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
async def home():
    return {"user_id": 1002}


@app.get("/shop")
async def shop():
    return {"shop": "商品信息"}


if __name__ == '__main__':
    uvicorn.run("03 fastapi quickstart:app", port=8080, debug=True, reload=True)
