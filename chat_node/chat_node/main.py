import socket
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI


async def send_join_event():
    own_address = socket.gethostbyname(socket.gethostname())
    data = {"name": "chat", "address": own_address}

    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8000/join", json=data)
        res = response.json()
        return res


@asynccontextmanager
async def lifespan(application: FastAPI):
    application.state.temp_data = ["hello", "world"]
    neighbors = await send_join_event()
    app.state.neighbors = list(map(lambda x: x["address"], neighbors))
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
