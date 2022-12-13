from random import choice, random
import socket, threading, time
from ast import literal_eval
from tkinter import *
import logging
import sqlite3
import sys
import os
import json


class Network:
    def __init__(self):
        f = open('../users.json')
        data = json.load(f)
        for i in data:
            if i['type'] == "host":
                self.port = i['port']
        super().__init__()
        self.listClients = []
        self.host = "127.0.0.1"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

        logging.warning("Ready For Connection ...")

    def listen(self):
        self.sock.listen(50)
        while True:
            client, address = self.sock.accept()
            client.settimeout(100)
            self.listClients.append(client)
            thread_clinet = threading.Thread(
                target=self.listenToClient, args=(client, address)
            )
            thread_clinet.daemon = True
            thread_clinet.start()

    def listenToClient(self, client, address):
        print(f"client connected to {client}  {address}")
        while True:

            try:

                recive_data = client.recv(1024).decode()
                #logging.warning("receive data : %s | From : %s", recive_data, address)
                #recive_data = literal_eval(recive_data)
            except:

               # logging.warning("client missing!! : [%s]", sys.exc_info())
                client.close()
                return
"""
                if recive_data["header"] in dic_fn.keys():
                    resp = dic_fn[recive_data["header"]]()
                    client.send(str({"resp": resp}).encode())

                else:
                    client.send(str({"resp": []}).encode())
"""



Network().listen()