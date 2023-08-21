# Project 1: XMPP chat

Welcome to my first project for the course **Computer Networks** at Universidad del Valle de Guatemala.


## Project description
This project uses the XMPP protocol, and each student had the freedom to choose the language in which to implement it. 
This project is developed in  🐍 Python 🐍 3.11.4, primarily relying on the slixmpp library. 
The client is implemented in CLI (Command Line Interface), and it's recommended to use the Visual Studio Code CLI as it has implemented colors for this CLI. 
The server used was provided by the course instructor, and the domain was **@alumchat.xyz**.


## Libraries 📚
Below, I list the libraries I used along with their versions.

### External libraries:
* `aioconsole`                `0.6.2`
* `aiofiles`                  `23.2.1`
* `slixmpp`                   `1.8.4`
* `xmpppy`                    `0.7.1`

### Internal libraries
* `time ⏰`
* `base64 🔢`


I chose  🐍 Python 🐍 because I wanted to learn how to program concurrently. Additionally, the book used for the course covers everything in  🐍 Python 🐍. 
Concurrent programming is a challenge, the learning curve is quite steep, but I believe it's necessary to learn it.


## Features

### Account management
- [X] Register: Log into an account, username and password are requested to verify if the user exists. If the user exists, the session is initiated.
- [X] Login: Create an account, username and password are required.
- [X] Account deletion: Delete an account that is no longer desired to continue.

## Functionalities within the chat
- [X] Request roster status: Display availability and status messages of my contacts.
- [X] Add user to contacts:Send a subscription request to a user to be able to interact.
- [X] Show contact details: Request information from a user.
- [X] Direct message: Converse with another user through messaging.
- [X] Group chats: Create, manage, and converse through group chats.
- [X] Change status: Change availability and status message.
- [X] Send file: The client allows a user to send any file to another user.
- [X] Log out: The user can close their session with the server.

## How to use the project

First, you should clone this repository.

```bash
  git clone https://github.com/Aristondo01/P1_Redes_XMPP.git
```

Then, I recommend using Visual Studio Code since the text has been formatted to use colors, which are visible in this IDE.

```bash
  run main.py
```

Make sure you're using the libraries and versions I mentioned above, and once you've done that, you'll have downloaded my XMPP protocol-based chat implementation.
