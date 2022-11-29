import requests
import bs4 as bs
import os
import socket


def initialize_connection():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect(('127.0.0.1', 9998))
    while True:
        message = input("enter smth: ").encode()
        connection.send(message)
        print(connection.recv(1024))


if __name__ == '__main__':
    initialize_connection()
