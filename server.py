from server_classes.Server import Server


def print_hello_mes():
    print("Hello! You have launched the console chat server.\n")
    print("You can init the server by entering the port and host of the server.\n")


def init_server():
    print_hello_mes()
    while True:
        input_str = input("Enter start() to init server. Enter close() to close script\n")
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
                    server = Server(host, port_int)
                    server.run_server()
                except Exception as e:
                    print("Error: ", e)
                    print(f"Error while connecting to server: host = '{host}', port = '{port_int}'")


def main():
    init_server()


if __name__ == "__main__":
    main()
