import socket
import asyncio
import random as rnd
import string
from server_classes.Client import Client
from server_scripts import requests as req


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.address = (host, port)
        self.server_socket = None
        self.main_loop = None
        self.loop_task = None
        self.clients = {}

    def create_server_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(self.address)
        self.server_socket.setblocking(False)

    def run_server_socket(self):
        self.server_socket.listen(0)

    @staticmethod
    def send(client, data_send):
        client.socket.sendall(data_send)

    async def listen_client(self, client):
        while True:
            try:
                get_data = await self.main_loop.sock_recv(client.socket, 1024)
            except ConnectionResetError:
                print(f"Client {client.index} disconnected from: {client.address}")
                self.remove_client(client)
                return None
            else:
                if get_data.decode() == "":
                    self.remove_client(client)
                    return None
                else:
                    req.handle_enter(self, client, get_data)

    async def loop(self):
        while True:
            client_socket, address = await self.main_loop.sock_accept(self.server_socket)
            client = Client(client_socket, address, self.gen_client_index(), self.gen_client_nick())
            self.add_client(client)
            print(f"Client {client.index} with nick({client.nick}) connected from: {client.address}")
            self.send(client, req.req_user_info(client))
            self.main_loop.create_task(self.listen_client(client))

    async def run_loop(self):
        try:
            self.loop_task = self.main_loop.create_task(self.loop())
            await self.loop_task
        except asyncio.CancelledError:
            return None

    def run_server(self):
        self.create_server_socket()
        self.run_server_socket()
        self.main_loop = asyncio.get_event_loop()
        self.main_loop.run_until_complete(self.run_loop())

    def add_client(self, client):
        self.clients[client.index] = client

    def remove_client(self, client):
        for key_curr_client in self.clients:
            for curr_connected_clients in self.clients[key_curr_client].connected_clients:
                if curr_connected_clients is client:
                    self.clients[key_curr_client].connected_clients.remove(client)
        self.clients.pop(client.index)

    def gen_client_index(self):
        server_ind = [key for key in self.clients]
        while True:
            index = rnd.randint(0, 99999999)
            if not (index in server_ind):
                break
        return index

    @staticmethod
    def gen_client_nick():
        return "".join(rnd.choice(string.ascii_lowercase) for _ in range(10))
