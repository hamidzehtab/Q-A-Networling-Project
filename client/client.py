import threading
import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter import ttk, font
from tkinter import *
import json
from tkinter import messagebox

start = 0


def takeAction(msg):
    message = json.loads(msg)
    if message['type'] == "info" and "welcomeMsg" in message:
        print("Got welcome message.")
        infoMessage.set("Please wait for the mathc to start.")
        player_name.grid_forget()
        submit_name.grid_forget()

    if message['type'] == "info" and "answer" in message:
        print("Got response for answer:", message['answer'], message['answer'] == "True")
        if message['answer'] == "True":
            messagebox.showinfo("Yay", "You got the correct answer!")
        else:
            messagebox.showerror("Oops!", "You got the wrong answer!")
        infoMessage.set("Please wait for the Quiz mathc to start the next round.")

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
        false = [False]
        global start_timer
        start_timer = threading.Timer(15, sendAnswer, false)
        start_timer.start()
    elif message['type'] == "scoreboard":
        infoMessage.set(message['scoreboard'])
    elif message['type'] == 'info' and 'timeout' in message:
        infoMessage.set("Please wait for the match to start the next round.")
        message = dict()
        message['type'] = "answer"
        message['answer'] = '5'
        client_socket.send(bytes(json.dumps(message), "utf8"))
    elif message['type'] == 'message':
        textCons.config(state=NORMAL)
        textCons.insert(END,message['content'] + "\n\n")
        textCons.config(state=DISABLED)
        textCons.see(END)


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


def send():  # event is passed by binders.
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


def sendAnswer(time=None):
    if time is None:
        time = True
    global start_timer
    start_timer.cancel()
    c1.config(state='disabled')
    c2.config(state='disabled')
    c3.config(state='disabled')
    c4.config(state='disabled')
    submit_button.config(state='disabled')
    message = dict()
    message['type'] = "answer"
    if time:
        message['answer'] = str(correct_option.get())
    else:
        message['answer'] = '5'
    client_socket.send(bytes(json.dumps(message), "utf8"))


def sendButton(msg):
    textCons.config(state=DISABLED)
    entryMsg.delete(0, END)
    snd = threading.Thread(target=sendMessage, args=[msg])
    snd.start()


def sendMessage(msg):
    textCons.config(state=DISABLED)
    message = dict()
    message['type'] = "message"
    message['content'] = f'{name}: {msg}'
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
top.title("Player Portal")
notebook = ttk.Notebook(top)
notebook.pack(pady=10, expand=True)
frame1 = ttk.Frame(notebook)
frame1.pack(fill='both', expand=True)
frame2 = ttk.Frame(notebook)
frame2.pack(fill='both', expand=True)
l1 = tkinter.Label(frame1, text="CN project", font=("Arial Bold", 25))
l1.grid(column=0, row=0)
player_name = tkinter.Label(frame1)
infoMessage = tkinter.StringVar()
infoMessage.set("Enter the button below to get started.")
infoLabel = tkinter.Label(frame1, textvariable=infoMessage)
infoLabel.grid(column=0, row=1)
quit = tkinter.StringVar()
question = tkinter.StringVar()
choice1 = tkinter.StringVar()
choice2 = tkinter.StringVar()
choice3 = tkinter.StringVar()
choice4 = tkinter.StringVar()
correct_option = tkinter.IntVar()
quesLabel = tkinter.Label(frame1, textvariable=question)
player_name.grid(column=0, row=2, columnspan=3, sticky=tkinter.W)
submit_name = tkinter.Button(frame1, text='Join Game', command=sendName)
submit_name.grid(column=1, row=2, columnspan=3, sticky=tkinter.W)
c1 = tkinter.Radiobutton(frame1, textvariable=choice1, variable=correct_option, value=1)
c2 = tkinter.Radiobutton(frame1, textvariable=choice2, variable=correct_option, value=2)
c3 = tkinter.Radiobutton(frame1, textvariable=choice3, variable=correct_option, value=3)
c4 = tkinter.Radiobutton(frame1, textvariable=choice4, variable=correct_option, value=4)
submit_button = tkinter.Button(frame1, text='Submit Answer', command=sendAnswer)
top.protocol("WM_DELETE_WINDOW", on_closing)

# ----the chat gui----


# to show chat window
frame2.configure(width=470, height=550)
labelHead = Label(frame2,
                  bg="#17202A",
                  fg="#EAECEE",
                  text=name,
                  font="Helvetica 13 bold",
                  pady=5)

labelHead.place(relwidth=1)
line = Label(frame2,
             width=450,
             bg="#ABB2B9")

line.place(relwidth=1,
           rely=0.07,
           relheight=0.012)

textCons = Text(frame2,
                width=20,
                height=2,
                bg="#17202A",
                fg="#EAECEE",
                font="Helvetica 14",
                padx=5,
                pady=5)

textCons.place(relheight=0.745,
               relwidth=1,
               rely=0.08)

labelBottom = Label(frame2,
                    bg="#ABB2B9",
                    height=80)

labelBottom.place(relwidth=1,
                  rely=0.825)

entryMsg = Entry(labelBottom,
                 bg="#2C3E50",
                 fg="#EAECEE",
                 font="Helvetica 13")

# place the given widget
# into the gui window
entryMsg.place(relwidth=0.74,
               relheight=0.06,
               rely=0.008,
               relx=0.011)

entryMsg.focus()

# create a Send Button
buttonMsg = Button(labelBottom,
                   text="Send",
                   font="Helvetica 10 bold",
                   width=20,
                   bg="#ABB2B9",
                   command=lambda: sendButton(entryMsg.get()))

buttonMsg.place(relx=0.77,
                rely=0.008,
                relheight=0.06,
                relwidth=0.22)

textCons.config(cursor="arrow")

# create a scroll bar
scrollbar = tkinter.Scrollbar(textCons)

# place the scroll bar
# into the gui window
scrollbar.place(relheight=1,
                relx=0.974)

scrollbar.config(command=textCons.yview)

textCons.config(state=DISABLED)

notebook.add(frame1, text='Main Game')
notebook.add(frame2, text='Chatroom')
# ----Now comes the sockets part----


HOST = "127.0.0.1"
f.close()
BUFSIZ = 1024
ADDR = (HOST, PORT)
start_timer = None
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.bind(('127.0.0.1', client_port))
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()

# client_socket.send(bytes("I'm here!", "utf8"))
