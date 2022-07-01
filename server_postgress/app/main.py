import uvicorn
from fastapi import FastAPI
from . import routers

app = FastAPI()


api_routers = [
    routers.users_router,
]
for api_router in api_routers:
    app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
