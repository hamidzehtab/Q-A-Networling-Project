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
            count += 1
        self.host = "127.0.0.1"
        # self.shareData = {"Q": [], "A": []}
        f.close()
        self.connect()
        send_message_thread = threading.Thread(target=self.send_data_to_server, args=(self.name, 'initiate_client', ''))
        send_message_thread.daemon = True
        send_message_thread.start()
        while True:
            input_data = self.listen_to_server()
            print(input_data)

    def connect(self):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("127.0.0.1", self.client_port))
        while True:
            try:
                self.sock.connect((self.host, self.port))
                logging.warning("Connected to server")
                break

            except:
                logging.warning("Can't Connect to server!!!")
                sleep(0.5)

    def listen_to_server(self):

        while True:
            try:
                return self.sock.recv(1024).decode()
            except:

                logging.warning("connection refused! : [%s]", sys.exc_info())
                f = open('../users.json', 'w')
                json.dump(self.data, f)
                return False

    def send_data_to_server(self, name, subject, args=""):

        try:
            self.sock.send(f"{name}:{subject}:{args}".encode())
        except:
            sleep(1)
            print("couldn't send")


Network()
