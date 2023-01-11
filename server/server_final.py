from random import choice, random
import socket, threading, time
from ast import literal_eval
from tkinter import *
import logging
import sqlite3
import sys
import os
import json
import time
import zmq


class Network:
    def __init__(self):

        f = open('../users.json', 'r')
        data = json.load(f)
        for i in data:
            if i['type'] == "host":
                self.port = i['port']
        self.listClients = []
        self.host = "127.0.0.1"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.bind(f'tcp://127.0.0.1:{self.port}')
        self.questions = []
        self.current_question = 0
        self.read_questions()
        self.scoreboard = {'user-1': 0, 'user-2': 0, 'user-3': 0}
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
            "answer": lambda: self.get_answers(name, args),
            "insertAnswer": lambda: self.insertAnswer(receive_data["args"]),
            "getQuestions": lambda: self.getQuestions(receive_data["args"]),
            "deleteAnswer": lambda: self.deleteAnswer(receive_data["args"]),
            "insertUser": lambda: self.insertUser(receive_data["args"]),
            "checkUsers": lambda: self.checkUsers(receive_data["args"]),
            "getAnswers": lambda: self.getAnswers(receive_data["args"]),
        }

        while True:
            # try:
            receive_data = client.recv(1024).decode()
            print("receive data : %s | From : %s", receive_data, address)
            name, method, args = receive_data.split(':')
            print(name, method, args)
            if method in dic_fn.keys():
                resp = dic_fn[method]()
                if resp:
                    client.send(str(resp).encode())
            else:
                client.send("error".encode())

        # except:
        #   logging.warning("client missing!! : [%s]", sys.exc_info())
        #  client.close()
        # return

    def initiate_client(self, name, args):
        num_ready_clients = 3 - len(self.listClients)
        if num_ready_clients == 0:
            # self.send_questions()
            for client in self.listClients:
                client.send('gameStarted'.encode())
            for i in range(4):
                for client in self.listClients:
                    client.settimeout(1)
                    client.send('question'.encode())
                    time.sleep(0.5)
                    client.send(f'{(self.questions[self.current_question]["question"])},'
                                f'{(self.questions[self.current_question]["options"][0])},{(self.questions[self.current_question]["options"][1])},'
                                f'{(self.questions[self.current_question]["options"][2])},{(self.questions[self.current_question]["options"][3])},'
                                f'{(self.questions[self.current_question]["answer"])}'.encode())
                for client in self.listClients:
                    client.send('scoreboard\n'.encode())
                    time.sleep(0.5)
                    client.send(str(self.scoreboard).encode())
                self.current_question += 1
        else:
            return f'{num_ready_clients} clients remaining'

    # def send_questions(self, name, args): return self.questions[self.current_question]"""

    def read_questions(self):
        f = open("../questions.json")
        data_json = json.load(f)
        for data in data_json:
            self.questions.append(data)
        print(self.questions)

    def get_answers(self, name, args):
        if args and (name in self.scoreboard):
            self.scoreboard[name] += 1


Network().listen()
