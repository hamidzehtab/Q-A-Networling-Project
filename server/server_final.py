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
                target=self.listen_to_client, args=(client, address)
            )
            thread_clinet.daemon = True
            thread_clinet.start()

    def listen_to_client(self, client, address):
        print(f"client connected to {client}  {address}")
        dic_fn = {
            "start_game": lambda: self.start_game(name, args),
            "initiate_client": lambda: self.initiate_client(name, args),
            "checkInfoUser": lambda: self.checkInfoUser(receive_data["args"]),
            "insertAnswer": lambda: self.insertAnswer(receive_data["args"]),
            "getQuestions": lambda: self.getQuestions(receive_data["args"]),
            "deleteAnswer": lambda: self.deleteAnswer(receive_data["args"]),
            "insertUser": lambda: self.insertUser(receive_data["args"]),
            "checkUsers": lambda: self.checkUsers(receive_data["args"]),
            "getAnswers": lambda: self.getAnswers(receive_data["args"]),
        }

        while True:
            #try:
                receive_data = client.recv(1024).decode()
                print("receive data : %s | From : %s", receive_data, address)
                name, method, args = receive_data.split(':')
                print(name, method, args)
                if method in dic_fn.keys():
                    resp = dic_fn[method]()
                    client.send(str(resp).encode())

                else:
                    client.send("error".encode())

            #except:
             #   logging.warning("client missing!! : [%s]", sys.exc_info())
              #  client.close()
               # return

    def initiate_client(self, name, args):
        print('hello')
        self.sock.send("game started".encode("utf-8"))


Network().listen()
