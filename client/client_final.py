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
        f = open('users.json')
        data = json.load(f)
        for i in data:
            if i['type'] == "host":
                self.port = i['port']
                
        self.host = "127.0.0.1"
        #self.shareData = {"Q": [], "A": []}
        self.Connect()

    def Connect(self):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.sock.connect((self.host, self.port))
                print(self.port)
                logging.warning("Connected to server")
                break

            except:
                logging.warning("Can't Connect to server!!!")
                sleep(0.5)

    def listenToServer(self):

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
                self.sock.close()
                self.Connect()
                return False

Network()