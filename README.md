

# Console asynchronous messenger

<h3 align="center">  Python asyncio socket messenger </h3>

<p align="center"> 
  <img src="source/console_mes.gif" alt="Animated gif" height="581px" width="900">
</p>

## Overview

<p align="justify"> 
This project presents an asynchronous console chat written using sockets and the asyncio library and (requiring no dependencies). For chat to work, you need one running server listening on a given port and an unlimited number of clients communicating between themselves. Clients connected to the server can use special commands or write messages. List of special commands:
</p>

```bash
change_nick(<your_new_nick>) - changes your nickname on the server
get_clients_info(<>) - returns a list of all clients on the server
connect_by_nick(<nick_of_the_connected_client>) - connects a client with this nick, now this client sees your messages
connect_by_index(<index_of_the_connected_client>) - connects a client with this index, now this client sees your messages
disconnect_by_nick(<nick_of_the_disconnected_client>) - disconnects a client with this nick. now this client does not see your messages
disconnect_by_index(<index_of_the_connected_client>) - disconnects a client with this index. now this client does not see your messages
get_connected_clients(<>) - returns a list of customers who see your messages
```

<p align="justify"> 
Any text is not a command - a message. The message will be sent to all connected clients.
</p>



## Installation
Clone this repo
```bash
https://github.com/DmitriyKhudiakov/Console-asynchronous-messenger.git
```

## Usage
Run server
```bash
server.py
```
Run client
```bash
client.py
```


## License
[MIT](https://choosealicense.com/licenses/mit/)
