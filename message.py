from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    username: str
    text: str
    timestamp: datetime = datetime.now()

class Chat:
    def __init__(self):
        self.chat_history = []

    def send_message(self, username, text):
        message = Message(username=username, text=text)
        self.chat_history.append(message)

    def display_chat_history(self):
        for message in self.chat_history:
            print(f"[{message.timestamp}] {message.username}: {message.text}")

# Create a new chat instance
chat = Chat()

# Send some messages
chat.send_message(username="John", text="Hello there!")
chat.send_message(username="Alice", text="Hi, how are you?")
chat.send_message(username="John", text="I'm doing well, thanks!")

# Display the chat history
chat.display_chat_history()
