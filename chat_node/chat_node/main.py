import socket
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from pydantic import BaseModel

class Message(BaseModel):
    sender: str
    message: str
    recipient: str

async def send_join_event():
    own_address = socket.gethostbyname(socket.gethostname())
    data = {"name": "chat", "address": own_address}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://main-node/join", json=data, timeout=1
        )
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

@app.post("/distributemessage")
async def distribute_message(msg: Message):
    print(msg)
    return msg


@app.get("/health")
async def healthcheck():
    return "I AM ALIVE"


@app.get("/main")
async def get_main():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://main-node/main")
        res = response.json()
    return {"Response from main: ": res}
