from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")

async def home () :
    return {
        "message" : "Главная станица"
    }


if __name__ == "__main__" :
    uvicorn.run("main:app" , reload=True)