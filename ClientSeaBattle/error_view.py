from tkinter import Frame, Button
from BaseView import BaseView


class ErrorView(BaseView):

    def __init__(self, userSocket, controller, text='Error'):
        BaseView.__init__(self, userSocket, controller)
        self.text = text

    def draw(self, root):
        frame = Frame(root, bg='green', bd=5)
        start_btn = Button(
            frame,
            text=self.text,
            bg='white',
            fg='black',
            height=2,
            width=20
        )
        start_btn.pack(fill='both')
        frame.grid(row=0, column=0)

