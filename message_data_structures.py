# this doesn't work!!!!

from dataclasses import dataclass
from datetime import datetime
import json
import os
from sortedcontainers import SortedList
from time import sleep

DIR = os.path.dirname(os.path.abspath(__file__))
REP = os.path.join(DIR, "chat_data")
# REP = os.path.join(DIR, "chat_history")
TIMESTAMP = True

@dataclass
class Message:
    print("Initializing message...")
    username: str
    text: str
    timestamp: datetime# = datetime.now()

    def __repr__(self, timestemp_on) -> str:
        if timestemp_on:
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
        return message

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
    def __init__(self, folder_path=REP, timestamp_on=TIMESTAMP):
        print(f"Initializing chat...{timestamp_on = }")
        self.timestamp_on = timestamp_on
        self.rep = folder_path
        self.users = self.fetch_users()
        self.sorted_list = SortedList(key=lambda msg: msg.timestamp)  # Sort by timestamp
        self.chat_history = self.download_chat_history(timestamp_on=timestamp_on)
        self.last_accessed_index = 0
        

    def fetch_users(self):
        users = []
        for filename in os.listdir(self.rep):
            if filename.endswith("_history.json"):
                username = filename.replace("_history.json", "")
                users.append(User(username))
        return users

    def update_sorted_list(self, downloaded_message):
        # print(type(downloaded_message))
        self.sorted_list.add(downloaded_message)

    def download_chat_history(self, timestamp_on=TIMESTAMP):
        self.sorted_list = SortedList(key=lambda msg: msg.timestamp)  # Sort by timestamp
        chat_history = {}
        for user in self.users:
            chat_history[user.username] = [message.to_dict() for message in user.user_messages]
            for downloaded_message in user.user_messages:
                self.update_sorted_list(downloaded_message)
        print(f"Downloaded {len(self.sorted_list)} messages from {len(self.users)} users")
        # print(f"They are: {self.sorted_list}")
        return chat_history

    def display_chat_history(self):
        for user in self.users:
            print(user)
            for message in user.user_messages:
                # print(repr(message))
                print(message)
            print()

    def get_next_message(self):
        if self.last_accessed_index < len(self.sorted_list):
            message = self.sorted_list[self.last_accessed_index]
            self.last_accessed_index += 1
            return message
        else:
            return None


if __name__ == "__main__":
    chat = Chat(REP)


    # print chat_sorted list with repr with parameter
    print('\n'.join([el.__repr__(1) for el in chat.sorted_list]))
    

    # [print(el) for el in chat.sorted_list]


    # while True:
    #     next_message = chat.get_next_message()
    #     if next_message is not None:
    #         print(next_message)
    #     else:
    #         break

    # print('\n'.join([el for el in chat.sorted_list]))


    # [repr(el) for el in chat.sorted_list]

    # chat.display_chat_history()

    # print every element of sorted list from start line, starting from new line

    # print('\n'.join(list(chat.sorted_list)))



    # print([f"{el}" for el in chat.sorted_list])

    # print([f"{el}" for el in chat.sorted_list])

    # john = User("John")
    # raul = User("Raul")
    # john.add_message("Hello")
    # sleep(0.3)
    # raul.add_message("Hi there!")
    # sleep(0.3)
    # john.add_message("How are you doing?")
    # sleep(0.3)
    # raul.add_message("I'm good, thanks for asking. How about you?")
    # sleep(0.3)
    # john.add_message("I'm doing great!")
    # sleep(0.3)
    # raul.add_message("That's wonderful to hear!")
    # sleep(0.3)
    # john.add_message("By the way, did you watch the latest episode of our favorite show?")
    # sleep(0.3)
    # raul.add_message("Yes! It was so intense. I couldn't believe what happened.")
    # sleep(0.3)
    # john.add_message("I know, right? The plot twists are always mind-blowing.")
    # sleep(0.3)
    # raul.add_message("Absolutely. It keeps us hooked until the very end.")
    # sleep(0.3)
    # john.add_message("Hey, have you tried the new restaurant that opened in town?")
    # sleep(0.3)
    # raul.add_message("Not yet, but I've heard great things about it. Shall we plan a visit?")
    # sleep(0.3)
    # john.add_message("Definitely! Let's make reservations for this weekend.")
    # sleep(0.3)
    # raul.add_message("Sounds like a plan. I'm looking forward to it!")
    # sleep(0.3)
    # john.add_message("Me too. It'll be a fantastic evening.")
    # sleep(0.3)
    # raul.add_message("Hey, did you hear about the upcoming concert?")
    # sleep(0.3)
    # john.add_message("Yes, I did! I've already bought the tickets. Are you going?")
    # sleep(0.3)
    # raul.add_message("Absolutely! I wouldn't miss it for anything.")
    # sleep(0.3)
    # john.add_message("Great! We'll have an amazing time together.")
    # sleep(0.3)
    # raul.add_message("For sure. It's always a blast when we hang out.")
