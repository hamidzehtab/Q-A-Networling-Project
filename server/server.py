import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
# Run tkinter code in another thread
import json
import tkinter as tk
from tkinter import messagebox
import threading
import sys


def buildInfo(msgKey, msgValue):
    msg = {
        "type": "info",
        msgKey: msgValue
    }
    return json.dumps(msg)


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    if msg is not None and type(msg) is str:
        msg = bytes(msg, "utf8")
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


def on_closing():
    global clients
    global addresses
    global HOST_CLOSED
    for sock in clients:
        sock.send(bytes("{quit}", "utf8"))
        sock.close()
    SERVER.close()
    HOST_CLOSED = True
    clients = {}
    addresses = {}
    sys.exit(0)


class QuizMaster(threading.Thread):
    HOST = None
    PORT = None
    question = None
    client_list = dict()
    clients_string = None

    def __init__(self, HOST=None, PORT=None):
        self.correct_option = None
        self.HOST = HOST
        self.PORT = PORT
        threading.Thread.__init__(self)
        self.start()
        self.start_timer = None
        self.end_timer = None
        self.num_of_answered = 0

    def callback(self):
        self.root.destroy()
        print("Inside callback.")
        on_closing()
        sys.exit(0)

    def addClientToList(self, client, client_name):
        self.client_list[client] = client_name
        self.buildClientList()

    def removeClientFromList(self, client):
        self.client_list.pop(client, None)
        self.buildClientList()

    def buildClientList(self):
        clients = ""
        for client, client_name in self.client_list.items():
            clients = clients + str(client_name) + ", "
        self.clients_string.set(clients)

    def checkAnswer(self, answer, name):
        print(type(answer), "answer", answer)
        print(type(self.correct_option), "correct_option", self.correct_option)
        if str(answer) == str(self.correct_option):
            scoreboard[name] += 1
            return True
        else:
            return False

    @staticmethod
    def send_scoreboard():
        msg = {'type': 'scoreboard', 'scoreboard': str(scoreboard)}
        broadcast(msg=json.dumps(msg))

    @staticmethod
    def time_finished():
        msg = {'type': 'info', 'timeout': True}
        broadcast(msg=json.dumps(msg))
        print("yo")

    def sendQuestion(self):

        if len(clients) >= 3:
            q = questions.pop()
            self.correct_option = q['answer']
            msg = {"type": "question", "question": q['question'], 'choices': list()}
            msg['choices'].append({
                "text": q['options'][0],
                # "value": "True" if self.correct_option == 1 else "False"
            })
            msg['choices'].append({
                "text": q['options'][1],
                # "value": "True" if self.correct_option == 2 else "False"
            })
            msg['choices'].append({
                "text": q['options'][2],
                # "value": "True" if self.correct_option == 3 else "False"
            })
            if len(q['options']) == 4:
                msg['choices'].append({
                    "text": q['options'][3],
                    # "value": "True" if self.correct_option == 4 else "False"
                })
            else:
                msg['choices'].append({
                    "text": "this a three choice question",
                    # "value": "True" if self.correct_option == 4 else "False"
                })
            broadcast(msg=json.dumps(msg))
        else:
            print('not enough participants')

    def run(self):
        self.root = tk.Tk()
        self.clients_string = tk.StringVar()
        self.root.title("CN Project")
        l1 = tk.Label(self.root, text="CN Quiz Project", font=("Arial Bold", 25))
        l1.grid(column=0, row=0)
        l2 = tk.Label(self.root,
                      text="Welcome to our CN quiz project, master!\nThere is a list of question, its options, "
                           "and only one"
                           "can be correct.\nThen watch your friends try answering them.See who gets most of them "
                           "Right \n"
                            "Developed By Hamid.R Zehtab and Ali.M Tabatabaei"
                           " \n",
                      anchor="w")
        l2.grid(column=0, row=1, sticky=tk.W)
        clients_info = tk.Label(self.root, text="Active Players:")
        clients_info.grid(column=1, row=1)
        clients_display = tk.Label(self.root, textvariable=self.clients_string)
        clients_display.grid(column=2, row=1)
        l3 = tk.Label(self.root, text="HOST: " + str(self.HOST))
        l3.grid(column=0, row=2, sticky=tk.W)
        l4 = tk.Label(self.root, text="PORT: " + str(self.PORT))
        l4.grid(column=0, row=3, sticky=tk.W)

        submit_question = tk.Button(self.root, text='Send Question', command=self.sendQuestion)
        submit_question.grid(column=1, row=6, columnspan=3, sticky=tk.W)
        print("Hi here.")
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.mainloop()


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes(buildInfo("greeting", "Greetings player! Now type your name and press enter!"), "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(buildInfo("welcomeMsg", welcome), "utf8"))
    msg = "%s has joined the chat!" % name
    quizMaster.addClientToList(client, name)
    broadcast(bytes(buildInfo("joined", msg), "utf8"))
    clients[client] = name
    scoreboard[name] = 0

    while True:
        msg = client.recv(BUFSIZ).decode("utf8")
        print(msg)
        if msg != "{quit}":
            try:
                msg = json.loads(msg)
                if msg['type'] == "answer":
                    client.send(bytes(buildInfo("answer", str(quizMaster.checkAnswer(msg["answer"], name))), "utf8"))
                    QuizMaster.send_scoreboard()
                if msg['type'] == 'message':
                    message = dict()
                    message['type'] = 'message'
                    message['content'] = msg['content']
                    print(message['content'])
                    broadcast(msg=json.dumps(message))
            except Exception as e:
                print("Incorrect Payload:", msg)
                on_closing()
                break
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            quizMaster.removeClientFromList(client)
            del clients[client]
            break


clients = {}
addresses = {}


def read_questions():
    f = open("../questions.json",encoding="utf8")
    data_json = json.load(f)
    for question in data_json:
        questions.append(question)
    print(questions)


import socket

f = open('../users.json', 'r')
data = json.load(f)
for i in data:
    if i['type'] == "host":
        port = i['port']
listClients = []
BUFSIZ = 1024
host = "127.0.0.1"
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SERVER.bind((host, port))
# SERVER.bind(f'tcp://127.0.0.1:{port}')
questions = []
current_question = 0
read_questions()
scoreboard = {}
start = 0
if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    quizMaster = QuizMaster(HOST='127.0.0.1', PORT=port)
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
