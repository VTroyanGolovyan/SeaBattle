from tkinter import Frame, Button
from BaseView import BaseView


def make_click_callback(socket, controller):
    def click(event):
        controller.changeView('Menu')
    return click


class ResultView(BaseView):

    def __init__(self, userSocket, controller, text=''):
        BaseView.__init__(self, userSocket, controller, text)
        self.res_btn = ''

    def draw(self, root):
        frame = Frame(root, bg='green', bd=5)
        res_btn = Button(
            frame,
            text=self.text,
            bg='white',
            fg='black',
            height=2,
            width=20
        )
        res_btn.bind(
            '<Button-1>',
            make_click_callback(self.userSocket, self.controller)
        )
        res_btn.pack(fill='both')

        frame.grid(row=0, column=0)


