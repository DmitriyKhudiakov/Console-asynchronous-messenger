import socket
import asyncio
from client_scripts import requests as req


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.address = (host, port)
        self.client_socket = None
        self.main_loop = None
        self.task_listen = None
        self.task_send = None
        self.index = None
        self.nick = None

    def create_client_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.address)
        self.client_socket.setblocking(False)

    async def listen_server(self):
        while True:
            try:
                get_data = await self.main_loop.sock_recv(self.client_socket, 1024)
            except ConnectionResetError:
                print("\nConnectionResetError\nIt looks like the server has finished working")
                print(f"Enter something to close session with server {self.address}")
                return None
            req.handle_server_message(self, get_data)

    async def send_server(self):
        while True:
            mes = await self.main_loop.run_in_executor(None, input, "")
            # print("\n")
            mes_to_send = req.handle_input(self, mes)
            await self.main_loop.sock_sendall(self.client_socket, mes_to_send)

    async def run_loop(self):
        try:
            self.task_listen = self.main_loop.create_task(self.listen_server())
            self.task_send = self.main_loop.create_task(self.send_server())
            await asyncio.gather(self.task_send, self.task_listen)
        except asyncio.CancelledError:
            return None

    def run_client(self):
        self.create_client_socket()
        self.main_loop = asyncio.get_event_loop()
        self.main_loop.run_until_complete(self.run_loop())
