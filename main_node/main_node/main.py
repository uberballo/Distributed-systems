from contextlib import asynccontextmanager
import uuid
from pydantic import BaseModel, Field

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(application: FastAPI):
    application.state.temp_data = ["hello", "world"]
    application.state.chat_nodes = []
    yield


class ChatNode(BaseModel):
    name: str
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    address: str


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"temp_data:": app.state.temp_data}


@app.get("/main")
async def read_main():
    return {"Greetings from main node"}


@app.post("/join")
async def handle_node_join(node: ChatNode):
    app.state.chat_nodes.append(node)
    return node


@app.get("/nodes")
async def get_nodes():
    return {"chat_nodes:": app.state.chat_nodes}
