import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# @app.middleware("http")
# async def CORSMiddleware(request: Request, call_next):
#     response = await call_next(request)
#     response.headers["Access-Control-Allow-Origin"] = "*"
#     return response
origins = [
    "http://localhost:63342"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",  # *：代表所有客户端
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/user")
def get_user():
    print("user:yuan", )
    return {
        "user": "yuan"
    }


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8030, reload=True,
                debug=True, workers=1)
