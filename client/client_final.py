import logging
import socket
import sys
import threading
from ast import literal_eval
from random import random
from time import sleep, ctime
from tkinter import *
import json


class Network:
    def __init__(self):
        self.sock = None
        is_bound = False
        f = open('../users.json', 'r+')
        self.data = json.load(f)
        f.close()
        count = 0
        f = open('../users.json', 'w')
        for data in self.data:
            if data['type'] == "host":
                self.port = data['port']
            if not is_bound and data['type'] == 'client' and data['isUsed'] == 0:
                is_bound = True

                self.client_port = data['port']
                self.name = data['name']
                data['isUsed'] = 1
                self.data[count].update(data)
                json.dump(self.data, f)
                print('socket chosen')
            count += 1
        self.host = "127.0.0.1"
        # self.shareData = {"Q": [], "A": []}
        f.close()
        self.connect()

    def connect(self):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("127.0.0.1", self.client_port))
        while True:
            try:
                self.sock.connect((self.host, self.port))
                print(self.port)
                logging.warning("Connected to server")
                break

            except:
                logging.warning("Can't Connect to server!!!")
                sleep(0.5)

    def listen_to_server(self):

        while True:
            try:
                data = self.sock.recv(409600).decode()

                try:
                    return literal_eval(data)

                except:
                    logging.warning("failed to get any data!! : %s", sys.exc_info())
                    return False
            except:

                logging.warning("connection refused! : [%s]", sys.exc_info())
                f = open('../users.json', 'rw')
                count = 0
                for data in self.data:
                    if data['name'] == self.name:
                        data['isUsed'] = 0
                        self.data[count].update(data)
                        json.dump(self.data, f)
                count += 1
                self.sock.close()
                self.connect()
                return False


Network()
