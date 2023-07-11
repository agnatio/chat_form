# this doesn't work!!!!

from dataclasses import dataclass
from datetime import datetime
import json
import os
from sortedcontainers import SortedList
from time import sleep
from enum import Enum

DIR = os.path.dirname(os.path.abspath(__file__))
REP = os.path.join(DIR, "chat_data")

# Define an enum class with 'TIMESTAMP' taking True or False values
class Options(Enum):
    TIMESTAMP = False

@dataclass
class Message:
    print("Initializing message...")
    username: str
    text: str
    timestamp: datetime = datetime.now()

    def __repr__(self) -> str:
        if Options.TIMESTAMP:
            formatted_timestamp = self.timestamp.strftime("%d-%m-%Y %H:%M:%S")
            return f"{formatted_timestamp} - {self.username}: {self.text}"
        else:
            return f"{self.username}: {self.text}"

    def to_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "username": self.username,
            "text": self.text
        }


class User:
    def __init__(self, username):
        self.username = username
        self.user_messages = []
        self.json_file = os.path.join(REP, f"{self.username}_history.json")
        if not os.path.exists(self.json_file):
            self.create_empty_json_file()
        else:
            self.load_messages()

    def create_empty_json_file(self):
        with open(self.json_file, "w") as f:
            json.dump([], f)

    def add_message(self, text):
        timestamp = datetime.now()
        message = Message(username=self.username, text=text, timestamp=timestamp)
        self.user_messages.append(message)
        self.save_messages()

    def load_messages(self):
        try:
            with open(self.json_file, "r") as f:
                messages = json.load(f)
                for message in messages:
                    timestamp_fromisoformat = datetime.fromisoformat(message["timestamp"])
                    self.user_messages.append(Message(
                        username=message["username"],
                        text=message["text"],
                        timestamp=timestamp_fromisoformat
                    ))
                print(f"Loaded {len(self.user_messages)} messages from {self.username}_history.json")
        except (json.JSONDecodeError, FileNotFoundError):
            self.user_messages = []

    def save_messages(self):
        with open(self.json_file, "w") as f:
            json.dump([message.to_dict() for message in self.user_messages], f, indent=4)


class Chat:
    def __init__(self):
        self.users = self.fetch_users()
        self.sorted_list = SortedList(key=lambda msg: msg.timestamp)  # Sort by timestamp
        self.chat_history = self.download_chat_history()
        self.last_accessed_index = 0

    def fetch_users(self):
        users = []
        for filename in os.listdir(REP):
            if filename.endswith("_history.json"):
                username = filename.replace("_history.json", "")
                users.append(User(username))
        return users

    def update_sorted_list(self, downloaded_message):
        self.sorted_list.add(downloaded_message)

    def download_chat_history(self):
        self.sorted_list = SortedList(key=lambda msg: msg.timestamp)  # Sort by timestamp
        chat_history = {}
        for user in self.users:
            chat_history[user.username] = [message.to_dict() for message in user.user_messages]
            for downloaded_message in user.user_messages:
                self.update_sorted_list(downloaded_message)
        print(f"Downloaded {len(self.sorted_list)} messages from {len(self.users)} users")
        print(f"They are: {self.sorted_list}")
        return chat_history

    def display_chat_history(self):
        for user in self.users:
            print(user)
            for message in user.user_messages:
                print(repr(message))
            print()

    def get_next_message(self):
        if self.last_accessed_index < len(self.sorted_list):
            message = self.sorted_list[self.last_accessed_index]
            self.last_accessed_index += 1
            return message
        else:
            return None


if __name__ == "__main__":
    chat = Chat()

    while True:
        next_message = chat.get_next_message()
        if next_message is not None:
            print(next_message)
        else:
            break

    # chat.display_chat_history()

    # john = User("John")
    # raul = User("Raul")
    # john.add_message("John started")
    # sleep(1)
    # raul.add_message("Raul answered")
    # sleep(1)
    # john.add_message("John 2")
    # sleep(1)
    # raul.add_message("Raul 2")
    # sleep(1)
    # john.add_message("John 3!")
