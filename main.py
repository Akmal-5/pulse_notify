from app.routers.auth import router as auth_routers
from fastapi import FastAPI
import uvicorn

app = FastAPI()

app.include_router(auth_routers)

if __name__ == "__main__" :
    uvicorn.run("main:app" , reload=True)