from random import choice, random
import socket, threading, time
from ast import literal_eval
from tkinter import *
import logging
import sqlite3
import sys
import os


logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")

directory = os.getcwd() + "/database/dataBase.db"

# objDataBase = None


class DataBase:
    def __init__(self):

        with sqlite3.connect(directory) as con:
            cur = con.cursor()
            cur.execute(
                "CREATE TABLE IF NOT EXISTS users (username TEXT ,password TEXT)"
            )
            cur.execute(
                "CREATE TABLE IF NOT EXISTS questions (id TEXT ,username ,description TEXT ,title TEXT )"
            )
            cur.execute(
                "CREATE TABLE IF NOT EXISTS answers (id TEXT ,username TEXT ,description TEXT ,reply_q TEXT )"
            )
            cur.execute("CREATE TABLE IF NOT EXISTS likes (id_a TEXT ,username TEXT)")
            cur.execute(
                "CREATE TABLE IF NOT EXISTS dislikes (id_a TEXT ,username TEXT)"
            )
            con.commit()

    def getQuestions(self, args: ["id-default", "username-default"]) -> list:

        logging.warning("---getQuestions----")

        with sqlite3.connect(directory) as con:
            cur = con.cursor()

            if "id" in args.keys():
                cur.execute(
                    'SELECT id,description,title FROM questions WHERE id="{0}"'.format(
                        args["id"]
                    )
                )
            elif "username" in args.keys():
                cur.execute(
                    'SELECT id,description,title FROM questions WHERE username="{0}"'.format(
                        args["username"]
                    )
                )
            else:
                cur.execute("SELECT id,description,title FROM questions")

            data = cur.fetchall()

            return [{"id": i[0], "description": i[1], "title": i[2]} for i in data]

    def deleteQuestion(self, args: ["id"]) -> bool:

        logging.warning("---deleteQuestion----")

        id = args["id"]

        with sqlite3.connect(directory) as con:

            cur = con.cursor()
            cur.execute('DELETE FROM questions WHERE id="{0}"'.format(id))
            con.commit()

            return True

    def deleteAnswer(self, args: ["id"]) -> bool:

        logging.warning("---deleteAnswer----")

        id = args["id"]
        with sqlite3.connect(directory) as con:

            cur = con.cursor()
            cur.execute('DELETE FROM answers WHERE id="{0}"'.format(id))
            con.commit()

            return True

    def getAnswers(self, args: ["reply_q-default", "username-default"]) -> list:

        logging.warning("---getAnswers----")

        with sqlite3.connect(directory) as con:
            cur = con.cursor()

            if "username" in args.keys():
                cur.execute(
                    'SELECT id,description,reply_q FROM answers WHERE username="{0}"'.format(
                        args["username"]
                    )
                )
            else:
                cur.execute(
                    'SELECT id,description,reply_q FROM answers WHERE reply_q="{0}"'.format(
                        args["reply_q"]
                    )
                )

            data = cur.fetchall()

            dataSort = []
            for item in [
                {"id": i[0], "description": i[1], "reply_q": i[2]} for i in data
            ]:
                dataSort.append(
                    {
                        **item,
                        "like": self.like(item["id"], mode="count"),
                        "dislike": self.dislike(item["id"], mode="count"),
                    }
                )

            return dataSort

    def checkUsers(self, args: ["username"]) -> bool:

        logging.warning("---checkUsers----")

        username = args["username"]

        with sqlite3.connect(directory) as con:

            cur = con.cursor()
            cur.execute(
                'SELECT username FROM users WHERE username="{0}"'.format(username)
            )
            data = cur.fetchall()
            if data and username == data[0][0]:
                return True

            else:
                return False

    def checkInfoUser(self, args: ["username", "password"]) -> bool:

        logging.warning("---checkInfoUser----")

        username = args["username"]
        password = args["password"]

        with sqlite3.connect(directory) as con:
            cur = con.cursor()
            cur.execute(
                'SELECT username,password FROM users WHERE username="{0}"'.format(
                    username
                )
            )
            data = cur.fetchall()
            if data and username == data[0][0] and password == data[0][1]:
                return True

            else:
                return False

    def insertUser(self, args: ["username", "password"]) -> bool:

        logging.warning("---insertUser----")

        username = args["username"]
        password = args["password"]

        with sqlite3.connect(directory) as con:
            cur = con.cursor()
            cur.execute("insert into users VALUES (?,?)", (username, password))
            con.commit()
            return True

    def insertQuestion(self, args: ["id", "username", "description", "title"]) -> bool:

        logging.warning("---insertQuestion----")

        id, username, description, title = (
            args["id"],
            args["username"],
            args["description"],
            args["title"],
        )

        with sqlite3.connect(directory) as con:
            cur = con.cursor()
            cur.execute(
                "insert into questions VALUES (?,?,?,?)",
                (id, username, description, title),
            )
            con.commit()
        return True

    def insertAnswer(self, args: ["id", "username", "description", "reply_q"]) -> bool:

        logging.warning("---insertAnswer----")

        id, username, description, reply_q = (
            args["id"],
            args["username"],
            args["description"],
            args["reply_q"],
        )
        with sqlite3.connect(directory) as con:
            cur = con.cursor()
            cur.execute(
                "insert into answers VALUES (?,?,?,?)",
                (id, username, description, reply_q),
            )
            con.commit()
        return True

    def like(self, id_a, mode, username=None) -> bool and str:

        logging.warning("---like----")

        with sqlite3.connect(directory) as con:
            cur = con.cursor()

            if mode == "ckeck":
                cur.execute('SELECT username FROM likes WHERE id_a="{0}"'.format(id_a))
                data = cur.fetchall()
                if data:
                    return True
                else:
                    return False

            elif mode == "handle":
                cur.execute(
                    'SELECT * FROM likes WHERE id_a="{0}" AND username="{1}"'.format(
                        id_a, username
                    )
                )
                data = cur.fetchall()
                if data:
                    cur.execute(
                        'DELETE FROM likes WHERE id_a="{0}" AND username="{1}"'.format(
                            id_a, username
                        )
                    )
                    con.commit()

                else:
                    if self.dislike(id_a, mode="ckeck"):
                        self.dislike(id_a, mode="handle", username=username)
                    cur.execute("insert into likes VALUES (?,?)", (id_a, username))
                    con.commit()
                return True

            elif mode == "count":
                cur.execute("SELECT COUNT(*) FROM likes WHERE id_a = {0}".format(id_a))
                data = cur.fetchall()
                return data[0][0]

    def dislike(self, id_a, mode, username=None) -> bool and str:

        logging.warning("---dislike----")

        with sqlite3.connect(directory) as con:
            cur = con.cursor()

            if mode == "ckeck":
                cur.execute(
                    'SELECT username FROM dislikes WHERE id_a="{0}"'.format(id_a)
                )
                data = cur.fetchall()
                if data:
                    return True
                else:
                    return False

            elif mode == "handle":
                cur.execute(
                    'SELECT * FROM dislikes WHERE id_a="{0}" AND username="{1}"'.format(
                        id_a, username
                    )
                )
                data = cur.fetchall()
                if data:
                    cur.execute(
                        'DELETE FROM dislikes WHERE id_a="{0}" AND username="{1}"'.format(
                            id_a, username
                        )
                    )
                    con.commit()

                else:
                    if self.like(id_a, mode="ckeck"):
                        self.like(id_a, mode="handle", username=username)
                    cur.execute("insert into dislikes VALUES (?,?)", (id_a, username))
                    con.commit()
                return True

            elif mode == "count":
                cur.execute(
                    "SELECT COUNT(*) FROM dislikes WHERE id_a = {0}".format(id_a)
                )
                data = cur.fetchall()
                return data[0][0]


