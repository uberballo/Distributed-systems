import socket
from asyncio import Lock
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from pydantic import BaseModel


class Message(BaseModel):
    id: str
    sender: str
    message: str


class NodeRequest(BaseModel):
    name: str
    id: str
    address: str


async def send_join_event():
    data = {"name": "chat", "address": app.state.own_address}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://main-node/join", json=data, timeout=1
        )
        res = response.json()
        filtered = list(
            filter(lambda x: x["address"] != app.state.own_address, res)
        )
        return filtered


@asynccontextmanager
async def lifespan(application: FastAPI):
    application.state.messages = []
    application.state.own_address = socket.gethostbyname(socket.gethostname())
    neighbors = await send_join_event()
    app.state.neighbors = list(map(lambda x: x["address"], neighbors))
    app.state.lock = Lock()
    yield


app = FastAPI(lifespan=lifespan)


def contains_message(message: Message):
    return message in app.state.messages


def store_message(message: Message):
    app.state.messages.append(message)


async def forward_message(message: Message):
    async with httpx.AsyncClient() as client:
        for neighbor in app.state.neighbors:
            print(
                f"Sending messages to {neighbor} from {app.state.own_address}"
            )
            try:
                res = await client.post(
                    f"http://{neighbor}/message",
                    json=message.__dict__,
                )
                print(res)
            except (httpx.ConnectTimeout, httpx.ConnectError):
                async with app.state.lock:
                    print(f"Removing neighbor {neighbor}")
                    if neighbor in app.state.neighbors:
                        app.state.neighbors.remove(neighbor)
            except httpx.ReadTimeout:
                pass


@app.get("/")
async def read_root():
    return f"Greetings from {app.state.own_address}"


@app.get("/health")
async def healthcheck():
    return "I AM ALIVE"


@app.post("/message")
async def post_message(message: Message):
    if not contains_message(message):
        store_message(message)
        await forward_message(message)
        return app.state.messages
    return app.state.messages


@app.get("/message")
async def get_messages():
    return app.state.messages


@app.post("/node")
async def post_new_nodes(node: NodeRequest):
    app.state.neighbors.append(node.address)
    return "Ok"


@app.get("/main")
async def get_main():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://main-node/main")
        res = response.json()
    return {"Response from main: ": res}
