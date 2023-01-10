#!/usr/bin/env python3
"""Script for Tkinter GUI quiz client."""
import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import json
from tkinter import messagebox

global start


def takeAction(msg):
    message = json.loads(msg)
    if message['type'] == "info" and "welcomeMsg" in message:
        print("Got welcome message.")
        infoMessage.set("Please wait for the Quiz Master to start.")
        player_name.grid_forget()
        submit_name.grid_forget()

    if message['type'] == "info" and "answer" in message:
        print("Got response for answer:", message['answer'], message['answer'] == "True")
        if message['answer'] == "True":
            messagebox.showinfo("Yay", "You got the correct answer!")
        else:
            messagebox.showerror("Oops!", "You got the wrong answer!")
        infoMessage.set("Please wait for the Quiz Master to start the next round.")

    elif message['type'] == "question":
        infoMessage.set("Select the answer below and click the button.")
        quesLabel.grid(column=0, row=2)
        c1.grid(column=0, row=3)
        c2.grid(column=0, row=4)
        c3.grid(column=0, row=5)
        c4.grid(column=0, row=6)
        submit_button.grid(column=0, row=7)
        question.set(message['question'])
        choice1.set(message['choices'][0]['text'])
        choice2.set(message['choices'][1]['text'])
        choice3.set(message['choices'][2]['text'])
        choice4.set(message['choices'][3]['text'])
        c1.config(state='normal')
        c2.config(state='normal')
        c3.config(state='normal')
        c4.config(state='normal')
        submit_button.config(state='normal')
    elif message['type'] == "scoreboard":
        infoMessage.set(message['scoreboard'])


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            if msg == "{quit}":
                client_socket.close()
                top.quit()
            else:
                takeAction(msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = quit.get()
    quit.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    quit.set("{quit}")
    send()


def sendName():
    client_socket.send(bytes(name, "utf8"))


def sendAnswer(start=None):
    c1.config(state='disabled')
    c2.config(state='disabled')
    c3.config(state='disabled')
    c4.config(state='disabled')
    submit_button.config(state='disabled')
    message = dict()
    message['type'] = "answer"
    message['answer'] = str(correct_option.get())
    client_socket.send(bytes(json.dumps(message), "utf8"))


is_bound = False
f = open('../users.json', 'r+')
data = json.load(f)
f.close()
count = 0
f = open('../users.json', 'w')
for user in data:
    if user['type'] == "host":
        PORT = user['port']
    if not is_bound and user['type'] == 'client' and user['isUsed'] == 0:
        is_bound = True
        client_port = user['port']
        name = user['name']
        user['isUsed'] = 1
        data[count].update(user)
        json.dump(data, f)
    count += 1

top = tkinter.Tk()
top.title("Player - P2P Quiz Application")
l1 = tkinter.Label(top, text="Quiz Master", font=("Arial Bold", 25))
l1.grid(column=0, row=0)
player_name = tkinter.Label(top)
infoMessage = tkinter.StringVar()
infoMessage.set("Enter your name below to get started.")
infoLabel = tkinter.Label(top, textvariable=infoMessage)
infoLabel.grid(column=0, row=1)
quit = tkinter.StringVar()
question = tkinter.StringVar()
choice1 = tkinter.StringVar()
choice2 = tkinter.StringVar()
choice3 = tkinter.StringVar()
choice4 = tkinter.StringVar()
correct_option = tkinter.IntVar()
quesLabel = tkinter.Label(top, textvariable=question)
player_name.grid(column=0, row=2, columnspan=3, sticky=tkinter.W)
submit_name = tkinter.Button(top, text='Submit Name', command=sendName)
submit_name.grid(column=1, row=2, columnspan=3, sticky=tkinter.W)
c1 = tkinter.Radiobutton(top, textvariable=choice1, variable=correct_option, value=1)
c2 = tkinter.Radiobutton(top, textvariable=choice2, variable=correct_option, value=2)
c3 = tkinter.Radiobutton(top, textvariable=choice3, variable=correct_option, value=3)
c4 = tkinter.Radiobutton(top, textvariable=choice4, variable=correct_option, value=4)
submit_button = tkinter.Button(top, text='Submit Answer', command=sendAnswer)
top.protocol("WM_DELETE_WINDOW", on_closing)

# ----Now comes the sockets part----


HOST = "127.0.0.1"
f.close()
BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.bind(('127.0.0.1', client_port))
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()

# client_socket.send(bytes("I'm here!", "utf8"))
