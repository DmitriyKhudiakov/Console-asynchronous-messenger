

class Client:
    def __init__(self, socket, address, index, nick):
        self.socket = socket
        self.address = address
        self.index = index
        self.nick = nick
        self.connected_clients = []
