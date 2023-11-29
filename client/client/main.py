import os
import json
import httpx

class ClientSystem:

    def __init__(self):
        self.username = self.whoami()
    
    def register(self): # Could be improved using regex.
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
        if os.path.isfile('./config.json'):
            with open('./config.json') as f:
                data = json.load(f)
                try:
                    return data['name']
                except KeyError:
                    return self.register()
        return self.register()

    def send_message(self, recipient, message):
        r = httpx.post('http://localhost:8001/distributemessage', json={"sender": self.username, "recipient": recipient, "message": message})
        print(r.text)

    def display_menu(self):
        print(f"\n===== System Menu ({self.username}) =====")
        print("1. Send a Message")
        print("2. Exit")

    def start(self):
        while True:
            self.display_menu()
            choice = input("Enter your option (1-2): ")

            if choice == "1":
                #Check that message and recipient are in valid format.
                recipient = input("Please enter recipient username: ")
                message = input("Please enter the message: ")
                self.send_message(recipient, message)
            elif choice == "2":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 2.")

    
def main():
    pass


if __name__ == "__main__":
    client = ClientSystem()
    client.start()