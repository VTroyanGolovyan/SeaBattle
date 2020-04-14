from tkinter import Tk
from socket import *

from server_listener import ServerListener
from view_factory import ViewFactory

root = Tk()
root.title('SeaBattle By vhdev')
root.resizable(width=False, height=False)
root.rowconfigure(1, weight=1)

try:
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(('127.0.0.1', 47775))
    viewController = ViewFactory(root, sock)
    viewController.changeView('Menu')
    # run server listener
    ServerListener(viewController, sock).start()
except Exception:
    viewController = ViewFactory(root, '')
    viewController.changeView('Error')

root.mainloop()
