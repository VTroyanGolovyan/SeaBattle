class BaseView:

    def __init__(self, userSocket, controller, text=''):
        self.userSocket = userSocket
        self.controller = controller
        self.text = text

    def draw(self, root):
        pass

    def update(self, *args):
        pass

    def remove(self):
        pass
