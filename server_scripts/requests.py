import json


def req_user_info(client):
    ret_dict = dict()
    ret_dict["message_type"] = "user_info"
    ret_dict["index"] = str(client.index)
    ret_dict["nick"] = str(client.nick)
    return json.dumps(ret_dict, indent=4).encode()


def send_message(client, data):
    if len(client.connected_clients) == 0:
        ret_dict = dict()
        ret_dict["message_type"] = "no_clients_connected"
        client.socket.sendall(json.dumps(ret_dict, indent=4).encode())
    else:
        for curr_client in client.connected_clients:
            ret_dict = dict()
            ret_dict["message_type"] = "message"
            ret_dict["message"] = str(data)
            ret_dict["sender"] = str(client.nick)
            curr_client.socket.sendall(json.dumps(ret_dict, indent=4).encode())
        ret_dict = dict()
        ret_dict["message_type"] = "done"
        client.socket.sendall(json.dumps(ret_dict, indent=4).encode())


def get_client_change_nick(server, client, data):
    client.nick = data["nick"]
    print(f"Client with index {client.index} change nick to '{client.nick}'")
    ret_dict = dict()
    ret_dict["message_type"] = "new_nick"
    ret_dict["nick"] = str(client.nick)
    client.socket.sendall(json.dumps(ret_dict, indent=4).encode())


def get_client_clients_info(server, client, data):
    ret_dict = dict()
    ret_dict["message_type"] = "ret_clients_ifo"
    ret_dict["clients"] = "".join("index: " + str(client) + " , nick: " + str(server.clients[client].nick) + "\n"
                                  for client in server.clients)
    client.socket.sendall(json.dumps(ret_dict, indent=4).encode())


def get_client_connect_by_nick(server, client, data):
    nick_connect = data["nick"]
    if nick_connect not in [server.clients[curr_client_index].nick for curr_client_index in server.clients]:
        ret_dict = dict()
        ret_dict["message_type"] = "no_nick"
        ret_dict["nick"] = nick_connect
        client.socket.sendall(json.dumps(ret_dict, indent=4).encode())
    else:
        n_clients_connected = 0
        for curr_client_index in server.clients:
            curr_client = server.clients[curr_client_index]
            if curr_client.nick == nick_connect:
                if curr_client not in client.connected_clients:
                    client.connected_clients.append(curr_client)
                    n_clients_connected += 1
        ret_dict = dict()
        ret_dict["message_type"] = "nick_connected"
        ret_dict["n_clients"] = str(n_clients_connected)
        client.socket.sendall(json.dumps(ret_dict, indent=4).encode())


def get_client_connect_by_index(server, client, data):
    try:
        index_connect = int(data["index"])
    except ValueError:
        return None
    if index_connect not in [int(curr_client_index) for curr_client_index in server.clients]:
        ret_dict = dict()
        ret_dict["message_type"] = "no_index"
        ret_dict["index"] = index_connect
        client.socket.sendall(json.dumps(ret_dict, indent=4).encode())
    else:
        n_clients_connected = 0
        for curr_client_index in server.clients:
            curr_client = server.clients[curr_client_index]
            if int(curr_client.index) == index_connect:
                if curr_client not in client.connected_clients:
                    client.connected_clients.append(curr_client)
                    n_clients_connected += 1
        ret_dict = dict()
        ret_dict["message_type"] = "index_connected"
        ret_dict["n_clients"] = str(n_clients_connected)
        client.socket.sendall(json.dumps(ret_dict, indent=4).encode())


def get_client_disconnect_by_nick(server, client, data):
    nick_disconnect = data["nick"]
    if nick_disconnect not in [server.clients[curr_client_index].nick for curr_client_index in server.clients]:
        ret_dict = dict()
        ret_dict["message_type"] = "no_nick"
        ret_dict["nick"] = nick_disconnect
        client.socket.sendall(json.dumps(ret_dict, indent=4).encode())
    else:
        n_clients_disconnected = 0
        for curr_client_index in server.clients:
            curr_client = server.clients[curr_client_index]
            if curr_client.nick == nick_disconnect:
                if curr_client in client.connected_clients:
                    client.connected_clients.remove(curr_client)
                    n_clients_disconnected += 1
        ret_dict = dict()
        ret_dict["message_type"] = "nick_disconnected"
        ret_dict["n_clients"] = str(n_clients_disconnected)
        client.socket.sendall(json.dumps(ret_dict, indent=4).encode())


def get_client_disconnect_by_index(server, client, data):
    try:
        index_disconnect = int(data["index"])
    except ValueError:
        return None
    if index_disconnect not in [int(curr_client_index) for curr_client_index in server.clients]:
        ret_dict = dict()
        ret_dict["message_type"] = "no_index"
        ret_dict["index"] = index_disconnect
        client.socket.sendall(json.dumps(ret_dict, indent=4).encode())
    else:
        n_clients_disconnected = 0
        for curr_client_index in server.clients:
            curr_client = server.clients[curr_client_index]
            if int(curr_client.index) == index_disconnect:
                if curr_client in client.connected_clients:
                    client.connected_clients.remove(curr_client)
                    n_clients_disconnected += 1
        ret_dict = dict()
        ret_dict["message_type"] = "index_disconnected"
        ret_dict["n_clients"] = str(n_clients_disconnected)
        client.socket.sendall(json.dumps(ret_dict, indent=4).encode())


def get_client_connected_clients(server, client, data):
    ret_dict = dict()
    ret_dict["message_type"] = "connected_clients"
    ret_dict["clients"] = "".join("index: " + str(curr_client.index) + " , nick: " + str(curr_client.nick) + "\n"
                                  for curr_client in client.connected_clients)
    client.socket.sendall(json.dumps(ret_dict, indent=4).encode())


def handle_enter(server, client, data_message):
    global ENTER_FUNC
    data = data_message.decode()
    if data.__contains__("message_type"):
        data_dict = json.loads(data)
        message_type = data_dict.get("message_type")
        if message_type in ENTER_FUNC:
            ENTER_FUNC[message_type](server, client, data_dict)
    else:
        send_message(client, data)


ENTER_FUNC = {
    "change_nick": get_client_change_nick,
    "clients_info": get_client_clients_info,
    "connect_by_nick": get_client_connect_by_nick,
    "connect_by_index": get_client_connect_by_index,
    "disconnect_by_nick": get_client_disconnect_by_nick,
    "disconnect_by_index": get_client_disconnect_by_index,
    "connected_clients": get_client_connected_clients,
}
