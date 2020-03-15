from tkinter import *
from threading import Thread
from socket import *

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('localhost', 47778))

root = Tk()
root.title('SeaBattle By vhdev')

buttons1 = []
buttons2 = []

turn = 1  # user turn in game


def MakeCallback(i, j, buttons):
    def Callback(event):
        global turn
        if turn == 1:
            print(str(i) + str(j))
            sock.send('push '.encode('utf-8') + str(i).encode('utf-8') + ' '.encode('utf-8') + str(j).encode(
                'utf-8') + '\n'.encode('utf-8'))
            buttons[i][j].configure(bg='grey', fg='grey')
            turn = 0

    return Callback


def MakeMap(container, size, buttons, clickable=False):
    for i in range(size):
        row = []
        for j in range(size):
            btn = Button(container, text='', bg='white', fg='white',  height=2, width=2)
            btn.grid(row=i, column=j)
            if clickable:
                btn.bind('<Button-1>', MakeCallback(i, j, buttons))
            row.append(btn)
        buttons.append(row)


frame1 = Frame(root, bg='green', bd=5)
frame2 = Frame(root, bg='red', bd=5)
frame1.grid(row=0, column=0)
frame2.grid(row=0, column=1)
MakeMap(frame1, 10, buttons1)
MakeMap(frame2, 10, buttons2, clickable=True)

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)


class ServerListener(Thread):
    def __init__(self, sock, my_map_buttons, enemy_map_buttons):
        super().__init__()
        self.sock = sock
        self.my_map_buttons = my_map_buttons
        self.enemy_map_buttons = enemy_map_buttons

    def run(self):
        while True:
            data = self.sock.recv(256).decode('utf-8').split(' ', 1)
            print(data)
            global turn
            if data[0] == 'push':
                coords = data[1].split(' ', 1)
                self.my_map_buttons[int(coords[0])][int(coords[1])].configure(bg='#f7f79c', fg='#f7f79c')
                root.update()
                turn = 1
            elif data[0] == 'hit':
                coords = data[1].split(' ', 1)
                self.enemy_map_buttons[int(coords[0])][int(coords[1])].configure(bg='#8dff36', fg='#8dff36')
                root.update()
            elif data[0] == 'myhit':
                coords = data[1].split(' ', 1)
                self.my_map_buttons[int(coords[0])][int(coords[1])].configure(bg='red', fg='#8dff36')
                root.update()
                turn = 1
            elif data[0] == 'gameover':
                turn = 0
                print(data[1])


ServerListener(sock, buttons1, buttons2).start()

root.mainloop()
