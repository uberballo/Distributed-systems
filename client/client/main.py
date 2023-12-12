import uuid
from os import system, name, path
from asyncio import sleep
import json
import httpx
import random
from httpx import ConnectError, ConnectTimeout
import asyncio
import aioconsole


class EmptyResponseListException(Exception):
    pass


class ClientSystem:
    def __init__(self):
        self.username = self.whoami()
        self.main_node = "127.0.0.1:8000"
        self.chat_node = ""
        self.chat_node = asyncio.run(self.get_chatnode())
        self.message_store = []

    async def get_chatnode(self):
        async with httpx.AsyncClient() as client:
            res = await client.get(f"http://{self.main_node}/nodes")
            if res.status_code == 200:
                nodes = res.json()
                try:
                    all_nodes = nodes["chat_nodes"]
                    if len(all_nodes) == 0:
                        raise EmptyResponseListException()
                    return random.choice([
                        node["address"]
                        for node in all_nodes
                        if node["address"] != self.chat_node
                    ])
                except (EmptyResponseListException, KeyError):
                    await sleep(2)
                    return (
                        await self.get_chatnode()
                    )  # Maybe dangerous way to keep polling for chat nodes.

    async def poll_messages(self):
        while True:
            try:
                async with httpx.AsyncClient() as client:
                    res = await client.get(f"http://127.0.0.1:8001/message")
                    messages = (
                        res.json()
                    )  # Add hashing to compare if the recieved messages and currently in store differs. Then clear the screen.
                    self.add_messages_to_store(messages)
            except (ConnectError, ConnectTimeout):
                # Get new chat node, if current fails.
                self.chat_node = await self.get_chatnode()
            await sleep(1)

    def register(self):  # Could be improved using regex.
        print("Welcome! To proceed, please register an account.")
        while True:
            username = input("Enter your username: ")
            stripped = username.strip().lower()
            if len(stripped) <= 0:
                print("Username is invalid, please try again.")
                continue
            with open("config.json", "w") as out:
                json.dump({"name": stripped}, out)
            return stripped

    def whoami(self):
        if path.isfile("./config.json"):
            with open("./config.json") as f:
                data = json.load(f)
                try:
                    return data["name"]
                except KeyError:
                    return self.register()
        return self.register()

    def add_messages_to_store(self, messages):
        new_message_store = list(
            {
                message["id"]: message
                for message in self.message_store + messages
            }.values()
        )
        if len(new_message_store) != len(self.message_store):
            self.message_store = new_message_store
            self.clear_chat()
            self.print_chat_log()

    async def send_message(self, message):
        try:
            async with httpx.AsyncClient() as client:
                client = await client.post(
                    "http://127.0.0.1:8001/message",
                    json={
                        "id": uuid.uuid4().hex,
                        "sender": self.username,
                        "message": message,
                    },
                )  # self.chat_node only contains the ip address, but it's lacking the port, so currently its hard coded to the exposed one.
                res = client.json()  # Potential failure point if res is empty.
                if len(res) == 0:
                    raise EmptyResponseListException()
                self.add_messages_to_store(res)
        except (ConnectError, ConnectTimeout, EmptyResponseListException):
            self.chat_node = await self.get_chatnode()
            await self.send_message(message)

    def print_chat_log(self):
        for message in self.message_store[-15:]:
            print(
                f"{message.get('sender', 'NULL')}:"
                f" {message.get('message', 'NULL')}"
            )

    def clear_chat(self):
        if name == "nt":
            system("cls")
        else:
            system("clear")

    async def start(self, loop):
        print(
            f"\n===== Distributed Messenger. Welcome {self.username}! Type"
            " (/exit) to exit. =====\n"
        )
        while True:
            self.print_chat_log()
            message = await aioconsole.ainput("")
            if message == "/exit":
                loop.stop()
                break
            await self.send_message(message)
            self.clear_chat()


def main():
    pass


if __name__ == "__main__":
    client = ClientSystem()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(client.start(loop))
    loop.create_task(client.poll_messages())
    loop.run_forever()
