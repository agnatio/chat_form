# PyQt5 Chat Window

This is a simple chat window application implemented using PyQt5 library in Python. It allows users to enter their name, send messages, and view the chat history. The chat history is saved to a JSON file with timestamps for each message.

## Prerequisites

* Python 3.x
* PyQt5 library

## Installation

1. Clone the repository or download the source code.
2. Install the required dependencies by running the following command:
   <pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"><button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs">pip install PyQt5
   </code></div></div></pre>

## Usage

Run the `chat_window.py` script to launch the chat window application.

<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>shell</span><button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-shell">python chat_window.py
</code></div></div></pre>

When the application starts, it will prompt you to enter your name in a dialog box. After entering the name, the chat window will appear.

* Enter your message in the text field at the bottom.
* Click the "Send" button to send the message.
* The sent messages will be displayed in the chat area above, along with timestamps.
* The chat history will be saved to a JSON file named `<<username>>_chat_history.json`.

## License

This project is licensed under the MIT License. See the [LICENSE](https://chat.openai.com/LICENSE) file for details.

Feel free to customize and extend the code as per your requirements.

## Acknowledgments

This project was built using the PyQt5 library, which provides a Python interface for the Qt framework. Special thanks to the developers and contributors of PyQt5.

## Resources

* PyQt5 Documentation: [https://www.riverbankcomputing.com/static/Docs/PyQt5/](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
* Qt Documentation: [https://doc.qt.io/qt-5/](https://doc.qt.io/qt-5/)

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## Authors

* Alexey [a](mailto:your.email@example.com)gnatio11@gmail.com

## Contact

For any inquiries or questions, please contact [a](mailto:your.email@example.com)gnatio11@gmail.com
