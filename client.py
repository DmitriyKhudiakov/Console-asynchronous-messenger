from client_classes.Client import Client


def print_hello_mes():
    print("Hello! You have launched the console chat client.\n")
    print("You can connect to the server by entering the port and host of the server.\n")
    print("The commands available to you after connecting to the server:")
    print("change_nick(<your_new_nick>) - changes your nickname on the server ")
    print("get_clients_info() - returns a list of all clients on the server")
    print("connect_by_nick(<nick_of_the_connected_client>) - connects a client with this nick, now this "
          "client sees your messages")
    print("connect_by_index(<index_of_the_connected_client>) - connects a client with this index, now this "
          "client sees your messages")
    print("disconnect_by_nick(<nick_of_the_disconnected_client>) - disconnects a client with this nick. now this "
          "client does not see your messages ")
    print("disconnect_by_index(<index_of_the_connected_client>) - disconnects a client with this index. now this "
          "client does not see your messages ")
    print("get_connected_clients() - returns a list of customers who see your messages")
    print("\n")


def init_client():
    print_hello_mes()
    while True:
        input_str = input("Enter start() to init client. Enter close() to close script\n")
        if input_str.replace(" ", "") == "close()":
            break
        elif input_str.replace(" ", "") == "start()":
            host = input("Enter server host: ")
            port = input("Enter server port: ")
            try:
                port_int = int(port)
            except ValueError:
                print(f"Error while connecting to server: host = '{host}', port = '{port}'")
            else:
                try:
                    client = Client(host, port_int)
                    client.run_client()
                except Exception as e:
                    print("Error: ", e)
                    print(f"Error while connecting to server: host = '{host}', port = '{port_int}'")


def main():
    init_client()


if __name__ == "__main__":
    main()
