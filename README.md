# Synthwave LAN Chat

Synthwave LAN Chat is a local network chat application built with Python. It includes a server script and a client script. The client interface is designed with a synthwave aesthetic using the Tkinter library. The application supports basic chat functionalities including broadcasting messages to all users and sending private messages.

## Description

The Synthwave LAN Chat project allows multiple users to connect to a central server and communicate with each other within a local network. Key features include:
- Broadcast messages to all connected users.
- Send private messages to specific users.
- List all connected users.
- Synthwave-themed graphical user interface.

## Requirements

- Python 3.x
- Tkinter (included with Python standard library)
- A local network for server and clients to connect

## How to Run

### Server

1. Open a terminal or command prompt.
2. Navigate to the directory containing `P_Server.py`.
3. Run the server script:
    ```sh
    python P_Server.py
    ```
4. The server will start and listen for incoming connections on port 12345.

### Client

1. Open a terminal or command prompt.
2. Navigate to the directory containing `P_Client.py`.
3. Run the client script:
    ```sh
    python P_Client.py
    ```
4. The client GUI will open. Enter your username and click "Login" to connect to the server.

## Commands

The client application supports the following commands:

1. **List Users:**
/users
This command will display a list of all currently connected users.

2. **Private Message:**
/pm [username] [message]
This command sends a private message to the specified user. Example:
/pm Alice Hello, Alice!

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Python](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
