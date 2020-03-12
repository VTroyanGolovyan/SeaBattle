from tkinter import *
from threading import Thread
from socket import *

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('localhost', 47777))

root = Tk()

buttons1 = []
buttons2 = []


def MakeCallback(i, j, buttons):
    def Callback(event):
        print(str(i) + str(j))
        sock.send('push '.encode('utf-8') + str(i).encode('utf-8') + ' '.encode('utf-8') + str(j).encode('utf-8'))
        buttons[i][j].configure(bg='green', fg='green')

    return Callback


def MakeMap(container, size, buttons):
    for i in range(size):
        row = []
        for j in range(size):
            btn = Button(container, text='', bg='white', fg='white')
            btn.grid(row=i, column=j)
            btn.bind('<Button-1>', MakeCallback(i, j, buttons))
            row.append(btn)
        buttons.append(row)


frame1 = Frame(root, bg='green', bd=5)
frame2 = Frame(root, bg='red', bd=5)
frame1.grid(row=0, column=0)
frame2.grid(row=0, column=1)
MakeMap(frame1, 10, buttons1)
MakeMap(frame2, 10, buttons2)

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)


class ServerListener(Thread):
    def __init__(self, sock, buttons):
        super().__init__()
        self.sock = sock
        self.buttons = buttons

    def run(self):
        while True:
            print('jojo')
            data = self.sock.recv(256).decode('utf-8').split(' ', 1)
            print(data)
            coords = data[1].split(' ', 1)
            self.buttons[int(coords[0])][int(coords[1])].configure(bg='red', fg='yellow')
            root.update()


ServerListener(sock, buttons1).start()

root.mainloop()
