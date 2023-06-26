from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QTextEdit, QDialog, QVBoxLayout, QFileDialog
from PyQt5.QtCore import Qt
import os
import sys
from datetime import datetime
import json

class NameDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Name Entry")

        layout = QVBoxLayout()

        self.label = QLabel("Please enter your name:")
        layout.addWidget(self.label)

        self.name_field = QLineEdit()
        self.name_field.returnPressed.connect(self.on_submit)  # Connect Enter key press to on_submit method
        layout.addWidget(self.name_field)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.on_submit)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def on_submit(self):
        name = self.name_field.text()
        if name:
            self.accept()

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 500, 400)
        self.setWindowTitle("Chat Window")
        self.chat_history_folder = "chat_history"

        self.label = QLabel(self)
        self.label.move(50, 50)

        self.text_field = QLineEdit(self)
        self.text_field.move(50, 300)
        self.text_field.resize(300, 30)
        self.text_field.returnPressed.connect(self.on_button_clicked)  # Connect Enter key press to on_button_clicked method

        self.text_area = QTextEdit(self)
        self.text_area.move(50, 100)
        self.text_area.resize(400, 180)
        self.text_area.setReadOnly(True)

        self.button = QPushButton(self)
        self.button.setText("Send")
        self.button.move(250, 300)
        self.button.clicked.connect(self.on_button_clicked)

        self.upload_button = QPushButton(self)
        self.upload_button.setText("Upload History")
        self.upload_button.move(360, 300)
        self.upload_button.clicked.connect(self.upload_chat_history)


        self.user_name = ""
        self.chat_history = []

        self.show_name_dialog()

    def show_name_dialog(self):
        dialog = NameDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.user_name = dialog.name_field.text()
            self.label.setText(self.user_name)

    def on_button_clicked(self):
        text = self.text_field.text()
        if text:
            current_time = datetime.now().strftime("%d.%m.%y|%H:%M:%S")
            message = {
                'timestamp': current_time,
                'user': self.user_name,
                'message': text
            }
            self.chat_history.append(message)
            self.text_field.clear()
            self.save_chat_history()
            self.update_chat_history()

    def save_chat_history(self):
        filename = f"{self.chat_history_folder}/{self.user_name}_chat_history.json"
        user_chat_history = [message for message in self.chat_history if message['user'] == self.user_name]
        with open(filename, 'w') as file:
            json.dump(user_chat_history, file, indent=4)

    def closeEvent(self, event):
        self.save_chat_history()
        event.accept()

    def upload_chat_history(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.chat_history = []
            for file_name in os.listdir(folder_path):
                if file_name.endswith(".json"):
                    file_path = os.path.join(folder_path, file_name)
                    with open(file_path, 'r') as file:
                        chat_data = json.load(file)
                        self.chat_history.extend(chat_data)
            self.update_chat_history()


    def update_chat_history(self):
        self.text_area.clear()
        sorted_history = sorted(self.chat_history, key=lambda x: x['timestamp'])
        for message in sorted_history:
            timestamp = message['timestamp']
            user = message['user']
            text = message['message']
            self.text_area.append(f"{timestamp} - {user}: {text}")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    chat_window = ChatWindow()
    chat_window.show()
    sys.exit(app.exec_())
