from menu_view import MenuView
from game_view import GameView
from result_view import ResultView
from error_view import ErrorView


class ViewFactory:

    def __init__(self, root, userSocket):
        self.userSocket = userSocket
        self.root = root
        self.view = self.createView('Menu')

    def changeView(self, name, text=''):
        self.clear()
        self.view = self.createView(name, text)
        self.view.draw(self.root)

    def clear(self):
        for element in self.root.grid_slaves():
            element.destroy()

    def createView(self, name, text=''):
        if name == 'Menu':
            return MenuView(self.userSocket, self)
        elif name == 'GameView':
            return GameView(self.userSocket, self)
        elif name == 'Result':
            return ResultView(self.userSocket, self, text)
        elif name == 'Error':
            return ErrorView(self.userSocket, self)

    def update(self, serverString):
        self.view.update(serverString)
