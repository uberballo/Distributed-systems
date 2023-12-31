import asyncio
import uuid
from asyncio import Task, sleep
from contextlib import asynccontextmanager
from typing import Any

import httpx
from fastapi import FastAPI
from pydantic import BaseModel, Field


class ChatNode(BaseModel):
    name: str
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    address: str


class OurApp(FastAPI):
    temp_data: list[str]
    background_tasks: list[Task]
    chat_nodes: list[ChatNode]
    chat_node_index: int

    def __init__(
        self,
        *,
        temp_data: list[str] | None = None,
        background_tasks: list[Task] | None = None,
        chat_nodes: list[ChatNode] | None = None,
        **fast_api_kwargs: Any,
    ) -> None:
        super().__init__(
            **fast_api_kwargs,
        )
        self.temp_data = temp_data or []
        self.background_tasks = background_tasks or []
        self.chat_nodes = chat_nodes or []
        self.chat_node_index = 0


@asynccontextmanager
async def lifespan(application: OurApp):
    application.temp_data = ["hello", "world"]
    application.chat_nodes = []
    application.background_tasks = []
    background_task = asyncio.create_task(
        healthcheck_nodes(application.chat_nodes)
    )
    application.background_tasks.append(background_task)
    yield


async def healthcheck_nodes(nodes: list[ChatNode]):
    while True:
        await sleep(30)
        for node in nodes:
            print(f"Healthchecking {node}")
            try:
                async with httpx.AsyncClient(timeout=1) as client:
                    print("sending response")
                    response = await client.get(
                        f"http://{node.address}/health"
                    )
                    print("Got response")
                    res = response.json()
                    print(f"{node} is alive, got {res}")
            except httpx.ConnectTimeout:
                print("Node not responding")
                nodes.remove(node)
                print(f"Removed node {node}")


def post_new_nodes(targets: list[ChatNode], new_node: ChatNode):
    for node in targets:
        httpx.post(f"http://{node.address}/node", json=new_node.__dict__)


app = OurApp(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"temp_data": app.temp_data}


@app.get("/main")
async def read_main():
    return {"Greetings from main node"}


@app.post("/join")
async def handle_node_join(node: ChatNode):
    print(f"New node joined: {node}")
    current_nodes = app.chat_nodes
    post_new_nodes(current_nodes, node)
    app.chat_nodes.append(node)

    return current_nodes


@app.get("/nodes")
async def get_nodes():
    return {"chat_nodes": app.chat_nodes}


@app.get("/node")
async def get_node():
    chat_node = app.chat_nodes[app.chat_node_index % len(app.chat_nodes)]
    app.chat_node_index += 1
    return {"chat_node": chat_node}
