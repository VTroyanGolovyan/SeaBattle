from tkinter import Frame, Button, Label, Entry, Listbox, Scrollbar
from tkinter import END, X, Y, BOTH, RIGHT
import tkinter.font as tkFont
from BaseView import BaseView


def MakeCallback(i, j, buttons, socket):
    def Callback(event):
        request = 'shot ' + str(i) + ' ' + str(j)
        socket.send(request.encode('utf-8'))

    return Callback


def MakeChatCallback(entry, socket):
    def Callback(event):
        check = entry.get().replace('#', '')
        check = check.replace(' ', '')
        if check == '':
            return
        request = 'msg ' + entry.get().replace('#', '')
        entry.delete(0, END)
        socket.send(request.encode('utf-8'))

    return Callback


def MakeMap(container, buttons, socket, font, clickable=False):
    for i in range(10):
        row = []
        for j in range(10):
            btn = Button(
                container,
                text='',
                bg='white',
                fg='black',
                height=2,
                width=2,
                font=font
            )
            btn.grid(row=i, column=j)
            if clickable:
                btn.bind(
                    '<Button-1>',
                    MakeCallback(i, j, buttons, socket)
                )
            row.append(btn)
        buttons.append(row)


def get_coords(data):
    coords = data.split(' ')
    return int(coords[0]), int(coords[1])


class GameView(BaseView):

    def __init__(self, userSocket, controller):
        BaseView.__init__(self, userSocket, controller)
        self.playerButtons = []
        self.enemyButtons = []
        self.infoLabel = Label()
        self.chatList = Listbox()
        self.fontStyle = tkFont.Font(size=12)

    def draw(self, root):
        playerFrame = Frame(root, bg='green', bd=2)
        enemyFrame = Frame(
            root,
            bg='green',
            bd=2,
            cursor='plus'
        )

        MakeMap(
            playerFrame,
            self.playerButtons,
            self.userSocket,
            self.fontStyle,
            False
        )
        MakeMap(
            enemyFrame,
            self.enemyButtons,
            self.userSocket,
            self.fontStyle,
            True
        )

        chatFrame = Frame(root, bg='white', bd=2)
        self.infoLabel = Label(
            chatFrame, bg='grey',
            fg='black',
            text='GameInfo'
        )

        chatBox = Listbox(chatFrame)
        self.chatList = chatBox
        entry = Entry(chatFrame)
        entry.insert(0, 'Write your text')

        def click(event):
            entry.delete(0, END)

        entry.bind('<Button-1>', click)

        sendBtn = Button(
            chatFrame,
            text='Send Message',
            bg='white',
            fg='black',
            cursor='hand1'
        )

        sendBtn.bind(
            '<Button-1>',
            MakeChatCallback(entry, self.userSocket)
        )

        entry.bind(
            '<Return>',
            MakeChatCallback(entry, self.userSocket)
        )

        scrollbar = Scrollbar(chatFrame)
        scrollbar.pack(side=RIGHT, fill=Y)

        chatBox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=chatBox.yview)

        self.infoLabel.pack(fill=X)
        chatBox.pack(expand=1, fill=BOTH)
        entry.pack(fill=X)
        sendBtn.pack(fill=X)

        playerFrame.grid(row=0, column=0, sticky='nsew')
        enemyFrame.grid(row=0, column=1, sticky='nsew')
        chatFrame.grid(row=0, column=2, sticky='nsew')

    def update(self, serverMessage):
        if serverMessage == '':
            self.controller.changeView('Error')
        data = serverMessage.split(' ', 1)

        print(data)
        if data[0] == 'msg':
            self.chatList.insert(END, data[1])
            self.chatList.yview(END)
        elif data[0] == 'beside':
            x, y = get_coords(data[1])
            self.enemyButtons[x][y].configure(
                bg='grey',
                fg='grey',
                cursor="plus"
            )
        elif data[0] == 'enemy_beside':
            x, y = get_coords(data[1])
            self.playerButtons[x][y].configure(
                bg='grey',
                fg='grey'
            )
        elif data[0] == 'hit':
            x, y = get_coords(data[1])
            self.enemyButtons[x][y].configure(
                bg='green',
                fg='white',
                text='#'
            )
        elif data[0] == 'enemy_hit':
            x, y = get_coords(data[1])
            self.playerButtons[x][y].configure(bg='red', fg='white')
        elif data[0] == 'win':
            self.controller.changeView('Result', text='You win')
        elif data[0] == 'lose':
            self.controller.changeView('Result', text='You lose')
        elif data[0] == 'turn':
            if int(data[1]) == 0:
                self.infoLabel.configure(
                    text='Your turn',
                    bg='green'
                )
            else:
                self.infoLabel.configure(
                    text='Enemy turn',
                    bg='red'
                )
        elif data[0] == 'set_ship':
            x, y = get_coords(data[1])
            self.playerButtons[x][y].configure(
                bg='yellow',
                fg='red',
                text='#'
            )