class Network(DataBase):
    def __init__(self):

        super().__init__()
        self.listClients = []
        self.host = "127.0.0.1"
        self.port = 1425
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

        dic_fn = {
            "dislike": lambda: self.dislike(
                recive_data["args"]["id"],
                mode="handle",
                username=recive_data["args"]["username"],
            ),
            "like": lambda: self.like(
                recive_data["args"]["id"],
                mode="handle",
                username=recive_data["args"]["username"],
            ),
            "deleteQuestion": lambda: self.deleteQuestion(recive_data["args"]),
            "insertQuestion": lambda: self.insertQuestion(recive_data["args"]),
            "checkInfoUser": lambda: self.checkInfoUser(recive_data["args"]),
            "insertAnswer": lambda: self.insertAnswer(recive_data["args"]),
            "getQuestions": lambda: self.getQuestions(recive_data["args"]),
            "deleteAnswer": lambda: self.deleteAnswer(recive_data["args"]),
            "insertUser": lambda: self.insertUser(recive_data["args"]),
            "checkUsers": lambda: self.checkUsers(recive_data["args"]),
            "getAnswers": lambda: self.getAnswers(recive_data["args"]),
        }

        while True:
            try:

                recive_data = client.recv(1024).decode()
                logging.warning("receive data : %s | From : %s", recive_data, address)
                recive_data = literal_eval(recive_data)

                if recive_data["header"] in dic_fn.keys():
                    resp = dic_fn[recive_data["header"]]()
                    client.send(str({"resp": resp}).encode())

                else:
                    client.send(str({"resp": []}).encode())

            except:

                logging.warning("client missing!! : [%s]", sys.exc_info())
                client.close()
                return


Network().listen()
