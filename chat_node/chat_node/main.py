from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(application: FastAPI):
    application.state.temp_data = ["hello", "world"]
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"temp_data:": app.state.temp_data}


@app.get("/main")
async def get_main():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://main-node:8000/main")
        res = response.json()
    return {"Response from main: ": res}
