
# Messenger App

This is a simple messenger application built using PyQt5. It allows users to send and receive messages in real-time. The application supports downloading chat history and displaying messages with timestamps.

## Features

* User authentication: Users can enter their name to start using the messenger app.
* Real-time messaging: Users can send and receive messages in real-time.
* Download chat history: Users can download chat history from a specified folder.
* Timestamps: Messages can be displayed with timestamps.

## Prerequisites

* Python 3.x
* PyQt5

## Getting Started

1. Clone the repository:
   <pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>bash</span><button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-bash">git clone <repository-url>
   </code></div></div></pre>
2. Install the required dependencies:
   <pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"><button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs">pip install pyqt5
   </code></div></div></pre>
3. Run the application:
   <pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>css</span><button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-css">python main.py
   </code></div></div></pre>

## Usage

1. Launch the application.
2. Enter your name in the authentication dialog and click "Submit".
3. The main window of the messenger app will appear.
4. Type your message in the input field and press Enter or click the "Send" button to send the message.
5. Received messages will be displayed in the chat window.
6. To download chat history, click on the "Actions" menu and select "Download messages". Choose the folder containing the chat history files.
7. The chat history will be displayed in the chat window with timestamps (if enabled).

## License

This project is licensed under the [MIT License](https://chat.openai.com/LICENSE).

## Acknowledgements

* [PyQt5](https://pypi.org/project/PyQt5/): Python bindings for the Qt application framework.
* [OpenAI](https://openai.com/): The underlying technology powering the chatbot assistant.
