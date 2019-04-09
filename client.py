import socket
import random
import string


host = "127.0.0.1"
port = 44819

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
len_of_printable = len(string.printable)


def send():
    while True:
        seq_num = yield
        message = yield
        data_to_send = "{%s}: {%s}" % (seq_num, message)
        s.sendall(data_to_send.encode())
        print(s.recv(1024))
        yield


def build_random_message():
    message = ''

    for _ in range(100):
        rand = random.randint(0, len_of_printable - 1)
        message += string.printable[rand]

    return message


def execute_senders(senders):
    seq_num = 0

    for sender in senders:
        next(sender)

    while True:
        for sender in senders:
            sender.send(seq_num)

        for sender in senders:
            message = build_random_message()
            sender.send(message)

        for sender in senders:
            print(f"Response: {next(sender)}")

        input("Press Enter to continue")
        seq_num += 1


def initialize_pool(pool_num):
    pool = []
    for _ in range(pool_num):
        pool.append(send())
    return pool


def main():
    pool_num = 2
    senders = initialize_pool(pool_num)

    execute_senders(senders)


if __name__ == '__main__':
    main()
