import asyncio
import json
import time
import uuid
from os import name, path, system

import httpx


class EmptyNodeListException(Exception):
    pass


class ClientSystem:
    def __init__(self):
        self.username = self.whoami()
        self.main_node = "main-node"
        self.chat_node = asyncio.run(self.get_chatnode())
        self.message_store = []

    async def get_chatnode(self):
        async with httpx.AsyncClient() as client:
            res = await client.get(f"http://{self.main_node}/node")
            if res.status_code == 200:
                node = res.json()
                try:
                    return node["chat_node"]["address"]
                except (EmptyNodeListException, KeyError):
                    time.sleep(2)
                    return (
                        await self.get_chatnode()
                    )  # Maybe dangerous way to keep polling for chat nodes.

    def register(self):  # Could be improved using regex.
        print("Welcome! To proceed, please register an account.")
        while True:
            username = input("Enter your username: ")
            stripped = username.strip().lower()
            if len(stripped) <= 0:
                print("Username is invalid, please try again.")
                continue
            with open("config.json", "w", encoding="utf-8") as out:
                json.dump({"name": stripped}, out)
            return stripped

    def whoami(self):
        if path.isfile("./config.json"):
            with open("./config.json", encoding="utf-8") as f:
                data = json.load(f)
                try:
                    return data["name"]
                except KeyError:
                    return self.register()
        return self.register()

    def add_messages_to_store(self, messages):
        self.message_store = list(
            {
                message["id"]: message
                for message in self.message_store + messages
            }.values()
        )

    def send_message(self, message):
        message = {
            "id": uuid.uuid4().hex,
            "sender": self.username,
            "message": message,
        }
        while True:
            try:
                r = httpx.post(
                    f"http://{self.chat_node}/message", json=message
                )
                print(r)
                print(r.text)
                # self.chat_node only contains the IP address, but it's lacking the port,
                # so currently its hard coded to the exposed one.
                res = r.json()  # Potential failure point if res is empty.
                self.add_messages_to_store(res)

                return
            except (httpx.TimeoutException, httpx.ReadTimeout):
                print("Could not connect to chat, getting new one")

                self.chat_node = asyncio.run(self.get_chatnode())

                continue

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

    def start(self):
        while True:
            print(
                f"\n===== Distributed Messenger. Welcome {self.username}!"
                f" Connected to {self.chat_node}. Type (/exit) to exit."
                " =====\n"
            )
            self.print_chat_log()
            message = input("Enter the message: ")
            if message == "/exit":
                break
            self.send_message(message)
            self.clear_chat()


def main():
    client = ClientSystem()
    client.start()


if __name__ == "__main__":
    main()
