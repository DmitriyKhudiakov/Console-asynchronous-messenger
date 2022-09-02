import json


def get_server_user_info(client, data):
    client.index = data["index"]
    client.nick = data["nick"]
    print("You are connected to server!")
    print(f"Your id = {client.index}, nick = {client.nick}")


def get_server_new_nick(client, data):
    client.nick = data["nick"]
    print(f"Your new nick is '{client.nick}'")


def get_server_clients_info(client, data):
    clients = data["clients"]
    print(f"Connected clients on the server:\n{clients}")


def get_server_message(client, data):
    sender = data["sender"]
    message = data["message"]
    print(f"Message from {sender} : {message}")


def get_server_no_clients_connected(client, data):
    print("No clients connected... Connect with clients to chat")


def get_server_done(client, data):
    print("                                                    Your message delivered")


def get_server_no_nick(client, data):
    nick = data["nick"]
    print(f"No connected clients with '{nick}' nickname")


def get_server_nick_connected(client, data):
    n_clients = int(data["n_clients"])
    if n_clients > 1:
        print(f"{n_clients} clients connected")
    else:
        print(f"{n_clients} client connect")


def get_server_no_index(client, data):
    index = data["index"]
    print(f"No connected clients with '{index}' index")


def get_server_index_connected(client, data):
    n_clients = int(data["n_clients"])
    if n_clients > 1:
        print(f"{n_clients} clients connected")
    else:
        print(f"{n_clients} client connect")


def get_server_nick_disconnected(client, data):
    n_clients = int(data["n_clients"])
    if n_clients > 1:
        print(f"{n_clients} clients disconnected")
    else:
        print(f"{n_clients} client disconnect")


def get_server_index_disconnected(client, data):
    n_clients = int(data["n_clients"])
    if n_clients > 1:
        print(f"{n_clients} clients disconnected")
    else:
        print(f"{n_clients} client disconnect")


def get_server_connected_clients(client, data):
    clients = data["clients"]
    print(f"Connected clients :\n{clients}")


def handle_server_message(client, data_message):
    global SERVER_GET_FUNC
    data = data_message.decode()
    if data.__contains__("message_type"):
        data_dict = json.loads(data)
        message_type = data_dict.get("message_type")
        if message_type in SERVER_GET_FUNC:
            SERVER_GET_FUNC[message_type](client, data_dict)


def input_change_nick(client, str_input):
    body_request = str_input[str_input.find("(") + 1:len(str_input) - str_input[::-1].find(")") - 1].split(",")
    ret_dict = dict()
    ret_dict["message_type"] = "change_nick"
    ret_dict["nick"] = body_request[0]
    return json.dumps(ret_dict, indent=4).encode()


def input_clients_info(client, str_input):
    ret_dict = dict()
    ret_dict["message_type"] = "clients_info"
    return json.dumps(ret_dict, indent=4).encode()


def input_connect_by_nick(client, str_input):
    body_request = str_input[str_input.find("(") + 1:len(str_input) - str_input[::-1].find(")") - 1].split(",")
    ret_dict = dict()
    ret_dict["message_type"] = "connect_by_nick"
    ret_dict["nick"] = body_request[0]
    return json.dumps(ret_dict, indent=4).encode()


def input_connect_by_index(client, str_input):
    body_request = str_input[str_input.find("(") + 1:len(str_input) - str_input[::-1].find(")") - 1].split(",")
    ret_dict = dict()
    ret_dict["message_type"] = "connect_by_index"
    ret_dict["index"] = body_request[0]
    return json.dumps(ret_dict, indent=4).encode()


def input_disconnect_by_nick(client, str_input):
    body_request = str_input[str_input.find("(") + 1:len(str_input) - str_input[::-1].find(")") - 1].split(",")
    ret_dict = dict()
    ret_dict["message_type"] = "disconnect_by_nick"
    ret_dict["nick"] = body_request[0]
    return json.dumps(ret_dict, indent=4).encode()


def input_disconnect_by_index(client, str_input):
    body_request = str_input[str_input.find("(") + 1:len(str_input) - str_input[::-1].find(")") - 1].split(",")
    ret_dict = dict()
    ret_dict["message_type"] = "disconnect_by_index"
    ret_dict["index"] = body_request[0]
    return json.dumps(ret_dict, indent=4).encode()


def input_connected_clients(client, str_input):
    ret_dict = dict()
    ret_dict["message_type"] = "connected_clients"
    return json.dumps(ret_dict, indent=4).encode()


def handle_input(client, str_input):
    global INPUT_FUNC
    if ("(" in str_input) and (")" in str_input):
        if str_input.find("(") < str_input.find(")"):
            input_command = str_input[:str_input.find("(")].replace(" ", "")
            if input_command in INPUT_FUNC:
                return INPUT_FUNC[input_command](client, str_input)
    return str_input.encode()


INPUT_FUNC = {
    "change_nick": input_change_nick,
    "get_clients_info": input_clients_info,
    "connect_by_nick": input_connect_by_nick,
    "connect_by_index": input_connect_by_index,
    "disconnect_by_nick": input_disconnect_by_nick,
    "disconnect_by_index": input_disconnect_by_index,
    "get_connected_clients": input_connected_clients,
}


SERVER_GET_FUNC = {
    "user_info": get_server_user_info,
    "new_nick": get_server_new_nick,
    "ret_clients_ifo": get_server_clients_info,
    "message": get_server_message,
    "no_clients_connected": get_server_no_clients_connected,
    "done": get_server_done,
    "no_nick": get_server_no_nick,
    "nick_connected": get_server_nick_connected,
    "no_index": get_server_no_index,
    "index_connected": get_server_index_connected,
    "nick_disconnected": get_server_nick_disconnected,
    "index_disconnected": get_server_index_disconnected,
    "connected_clients": get_server_connected_clients,
}
