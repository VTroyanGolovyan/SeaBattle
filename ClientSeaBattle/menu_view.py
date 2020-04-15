from tkinter import Frame, Button, Label
from tkinter import BOTH, X
from BaseView import BaseView


def make_click_callback(socket, controller):
    def click(event):
        socket.send('new_game'.encode('utf-8'))
        controller.changeView('GameView')

    return click


class MenuView(BaseView):

    def __init__(self, userSocket, controller):
        BaseView.__init__(self, userSocket, controller)

    def draw(self, root):
        frame = Frame(root, bd=5)

        game_label = Label(
            frame,
            text='Sea Battle',
            bg='#c509d6',
            fg='black',
            height=2,
            width=20
        )

        start_btn = Button(
            frame,
            text='Start',
            bg='white',
            fg='black',
            height=2,
            width=20,
            cursor='hand1'
        )
        start_btn.bind(
            '<Button-1>',
            make_click_callback(self.userSocket, self.controller)
        )
        game_label.pack(fill=X, pady=(20, 20))
        start_btn.pack(fill=BOTH)
        frame.grid(row=0, column=0, padx=(40, 40), pady=(40, 60))
