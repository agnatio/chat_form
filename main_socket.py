import os
import json
import socket
import threading
from datetime import datetime
from PyQt5.QtCore import QCoreApplication, QMetaObject, QRect, QSize, QUrl, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMenuBar, QPushButton, QStatusBar, QTextEdit, QVBoxLayout, QWidget, QAction, QDialog, QGridLayout, QMenu
from message_data_structures import Message, User, Chat
from typing import List



class AuthorizationDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.icon = QIcon(os.path.join(self.current_dir, "fox.ico"))
        self.setWindowTitle("Name Entry")
        self.setFixedSize(250, 150)
        self.setWindowIcon(self.icon)
        layout = QVBoxLayout()
        self.label = QLabel("Please enter your name:")
        layout.addWidget(self.label)
        self.name_field = QLineEdit()
        self.name_field.returnPressed.connect(self.on_submit)
        layout.addWidget(self.name_field)
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.on_submit)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

    def on_submit(self):
        name = self.name_field.text()
        if name:
            self.accept()


class MessingerApp(object):
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.chat_history_folder = os.path.join(self.current_dir, "chat_history")
        self.icon = QIcon(os.path.join(self.current_dir, "fox.ico"))
        self.folder_path: str = None
        self.folder_path2: str = None
        self.client_socket = None

    def setupUi(self, MainWindow: QMainWindow) -> None:
        print("setupUi...")
        self.setup_main_window(MainWindow)
        self.setup_actions(MainWindow)
        self.setup_central_widget(MainWindow)
        self.setup_menu_bar(MainWindow)
        self.setup_status_bar(MainWindow)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

        self.user_name: str = ""
        self.user2: User
        self.chat_history: List[Message] = []
        self.temp_history: List[Message] = []
        self.show_name_dialog()

    def setup_main_window(self, MainWindow: QMainWindow) -> None:
        if MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(675, 570)
        MainWindow.showEvent = self.on_main_window_show
        MainWindow.setWindowIcon(self.icon)
        MainWindow.setWindowTitle("MESSENGER")

    def setup_actions(self, MainWindow: QMainWindow) -> None:
        self.actionDownload_messages = QAction(MainWindow)
        self.actionDownload_messages.setObjectName("actionDownload_messages")
        self.actionDownload_messages.triggered.connect(self.upload_chat_history)

        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionSettings.setCheckable(True)
        self.actionSettings.triggered.connect(lambda: self.upload_chat_history_folder(self.folder_path))

    def setup_central_widget(self, MainWindow: QMainWindow) -> None:
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setReadOnly(True)
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.Send = QPushButton(self.centralwidget)
        self.Send.setObjectName("Send")
        self.Send.setMinimumSize(QSize(100, 30))
        self.Send.setMaximumSize(QSize(200, 30))
        self.Send.clicked.connect(self.on_button_clicked)
        self.lineEdit.returnPressed.connect(self.Send.click)
        self.horizontalLayout.addWidget(self.Send)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

    def setup_menu_bar(self, MainWindow: QMainWindow) -> None:
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 675, 26))
        self.menuChat = QMenu(self.menubar)
        self.menuChat.setObjectName("menuChat")
        self.menuSetup = QMenu(self.menubar)
        self.menuSetup.setObjectName(u"menuSetup")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuChat.menuAction())
        self.menubar.addAction(self.menuSetup.menuAction())
        self.menuChat.addAction(self.actionDownload_messages)
        self.menuSetup.addAction(self.actionSettings)

    def setup_status_bar(self, MainWindow: QMainWindow) -> None:
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

    def on_main_window_show(self, event) -> None:
        self.lineEdit.setFocus(Qt.OtherFocusReason)
        event.accept()

    def show_name_dialog(self) -> None:
        dialog = AuthorizationDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.user_name = dialog.name_field.text()
            self.user2 = User(self.user_name)
            self.label.setText(self.user_name)
            self.connect_to_server()  # Connect to the remote server
        else:
            sys.exit()

    def connect_to_server(self) -> None:
        server_address = "your_server_address"  # Replace with your actual server address
        server_port = 12345  # Replace with the appropriate port number

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_address, server_port))

        # Send the user's name to the server
        self.client_socket.send(self.user_name.encode())

        # Start a separate thread to receive messages from the server
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

    def receive_messages(self) -> None:
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                self.textEdit.append(message)
            except Exception as e:
                print("Error receiving message:", e)
                break

    def send_message(self, message: str) -> None:
        try:
            self.client_socket.send(message.encode())
        except Exception as e:
            print("Error sending message:", e)

    def on_button_clicked(self) -> None:
        text = self.lineEdit.text()
        if text:
            print(f"Time is checked {self.actionSettings.isChecked() = }")
            message2 = self.user2.add_message(text)
            self.lineEdit.clear()
            self.textEdit.append(message2.__repr__(self.actionSettings.isChecked()))
            self.lineEdit.setFocus(Qt.OtherFocusReason)
            self.temp_history.append(message2)
            self.send_message(message2)  # Send the message to the server

    def upload_chat_history(self) -> None:
        """this is complicated logic because of different potential user behaviour. For example start opening a folder and then sopping the process in the middle"""
        if self.folder_path:
            print(f" 1st level Folder path {self.folder_path}")  ####!!!! here must reserve folder path and not let make it empty
            self.folder_path = QFileDialog.getExistingDirectory(None, "Select Folder")
            if self.folder_path:
                print(f" 2nd level Folder path {self.folder_path}")
                self.upload_chat_history_folder(self.folder_path)
            else:
                self.folder_path = self.folder_path2
                print(f" 5nd level Folder path {self.folder_path}")
                self.upload_chat_history_folder(self.folder_path)
        else:
            self.folder_path = QFileDialog.getExistingDirectory(None, "Select Folder")
            self.folder_path2 = self.folder_path
            print(f" 3rd level Folder path {self.folder_path}")
            if self.folder_path:
                print(f" 4nd level Folder path {self.folder_path}")
                self.upload_chat_history_folder(self.folder_path)

    def upload_chat_history_folder(self, folder_path: str) -> None:
        self.chat_history = []
        self.textEdit.clear()
        if not folder_path and not self.folder_path2:
            print("No folder selected and no folder selected previously")
            self.textEdit.clear()
            for message in self.temp_history:
                self.textEdit.append(message.__repr__(self.actionSettings.isChecked()))
        else:
            chat = Chat(folder_path, timestamp_on=self.actionSettings.isChecked())
            while True:
                next_message = chat.get_next_message()
                if next_message is not None:
                    self.textEdit.append(next_message.__repr__(self.actionSettings.isChecked()))
                else:
                    break


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = MessingerApp()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
