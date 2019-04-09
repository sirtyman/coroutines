import socket


host = "127.0.0.1"
port = 44819


def receive():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        print(f"Listening on port {port}")
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                try:
                    msg_received = conn.recv(1024)
                    print(msg_received)

                    conn.send("ACK".encode())
                    print("ACK sent")
                except socket.error as err:
                    print(err)


def main():
    receive()


if __name__ == "__main__":
    main()
