import os
import json
from datetime import datetime
from PyQt5.QtCore import QCoreApplication, QMetaObject, QRect, QSize, QUrl, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMenuBar, \
    QPushButton, QStatusBar, QTextEdit, QVBoxLayout, QWidget, QAction, QDialog, QGridLayout, QMessageBox, QMenu

class Authorisation(QDialog):
    def __init__(self):
        super().__init__()
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.icon = QIcon(os.path.join(self.current_dir, "fox.ico"))

        self.setWindowTitle("Name Entry")
        self.setFixedSize(150, 100)
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

class Ui_MainWindow(object):
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.chat_history_folder = os.path.join(self.current_dir, "chat_history")
        self.icon = QIcon(os.path.join(self.current_dir, "fox.ico"))

    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(675, 570)
        MainWindow.showEvent = self.on_main_window_show
        MainWindow.setWindowIcon(self.icon)
        MainWindow.setWindowTitle("MESSENGER")
        self.actionDownload_messages = QAction(MainWindow)
        self.actionDownload_messages.setObjectName("actionDownload_messages")
        self.actionDownload_messages.triggered.connect(self.upload_chat_history)
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
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 675, 26))
        self.menuChat = QMenu(self.menubar)
        self.menuChat.setObjectName("menuChat")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuChat.menuAction())
        self.menuChat.addAction(self.actionDownload_messages)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

        self.user_name = ""
        self.chat_history = []

        self.show_name_dialog()

    def on_main_window_show(self, event):
        self.lineEdit.setFocus(Qt.OtherFocusReason)
        event.accept()

    def show_name_dialog(self):
        dialog = Authorisation()
        if dialog.exec_() == QDialog.Accepted:
            self.user_name = dialog.name_field.text()
            self.label.setText(self.user_name)
        else:
            sys.exit()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "MainWindow", None))
        self.actionDownload_messages.setText(QCoreApplication.translate("MainWindow", "Download messages", None))
        self.label.setText(QCoreApplication.translate("MainWindow", "TextLabel", None))
        self.Send.setText(QCoreApplication.translate("MainWindow", "Send", None))
        self.menuChat.setTitle(QCoreApplication.translate("MainWindow", "Chat", None))

    def on_button_clicked(self):
        print('PyQt5 button click')
        text = self.lineEdit.text()
        if text:
            current_time = datetime.now().strftime("%d.%m.%y|%H:%M:%S")
            message = {
                'timestamp': current_time,
                'user': self.user_name,
                'message': text
            }
            print(message)
            self.chat_history.append(message)
            self.lineEdit.clear()
            self.save_chat_history()
            self.update_chat_history()

    def save_chat_history(self):
        filename = os.path.join(self.chat_history_folder, f"{self.user_name}_chat_history.json")
        user_chat_history = [message for message in self.chat_history if message['user'] == self.user_name]
        with open(filename, 'w') as file:
            json.dump(user_chat_history, file, indent=4)

    def update_chat_history(self):
        self.textEdit.clear()
        sorted_history = sorted(self.chat_history, key=lambda x: x['timestamp'])
        for message in sorted_history:
            timestamp = message['timestamp']
            user = message['user']
            text = message['message']
            self.textEdit.append(f"{timestamp} - {user}: {text}")

    def upload_chat_history(self):
        folder_path = QFileDialog.getExistingDirectory(None, "Select Folder")
        if folder_path:
            self.chat_history = []
            for file_name in os.listdir(folder_path):
                if file_name.endswith(".json"):
                    file_path = os.path.join(folder_path, file_name)
                    with open(file_path, 'r') as file:
                        chat_data = json.load(file)
                        self.chat_history.extend(chat_data)
            self.update_chat_history()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
