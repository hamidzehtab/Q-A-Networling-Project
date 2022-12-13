import logging
import socket
import sys
import threading
from ast import literal_eval
from random import random
from time import sleep, ctime
from tkinter import *

logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")


# fortest
class Network:
    def __init__(self):

        self.host = "127.0.0.1"
        self.port = 1425
        self.shareData = {"Q": [], "A": []}
        self.Connect()

    def Connect(self):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.sock.connect((self.host, self.port))
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

    def sendData2Server(self, args):

        if "args" not in args.keys():
            args["args"] = {}

        while True:
            try:
                self.sock.send(str(args).encode())
            except:
                self.sock.close()
                self.Connect()
                sleep(1)
                continue
            data = self.listenToServer()
            if data:
                return data
            else:
                sleep(1)
                continue


class Interface(Network):
    def __init__(self, window):

        self.window = window
        self.login = {}
        self.currentPage = Canvas(window)  # just for init
        self.window.attributes("-fullscreen", True)
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        super().__init__()

    def topCanvas(self):

        topCanvas = Canvas(
            self.currentPage,
            highlightbackground="#490C67",
            bg="#6008AE",
            width=self.screen_width - 2,
            height=self.screen_height // 10,
        )
        threading.Thread(target=self.clock, args=(topCanvas,)).start()

        if self.login:
            Button(
                topCanvas,
                text="LogOut",
                width="8",
                font=("bold", "12"),
                height="1",
                bg="#FFC391",
                command=self.LogOut,
            ).place(x=20, y=24)
            Button(
                topCanvas,
                text="Profile",
                width="8",
                font=("bold", "12"),
                height="1",
                bg="#FFC391",
                command=self.profile,
            ).place(x=110, y=24)

        else:
            Button(
                topCanvas,
                text="SignIn/SignUp",
                width="15",
                font=("bold", "12"),
                height="1",
                bg="#FFC391",
                command=self.loginPage,
            ).place(x=20, y=24)

        topCanvas.place(x=0, y=0)

    def checkLogin(self, currentPage):

        if self.login:
            currentPage()

        else:
            self.loginPage()

    def objLambda(
            self,
            obj,
            args,
            mode="default",
            s_if=None,
            s_else=None,
            update_page=None,
            argsUpdate_page=None,
    ):

        if mode == "default":
            return lambda: obj(args)

        elif mode == "condition":
            return (
                lambda: obj(args) and update_page(argsUpdate_page) if s_if else s_else()
            )

        elif mode == "refresh":
            return lambda: obj(args) and update_page()

    def createAcount(self):

        self.currentPage.destroy()

        centerFrame_width = 346
        centerFrame_height = 380

        def waitForCreate(username, password, re_password, canvas):  #

            username = username.get()
            password = password.get()
            re_password = re_password.get()

            if not username or not password or not re_password:
                warningLabel = Label(
                    canvas,
                    text="Fill in all fields",
                    bg="#E2C2F8",
                    highlightbackground="#F64E4E",
                    width=33,
                    height=1,
                    font=("bold", 12),
                )
                warningLabel.place(x=8, y=centerFrame_height - 100)
                threading.Thread(
                    target=lambda: [
                        i() for i in [lambda: sleep(2), warningLabel.destroy]
                    ]
                ).start()
                return

            elif password != re_password:
                warningLabel = Label(
                    canvas,
                    text="Password fields do not match",
                    bg="#E2C2F8",
                    highlightbackground="#F64E4E",
                    width=33,
                    height=1,
                    font=("bold", 12),
                )
                warningLabel.place(x=8, y=centerFrame_height - 100)
                threading.Thread(
                    target=lambda: [
                        i() for i in [lambda: sleep(2), warningLabel.destroy]
                    ]
                ).start()
                return

            elif self.sendData2Server(
                    {"header": "checkUsers", "args": {"username": username}}
            )["resp"]:
                warningLabel = Label(
                    canvas,
                    text="This username already exists",
                    bg="#E2C2F8",
                    highlightbackground="#F64E4E",
                    width=33,
                    height=1,
                    font=("bold", 12),
                )
                warningLabel.place(x=8, y=centerFrame_height - 100)
                threading.Thread(
                    target=lambda: [
                        i() for i in [lambda: sleep(2), warningLabel.destroy]
                    ]
                ).start()
                return

            req = {
                "header": "insertUser",
                "args": {"username": username, "password": password},
            }

            if self.sendData2Server(req)["resp"]:
                self.login = True
                self.mainPage()

            else:
                warningLabel = Label(
                    canvas,
                    text="Happen Problem in Server!",
                    bg="#E2C2F8",
                    highlightbackground="#F64E4E",
                    width=33,
                    height=1,
                    font=("bold", 12),
                )
                warningLabel.place(x=8, y=centerFrame_height - 123)
                threading.Thread(
                    target=lambda: [
                        i() for i in [lambda: sleep(3), lambda: warningLabel.destroy()]
                    ]
                ).start()
                return

        self.currentPage = Canvas(
            self.window,
            bg="#E2C2F8",
            width=self.screen_width - 2,
            height=self.screen_height - 2,
        )
        self.currentPage.place(x=-1, y=-1)

        # =============================================================================================================== {< Top Canvas
        topCanvas = Canvas(
            self.currentPage,
            highlightbackground="#490C67",
            bg="#6008AE",
            width=self.screen_width - 2,
            height=self.screen_height // 10,
        )
        threading.Thread(target=self.clock, args=(topCanvas,)).start()
        topCanvas.place(x=0, y=0)
        # =============================================================================================================== >}

        # =============================================================================================================== {< Center Frame
        centerFrame = Frame(
            self.currentPage, width=centerFrame_width, height=centerFrame_height
        )
        centerCanvas = Canvas(
            centerFrame,
            bg="#D488FA",
            highlightbackground="#490C67",
            width=centerFrame_width - 4,
            height=centerFrame_height - 4,
        )
        centerSmallCanvas = Canvas(
            centerCanvas,
            bg="#374CFF",
            highlightbackground="#490C67",
            width=centerFrame_width - 30,
            height=4 * centerFrame_height // 5,
        )
        centerBottomCanvas = Canvas(
            centerCanvas,
            bg="#374CFF",
            highlightbackground="#490C67",
            width=centerFrame_width - 4,
            height=26,
        )
        centerBottomCanvas.place(x=0, y=centerFrame_height - 32)
        centerSmallCanvas.place(x=13, y=10)
        centerFrame.place(
            x=(self.screen_width - centerFrame_width) // 2,
            y=(self.screen_height - centerFrame_height) // 2,
        )
        centerCanvas.pack(side="left", fill="both", expand=True)

        username = Entry(centerSmallCanvas, width="23", font=("", 17), bg="#BEFCBE")
        Label(
            centerSmallCanvas,
            text="UserName",
            bg="#5F70FF",
            width=33,
            height=1,
            font=("bold", "12"),
        ).place(x=8, y=26)
        password = Entry(centerSmallCanvas, width="23", font=("", 17), bg="#BEFCBE")
        Label(
            centerSmallCanvas,
            text="Password",
            bg="#5F70FF",
            width=33,
            height=1,
            font=("bold", "12"),
        ).place(x=8, y=126)
        password2 = Entry(centerSmallCanvas, width="23", font=("", 17), bg="#BEFCBE")
        Label(
            centerSmallCanvas,
            text="Repeat Password",
            bg="#5F70FF",
            width=33,
            height=1,
            font=("bold", "12"),
        ).place(x=8, y=190)

        username.place(x=8, y=50)
        password.place(x=8, y=150)
        password2.place(x=8, y=214)

        Button(
            centerBottomCanvas,
            text="Create",
            width=19,
            font=("bold", "12"),
            height="1",
            bg="#374CFF",
            command=lambda: waitForCreate(
                username, password, password2, centerSmallCanvas
            ),
        ).place(x=1, y=0)

        Button(
            centerBottomCanvas,
            text="Cancel",
            width=18,
            font=("bold", "12"),
            height="1",
            bg="#374CFF",
            command=lambda: self.loginPage(),
        ).place(x=175, y=0)
        # =============================================================================================================== >}

        # =============================================================================================================== {< Bottom Canvas
        bottomCanvas = Canvas(
            self.currentPage,
            highlightbackground="#490C67",
            bg="#6008AE",
            width=self.screen_width - 2,
            height=self.screen_height // 10,
        )
        bottomCanvas.place(x=-1, y=self.screen_height - self.screen_height // 10)
        # =============================================================================================================== >}

    def loginPage(self):

        self.currentPage.destroy()

        centerFrame_width = 346
        centerFrame_height = 400

        def waitForLogin(username, password, canvas):

            username = username.get()
            password = password.get()

            if not username or not password:
                warningLabel = Label(
                    canvas,
                    text="Fill in all fields",
                    bg="#E2C2F8",
                    highlightbackground="#F64E4E",
                    width=33,
                    height=1,
                    font=("bold", 12),
                )
                warningLabel.place(x=8, y=centerFrame_height - 123)
                threading.Thread(
                    target=lambda: [
                        i() for i in [lambda: sleep(2), warningLabel.destroy]
                    ]
                ).start()
                return

            req = {
                "header": "checkInfoUser",
                "args": {"username": username, "password": password},
            }

            if self.sendData2Server(req)["resp"]:
                self.login = {"username": username, "password": password}
                self.mainPage()

            else:
                warningLabel = Label(
                    canvas,
                    text="Username or Password is incorrect!",
                    bg="#E2C2F8",
                    highlightbackground="#F64E4E",
                    width=33,
                    height=1,
                    font=("bold", 12),
                )
                warningLabel.place(x=8, y=centerFrame_height - 123)
                threading.Thread(
                    target=lambda: [
                        i() for i in [lambda: sleep(2), warningLabel.destroy]
                    ]
                ).start()
                return

        self.currentPage = Canvas(
            self.window,
            bg="#E2C2F8",
            width=self.screen_width - 2,
            height=self.screen_height - 2,
        )
        self.currentPage.place(x=-1, y=-1)

        # =============================================================================================================== {< Top Canvas
        topCanvas = Canvas(
            self.currentPage,
            highlightbackground="#490C67",
            bg="#6008AE",
            width=self.screen_width - 2,
            height=self.screen_height // 10,
        )
        threading.Thread(target=self.clock, args=(topCanvas,)).start()
        topCanvas.place(x=0, y=0)
        # =============================================================================================================== >}

        # =============================================================================================================== {< Cneter Frame
        centerFrame = Frame(
            self.currentPage, width=centerFrame_width, height=centerFrame_height
        )
        centerFrame.place(
            x=(self.screen_width - centerFrame_width) // 2,
            y=(self.screen_height - centerFrame_height) // 2,
        )
        centerCanvas = Canvas(
            centerFrame,
            bg="#D488FA",
            highlightbackground="#490C67",
            width=centerFrame_width - 4,
            height=centerFrame_height - 4,
        )
        centerCanvas.pack(side="left", fill="both", expand=True)

        centerSmallCanvas = Canvas(
            centerCanvas,
            bg="#374CFF",
            highlightbackground="#490C67",
            width=centerFrame_width - 30,
            height=3 * centerFrame_height // 4,
        )
        centerBottomCanvas = Canvas(
            centerCanvas,
            bg="#374CFF",
            highlightbackground="#490C67",
            width=centerFrame_width - 4,
            height=53,
        )
        username = Entry(centerSmallCanvas, width="23", font=("", 17), bg="#BEFCBE")
        Label(
            centerSmallCanvas,
            text="UserName",
            bg="#5F70FF",
            width=33,
            height=1,
            font=("bold", "12"),
        ).place(x=8, y=26)
        password = Entry(
            centerSmallCanvas, width="23", font=("", 17), bg="#BEFCBE", show="*"
        )
        Label(
            centerSmallCanvas,
            text="Password",
            bg="#5F70FF",
            width=33,
            height=1,
            font=("bold", "12"),
        ).place(x=8, y=126)
        username.place(x=8, y=50)
        password.place(x=8, y=150)
        centerSmallCanvas.place(x=13, y=10)
        centerBottomCanvas.place(x=0, y=centerFrame_height - 57)

        Button(
            centerBottomCanvas,
            text="Login",
            width=21,
            font=("bold", "10"),
            height="1",
            bg="#374CFF",
            command=lambda: waitForLogin(username, password, centerSmallCanvas),
        ).place(x=1, y=0)
        Button(
            centerBottomCanvas,
            text="Cancel",
            width=21,
            font=("bold", "10"),
            height="1",
            bg="#374CFF",
            command=lambda: self.mainPage(),
        ).place(x=178, y=0)

        Button(
            centerBottomCanvas,
            text="Create Acount",
            width=42,
            font=("bold", "10"),
            height="1",
            bg="#374CFF",
            command=lambda: self.createAcount(),
        ).place(x=1, y=28)
        # =============================================================================================================== >}

        # =============================================================================================================== {< Bottom Canvas
        bottomCanvas = Canvas(
            self.currentPage,
            highlightbackground="#490C67",
            bg="#6008AE",
            width=self.screen_width - 2,
            height=self.screen_height // 10,
        )
        bottomCanvas.place(x=-1, y=self.screen_height - self.screen_height // 10)
        # =============================================================================================================== >}

    def subQuestionPage(self, args: ["Q_id", "Q_title", "Q_desc"]):

        Q_id, Q_title, Q_desc = args[0], args[1], args[2]

        self.currentPage.destroy()
        self.currentPage = Canvas(
            self.window,
            bg="#E2C2F8",
            width=self.screen_width - 2,
            height=self.screen_height - 2,
        )

        centerFrame_width = 930
        centerFrame_height = 500

        def threadingContainer(frame):  # Container

            A_temp = {}
            cach = {}
            try:
                while True:
                    A_list = self.sendData2Server(
                        {"header": "getAnswers", "args": {"reply_q": Q_id}}
                    )["resp"]
                    Canvas(frame)

                    if A_list and A_list != cach:
                        cach = A_list
                        for Q in A_list:
                            if Q["id"] not in A_temp.keys():  # Create Questions

                                _desc = Q["description"]
                                line = len(_desc) // 120 + _desc.count("\n") + 1

                                _text = ""
                                for i in range(line + 1):
                                    if i + 1 == line:
                                        _text = "{0}\n{1}".format(
                                            _text, _desc[120 * i:]
                                        )

                                    elif i == 0:
                                        _text = _desc[:120]

                                    else:
                                        _text = "{0}\n{1}".format(
                                            _text, _desc[120 * i + 1: 120 * (i + 1)]
                                        )

                                _text = _text.strip()

                                A_temp[Q["id"]] = Canvas(
                                    frame,
                                    bg="#374CFF",
                                    highlightbackground="#490C67",
                                    width=centerFrame_width - 12,
                                    height=18 * line + 40,
                                    borderwidth=4,
                                )
                                Label(
                                    A_temp[Q["id"]],
                                    width=131,
                                    height=line,
                                    text=_text,
                                    bg="#ADD4FB",
                                ).place(x=4, y=5)

                                username = ""
                                if self.login:
                                    username = self.login["username"]

                                Button(
                                    A_temp[Q["id"]],
                                    text="Like {0}".format(Q["like"]),
                                    width="7",
                                    font=("bold", "12"),
                                    height="1",
                                    bg="#56F64E",
                                    command=self.objLambda(
                                        self.sendData2Server,
                                        {
                                            "header": "like",
                                            "args": {
                                                "id": Q["id"],
                                                "username": username,
                                            },
                                        },
                                        mode="condition",
                                        s_if=self.login,
                                        s_else=self.loginPage,
                                        update_page=self.subQuestionPage,
                                        argsUpdate_page=args,
                                    ),
                                ).place(x=4, y=18 * line + 15)

                                Button(
                                    A_temp[Q["id"]],
                                    text="DisLike {0}".format(Q["dislike"]),
                                    width="8",
                                    font=("bold", "12"),
                                    height="1",
                                    bg="#F64E4E",
                                    command=self.objLambda(
                                        self.sendData2Server,
                                        {
                                            "header": "dislike",
                                            "args": {
                                                "id": Q["id"],
                                                "username": username,
                                            },
                                        },
                                        mode="condition",
                                        s_if=self.login,
                                        s_else=self.loginPage,
                                        update_page=self.subQuestionPage,
                                        argsUpdate_page=args,
                                    ),
                                ).place(x=80, y=18 * line + 15)

                                A_temp[Q["id"]].pack()

                        IDtemp_ls = [item["id"] for item in A_list]
                        cp_Q = A_temp.copy()
                        for Q_ID in cp_Q.keys():  # delete Questions
                            if Q_ID not in IDtemp_ls:
                                A_temp[Q_ID].destroy()
                                del A_temp[Q_ID]

                    sleep(2)
            except:
                return

        # =============================================================================================================== {< Top Canvas
        self.topCanvas()
        # =============================================================================================================== >}

        # =============================================================================================================== {< Question Frame
        line = len(Q_desc) // 120
        clean_title = " ".join(Q_title[:30].split("\n"))
        _text = "{0}...  : \n".format(clean_title)

        for i in range(line + 1):
            if i + 1 == line:
                _text = "{0}\n{1}".format(_text, Q_desc[120 * i:])

            else:
                _text = "{0}\n{1}".format(_text, Q_desc[120 * i + 1: 120 * (i + 1)])

        questionFrame = Frame(self.currentPage, width=centerFrame_width, height=117)
        questionCanvas = Canvas(
            questionFrame,
            bg="gray",
            highlightbackground="#490C67",
            width=centerFrame_width - 4,
            height=117,
        )
        scrollbarQ = Scrollbar(
            questionFrame, orient="vertical", command=questionCanvas.yview
        )
        scrollable_Q = Frame(questionCanvas)
        labelQ = Label(scrollable_Q, text=_text, bg="gray", width=131, height=line)
        scrollable_Q.bind(
            "<Configure>",
            lambda e: questionCanvas.configure(scrollregion=questionCanvas.bbox("all")),
        )
        questionCanvas.create_window((0, 0), window=scrollable_Q, anchor="nw")
        questionCanvas.configure(yscrollcommand=scrollbarQ.set)

        labelQ.pack()
        scrollbarQ.pack(side="right", fill="y")
        questionFrame.place(
            x=(self.screen_width - centerFrame_width) // 2,
            y=(self.screen_height - centerFrame_height) // 2 - 50,
        )
        questionCanvas.pack(side="left", fill="both", expand=True)
        # =============================================================================================================== >}

        # =============================================================================================================== {< Center Frame
        centerFrame = Frame(
            self.currentPage, width=centerFrame_width, height=centerFrame_height
        )
        centerCanvas = Canvas(
            centerFrame,
            bg="#D488FA",
            highlightbackground="#490C67",
            width=centerFrame_width - 4,
            height=centerFrame_height - 4,
        )
        scrollbar = Scrollbar(
            centerFrame, orient="vertical", command=centerCanvas.yview
        )
        scrollable_frame = Frame(centerCanvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: centerCanvas.configure(scrollregion=centerCanvas.bbox("all")),
        )
        centerCanvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        centerCanvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        centerFrame.place(
            x=(self.screen_width - centerFrame_width) // 2,
            y=(self.screen_height - centerFrame_height) // 2 + 75,
        )
        centerCanvas.pack(side="left", fill="both", expand=True)
        # =============================================================================================================== >}

        # =============================================================================================================== {< Bottom Answer Canvas
        answerCanvas = Canvas(
            self.currentPage,
            bg="#6008AE",
            highlightbackground="#490C67",
            width=centerFrame_width + 14,
            height=34,
        )

        Button(
            answerCanvas,
            text="Answer",
            width="15",
            font=("bold", "12"),
            height="1",
            bg="#FF9237",
            command=lambda: self.checkLogin(lambda: self.answerFrame(Q_id)),
        ).place(x=centerFrame_width // 2 - 45, y=3)
        Button(
            answerCanvas,
            text="Back",
            width="15",
            font=("bold", "12"),
            height="1",
            bg="#FF9237",
            command=lambda: self.mainPage(),
        ).place(x=4, y=3)

        answerCanvas.place(
            x=(self.screen_width - centerFrame_width) // 2,
            y=(self.screen_height + centerFrame_height) // 2 + 80,
        )
        # =============================================================================================================== >}

        self.currentPage.place(x=-1, y=-1)
        threading.Thread(
            target=threadingContainer, args=(scrollable_frame,)
        ).start()  # Create container for Connection realtime to Server

    def mainPage(self):

        self.currentPage.destroy()
        centerFrame_width = 930
        centerFrame_height = 560

        def threadingContainer(frame):  # Container

            Q_Temp = {}
            cach = {}
            try:
                while True:
                    Q_list = self.sendData2Server({"header": "getQuestions"})["resp"]

                    Canvas(frame)
                    if Q_list and Q_list != cach:
                        cach = Q_list
                        for Q in Q_list:
                            if Q["id"] not in Q_Temp.keys():  # Create Questions

                                Q_Temp[Q["id"]] = Canvas(
                                    frame,
                                    bg="#374CFF",
                                    highlightbackground="#490C67",
                                    width=centerFrame_width - 12,
                                    height=centerFrame_height
                                           / (centerFrame_height / 67),
                                    borderwidth=4,
                                )
                                Button(
                                    Q_Temp[Q["id"]],
                                    text="more",
                                    width="7",
                                    font=("bold", "12"),
                                    height="1",
                                    bg="#FF9237",
                                    command=self.objLambda(
                                        self.subQuestionPage,
                                        (Q["id"], Q["title"], Q["description"]),
                                    ),
                                ).place(x=4, y=43)

                                _text = " ".join(Q["title"].split("\n"))
                                if len(_text) > 240:
                                    _text = "{0}\n{1}...".format(
                                        _text[:120], _text[121:235]
                                    )
                                elif len(_text) > 120:
                                    _text = "{0}\n{1}".format(_text[:120], _text[121:])

                                Label(
                                    Q_Temp[Q["id"]],
                                    text=_text,
                                    bg="#ADD4FB",
                                    width=131,
                                    height=2,
                                ).place(x=4, y=5)
                                Q_Temp[Q["id"]].pack()

                        IDtemp_ls = [item["id"] for item in Q_list]
                        cp_Q = Q_Temp.copy()
                        for Q_ID in cp_Q.keys():  # delete Questions
                            if Q_ID not in IDtemp_ls:
                                Q_Temp[Q_ID].destroy()
                                del Q_Temp[Q_ID]

                    sleep(1)
            except:
                return

        self.currentPage = Canvas(
            self.window,
            bg="#E2C2F8",
            width=self.screen_width - 2,
            height=self.screen_height - 2,
        )

        # =============================================================================================================== {< Top Canvas
        self.topCanvas()
        # =============================================================================================================== >}

        # =============================================================================================================== {< Question Canvas
        questionCanvas = Canvas(
            self.currentPage,
            bg="#6008AE",
            highlightbackground="#490C67",
            width=centerFrame_width + 14,
            height=self.screen_height // 12,
        )
        Button(
            questionCanvas,
            text="Question",
            width="15",
            font=("bold", "12"),
            height="1",
            bg="#FFC391",
            command=lambda: self.checkLogin(self.questionPage),
        ).place(x=centerFrame_width // 2 - 45, y=20)
        # =============================================================================================================== >}

        # =============================================================================================================== {< Center Frame
        centerFrame = Frame(
            self.currentPage, width=centerFrame_width, height=centerFrame_height
        )
        centerCanvas = Canvas(
            centerFrame,
            bg="#D488FA",
            highlightbackground="#490C67",
            width=centerFrame_width - 4,
            height=centerFrame_height - 4,
        )
        scrollbar = Scrollbar(
            centerFrame, orient="vertical", command=centerCanvas.yview
        )
        scrollable_frame = Frame(centerCanvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: centerCanvas.configure(scrollregion=centerCanvas.bbox("all")),
        )
        centerCanvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        centerCanvas.configure(yscrollcommand=scrollbar.set)

        centerFrame.place(
            x=(self.screen_width - centerFrame_width) // 2,
            y=(self.screen_height - centerFrame_height) // 2,
        )
        questionCanvas.place(
            x=(self.screen_width - centerFrame_width) // 2,
            y=(self.screen_height + centerFrame_height) // 2 + 10,
        )
        centerCanvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        # =============================================================================================================== >}

        self.currentPage.place(x=-1, y=-1)
        threading.Thread(
            target=threadingContainer, args=(scrollable_frame,)
        ).start()  # Create container for Connection realtime to Server

    def LogOut(self):

        if self.login:
            self.login = {}
            self.mainPage()

    def questionPage(self):

        self.currentPage.destroy()
        centerFrame_width = 900
        centerFrame_height = 500

        def actionButton(centerCanvas, entrytitle, entryDesc):

            entrytitle = entrytitle.get(1.0, END + "-1c")
            entryDesc = entryDesc.get(1.0, END + "-1c")

            if not entrytitle or not entryDesc:
                warninngCanvas = Label(
                    centerCanvas, text="Fill in all fields ,Please", width=20, height=1
                )
                warninngCanvas.place(x=379, y=centerFrame_height - 24)
                threading.Thread(
                    target=lambda: [
                        i() for i in [lambda: sleep(2), warninngCanvas.destroy]
                    ]
                ).start()
                return

            arg = {
                "header": "insertQuestion",
                "args": {
                    "id": int(random() * 1000000000),
                    "username": self.login["username"],
                    "description": entryDesc,
                    "title": entrytitle,
                },
            }

            warninngCanvas = Canvas(centerCanvas, bg="blue", width=15, height=10)
            warninngCanvas.place(x=centerFrame_width // 2 - 25, y=3)
            if self.sendData2Server(arg)["resp"]:
                warninngCanvas = Label(
                    centerCanvas, text="SuccessFul", width=20, height=1
                )
                warninngCanvas.place(x=379, y=centerFrame_height - 24)
                threading.Thread(
                    target=lambda: [
                        i()
                        for i in [
                            lambda: sleep(2),
                            warninngCanvas.destroy,
                            self.mainPage,
                        ]
                    ]
                ).start()

            else:
                warninngCanvas = Label(
                    centerCanvas, text="Happen Problem in Server!", width=20, height=1
                )
                warninngCanvas.place(x=379, y=centerFrame_height - 24)
                threading.Thread(
                    target=lambda: [
                        i() for i in [lambda: sleep(2), warninngCanvas.destroy]
                    ]
                ).start()
                return

        self.currentPage = Canvas(
            self.window,
            bg="#E2C2F8",
            width=self.screen_width - 2,
            height=self.screen_height - 2,
        )
        self.currentPage.place(x=-1, y=-1)

        # =============================================================================================================== {< Top Canvas
        self.topCanvas()
        # =============================================================================================================== >}

        # =============================================================================================================== {< Center Frame
        centerFrame = Frame(
            self.currentPage, width=centerFrame_width, height=centerFrame_height
        )
        centerCanvas = Canvas(
            centerFrame,
            bg="#D488FA",
            highlightbackground="#490C67",
            width=centerFrame_width - 4,
            height=centerFrame_height - 4,
        )
        entrytitle = Text(
            centerCanvas,
            bg="#BEFCBE",
            height=2,
            width=78,
            padx=10,
            pady=10,
            font=("Arial (Body CS)", "15"),
        )
        entrytitle.place(x=10, y=25)
        entryDesc = Text(
            centerCanvas,
            bg="#BEFCBE",
            height=14,
            width=78,
            padx=10,
            pady=10,
            font=("Arial (Body CS)", "15"),
        )
        entryDesc.place(x=10, y=140)
        Label(centerCanvas, bg="#D488FA", text="Title", width=10, height=1).place(
            x=centerFrame_width // 2 - 25, y=3
        )
        Label(centerCanvas, bg="#D488FA", text="Description", width=15, height=1).place(
            x=centerFrame_width // 2 - 45, y=115
        )
        centerFrame.place(
            x=(self.screen_width - centerFrame_width) // 2,
            y=(self.screen_height - centerFrame_height) // 2,
        )
        centerCanvas.pack(side="left", fill="both", expand=True)
        # =============================================================================================================== >}

        # =============================================================================================================== {< Bottom Canvas
        bottomCanvas = Canvas(
            self.currentPage,
            bg="#6008AE",
            highlightbackground="#490C67",
            width=centerFrame_width - 4,
            height=self.screen_height // 11,
        )

        Button(
            bottomCanvas,
            text="Cancel",
            width="15",
            font=("bold", "12"),
            height="1",
            bg="#FFC391",
            command=lambda: self.mainPage(),
        ).place(x=10, y=10)
        Button(
            bottomCanvas,
            text="Register",
            width="15",
            font=("bold", "12"),
            height="1",
            bg="#FFC391",
            command=lambda: actionButton(centerCanvas, entrytitle, entryDesc),
        ).place(x=centerFrame_width // 2 - 70, y=10)

        bottomCanvas.place(
            x=(self.screen_width - centerFrame_width) // 2,
            y=self.screen_height - self.screen_height // 6,
        )
        # =============================================================================================================== >}

    def answerFrame(self, Q_ID):

        centerFrame_width = 900
        centerFrame_height = 500

        def actionButton(centerCanvas, entryDesc):

            entryDesc = entryDesc.get(1.0, END + "-1c")

            if not entryDesc:
                warninngCanvas = Label(
                    centerCanvas,
                    text="Fill in description fields",
                    bg="#E2C2F8",
                    width=20,
                    height=1,
                )
                warninngCanvas.place(x=centerFrame_width // 2 - 35, y=centerFrame_height - 50)
                threading.Thread(
                    target=lambda: [
                        i()
                        for i in [lambda: sleep(2), lambda: warninngCanvas.destroy()]
                    ]
                ).start()
                return

            arg = {
                "header": "insertAnswer",
                "args": {
                    "id": int(random() * 1000000000),
                    "username": self.login["username"],
                    "description": entryDesc,
                    "reply_q": Q_ID,
                },
            }

            if self.sendData2Server(arg)["resp"]:
                warningLabel = Label(
                    centerCanvas, text="SuccessFul", bg="#E2C2F8", width=20, height=1
                )
                warningLabel.place(
                    x=centerFrame_width // 2 - 35, y=centerFrame_height - 50
                )
                threading.Thread(
                    target=lambda: [
                        i()
                        for i in [lambda: sleep(2), warningLabel.destroy, self.mainPage]
                    ]
                ).start()

            else:
                warningLabel = Label(
                    centerCanvas, text="Happen Problem in Server!", width=20, height=1
                )
                warningLabel.place(
                    x=centerFrame_width // 2 - 35, y=centerFrame_height - 50
                )
                threading.Thread(
                    target=lambda: [
                        i() for i in [lambda: sleep(1), lambda: warningLabel.destroy()]
                    ]
                ).start()

        # =============================================================================================================== {< Center Frame
        centerFrame = Frame(
            self.currentPage,
            highlightbackground="#490C67",
            bg="#D488FA",
            width=centerFrame_width,
            height=centerFrame_height,
        )
        centerCanvas = Canvas(
            centerFrame,
            highlightbackground="#490C67",
            bg="#D488FA",
            width=centerFrame_width + 43,
            height=centerFrame_height + 40,
        )

        centerCanvas2 = Canvas(
            centerCanvas,
            bg="#6008AE",
            highlightbackground="#490C67",
            width=centerFrame_width - 8,
            height=centerFrame_height - 40,
        )
        entryDesc = Text(
            centerCanvas2,
            bg="#BEFCBE",
            height=17,
            width=76,
            padx=10,
            pady=10,
            font=("Arial (Body CS)", "15"),
        )
        entryDesc.place(x=17, y=26)
        Label(centerCanvas2, text="Title", bg="#6008AE", width=10, height=1).place(
            x=centerFrame_width // 2 - 25, y=3
        )
        centerCanvas3 = Canvas(
            centerCanvas,
            bg="#6008AE",
            highlightbackground="#490C67",
            width=centerFrame_width - 8,
            height=35,
        )
        centerCanvas3.place(x=10, y=centerFrame_height - 10)

        Button(
            centerCanvas3,
            text="Send",
            width="15",
            font=("bold", "12"),
            height="1",
            bg="#FFC391",
            command=lambda: actionButton(centerCanvas, entryDesc),
        ).place(x=centerFrame_width // 2 - 45, y=4)

        Button(
            centerCanvas3,
            text="Cancel",
            width="15",
            font=("bold", "12"),
            height="1",
            bg="#FFC391",
            command=lambda: centerFrame.destroy(),
        ).place(x=5, y=4)

        centerFrame.place(
            x=(self.screen_width - centerFrame_width) // 2 - 15,
            y=(self.screen_height - centerFrame_height) // 2 + 75,
        )
        centerCanvas.pack(side="left", fill="both", expand=True)
        centerCanvas2.place(x=10, y=10)
        # =============================================================================================================== >}

    def profile(self):

        centerFrame_width = 900
        centerFrame_height = 500

        self.currentPage.destroy()
        self.currentPage = Canvas(
            self.window,
            bg="#E2C2F8",
            width=self.screen_width - 2,
            height=self.screen_height - 2,
        )

        # =============================================================================================================== {< Top Canvas
        topCanvas = Canvas(
            self.currentPage,
            highlightbackground="#490C67",
            bg="#6008AE",
            width=self.screen_width - 2,
            height=self.screen_height // 10,
        )
        threading.Thread(target=self.clock, args=(topCanvas,)).start()
        Button(
            topCanvas,
            text="LogOut",
            width="6",
            font=("bold", "12"),
            height="1",
            bg="#FFC391",
            command=lambda: self.LogOut(),
        ).place(x=20, y=24)
        Button(
            topCanvas,
            text="Main Page",
            width="9",
            font=("bold", "12"),
            height="1",
            bg="#FFC391",
            command=lambda: self.mainPage(),
        ).place(x=110, y=24)
        topCanvas.place(x=0, y=0)
        # =============================================================================================================== >}

        # =============================================================================================================== {< Botton Canvas
        bottomCanvas = Canvas(
            self.currentPage,
            highlightbackground="#490C67",
            bg="#6008AE",
            width=self.screen_width - 2,
            height=self.screen_height // 11,
        )
        bottomCanvas.place(x=0, y=self.screen_height - self.screen_height // 11 - 2)
        # =============================================================================================================== >}

        # =============================================================================================================== {< Left Canvas
        leftCanvas = Canvas(
            self.currentPage,
            highlightbackground="#490C67",
            bg="#6008AE",
            width=self.screen_width // 2 - 40,
            height=centerFrame_height - 4,
        )
        centerLeftFrame = Frame(
            leftCanvas,
            width=self.screen_width // 2 - 70,
            height=centerFrame_height - 60,
        )
        Label(
            leftCanvas,
            text="Questions",
            bg="#42F16D",
            width=69,
            height=1,
            font=("bold", 12),
        ).place(x=15, y=14)

        centerLeftCanvas = Canvas(
            centerLeftFrame,
            bg="#D488FA",
            highlightbackground="#490C67",
            width=self.screen_width // 2 - 70,
            height=centerFrame_height - 60,
        )
        leftScrollbar = Scrollbar(
            centerLeftFrame, orient="vertical", command=centerLeftCanvas.yview
        )

        leftScrollable_frame = Frame(centerLeftCanvas)
        leftScrollable_frame.bind(
            "<Configure>",
            lambda e: centerLeftCanvas.configure(
                scrollregion=centerLeftCanvas.bbox("all")
            ),
        )
        centerLeftCanvas.create_window((0, 0), window=leftScrollable_frame, anchor="nw")
        centerLeftCanvas.configure(yscrollcommand=leftScrollbar.set)

        leftScrollbar.pack(side="right", fill="y")
        leftCanvas.place(x=20, y=150)
        centerLeftFrame.place(x=15, y=40)
        centerLeftCanvas.pack(side="left", fill="both", expand=True)
        # ==-
        resp = self.sendData2Server(
            {"header": "getQuestions", "args": {"username": self.login["username"]}}
        )["resp"]

        for Q in resp:

            _desc = Q["description"]
            line = len(_desc) // 120 + _desc.count("\n") + 1

            _Q_description = ""
            for i in range(line + 1):
                if i + 1 == line:
                    _Q_description = "{0}\n{1}".format(
                        _Q_description, _desc[120 * i + 1:]
                    )

                elif i == 0:
                    _Q_description = _desc[:120]

                else:
                    _Q_description = "{0}\n{1}".format(
                        _Q_description, _desc[120 * i + 1: 120 * (i + 1)]
                    )

            _Q_description = _Q_description.strip()

            itemCanvas = Canvas(
                leftScrollable_frame,
                bg="#374CFF",
                highlightbackground="#490C67",
                width=centerFrame_width - 12,
                height=18 * line + 30,
                borderwidth=4,
            )
            Label(
                itemCanvas, width=88, height=line, text=_Q_description, bg="#ADD4FB"
            ).place(x=1, y=1)
            Button(
                itemCanvas,
                text="Delete",
                width="6",
                font=("bold", "12"),
                height="1",
                bg="#FF9237",
                command=self.objLambda(
                    self.sendData2Server,
                    {"header": "deleteQuestion", "args": {"id": Q["id"]}},
                    mode="refresh",
                    update_page=self.profile,
                ),
            ).place(x=4, y=18 * line + 5)
            itemCanvas.pack()
        # =============================================================================================================== >}

        # =============================================================================================================== {<Right Canvas
        rightCanvas = Canvas(
            self.currentPage,
            highlightbackground="#490C67",
            bg="#6008AE",
            width=self.screen_width // 2 - 40,
            height=centerFrame_height - 4,
        )
        centerRightFrame = Frame(
            rightCanvas,
            width=self.screen_width // 2 - 70,
            height=centerFrame_height - 60,
        )
        Label(
            rightCanvas,
            text="Answers",
            bg="#42F16D",
            width=69,
            height=1,
            font=("bold", 12),
        ).place(x=15, y=14)

        centerRightCanvas = Canvas(
            centerRightFrame,
            bg="#D488FA",
            highlightbackground="#490C67",
            width=self.screen_width // 2 - 70,
            height=centerFrame_height - 60,
        )
        rightScrollbar = Scrollbar(
            centerRightFrame, orient="vertical", command=centerRightCanvas.yview
        )

        rightScrollable_frame = Frame(centerRightCanvas)
        rightScrollable_frame.bind(
            "<Configure>",
            lambda e: centerRightCanvas.configure(
                scrollregion=centerRightCanvas.bbox("all")
            ),
        )
        centerRightCanvas.create_window(
            (0, 0), window=rightScrollable_frame, anchor="nw"
        )
        centerRightCanvas.configure(yscrollcommand=rightScrollbar.set)

        rightScrollbar.pack(side="right", fill="y")
        rightCanvas.place(x=self.screen_width // 2 + 20, y=150)
        centerRightFrame.place(x=15, y=40)
        centerRightCanvas.pack(side="left", fill="both", expand=True)

        resp = self.sendData2Server(
            {"header": "getAnswers", "args": {"username": self.login["username"]}}
        )["resp"]

        for A in resp:

            _desc = A["description"]
            A_resp = self.sendData2Server(
                {"header": "getQuestions", "args": {"id": A["reply_q"]}}
            )["resp"]
            _title = "Deleted Question!"
            if A_resp:
                title = " ".join(A_resp[0]["title"].strip().split("\n"))
                _title = title if len(title) < 50 else title[:50] + "..."

            line = len(_desc) // 120 + _desc.count("\n") + 2
            _text = ""
            for i in range(line + 1):
                if i + 1 == line:
                    _text = "{0}\n{1}".format(_text, _desc[120 * i + 1:])

                elif i == 0:
                    _text = "Title : {0}\nAnswer : {1}".format(_title, _desc[:120])

                else:
                    _text = "{0}\n{1}".format(_text, _desc[120 * i + 1: 120 * (i + 1)])

            _text = _text.strip()

            itemCanvas = Canvas(
                rightScrollable_frame,
                bg="#374CFF",
                highlightbackground="#490C67",
                width=centerFrame_width - 12,
                height=20 * line + 30,
                borderwidth=4,
            )
            Label(itemCanvas, width=88, height=line, text=_text, bg="#ADD4FB").place(
                x=1, y=1
            )

            Button(
                itemCanvas,
                text="Delete",
                width="6",
                font=("bold", "12"),
                height="1",
                bg="#FF9237",
                command=self.objLambda(
                    self.sendData2Server,
                    {"header": "deleteAnswer", "args": {"id": A["id"]}},
                    mode="refresh",
                    update_page=self.profile,
                ),
            ).place(x=4, y=18 * line + 10)
            itemCanvas.pack()
        # =============================================================================================================== >}

        self.currentPage.place(x=-1, y=-1)

    def clock(self, frame):

        while True:
            try:
                roz = {
                    "Fri": "جمعه",
                    "Sat": "شنبه",
                    "Sun": "یک شنبه",
                    "Mon": "دو شنبه",
                    "Tue": "سه شنبه",
                    "Wed": "چهارشنبه",
                    "Thu": "پنج شنبه",
                }
                mah = {
                    "Jan": "01",
                    "Feb": "02",
                    "Mar": "03",
                    "Apr": "04",
                    "May": "05",
                    "Jun": "06",
                    "Jul": "07",
                    "Aug": "08",
                    "Sep": "09",
                    "Oct": "10",
                    "Nov": "11",
                    "Dec": "12",
                }
                time_date = ctime().split(" ")
                date = (
                        time_date[5]
                        + "/"
                        + str(mah[time_date[1]])
                        + "/"
                        + time_date[3]
                        + "\n"
                        + roz[time_date[0]]
                )

                clock = Label(
                    frame,
                    font=("bold", 14),
                    fg="lightblue",
                    text=time_date[4],
                    bg="#6008AE",
                )
                date = Label(
                    frame, font=("bold", 13), fg="lightblue", text=date, bg="#6008AE"
                )

                clock.place(x=self.screen_width // 2 - 33, y=10)
                date.place(x=self.screen_width - 100, y=20)
                sleep(1)
            except:
                return


window = Tk()
Interface(window).mainPage()
window.mainloop()
