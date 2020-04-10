from threading import Thread


class ServerListener(Thread):

    def __init__(self, controller, userSocket):
        Thread.__init__(self)
        self.controller = controller
        self.userSocket = userSocket

    def run(self):
        while True:
            try:
                data = self.userSocket.recv(256).decode('utf-8')
                data_arr = data.split('#')
                for change in data_arr:
                    if change != '':
                        self.controller.update(change)
                if data == '':
                    break
            except Exception:
                break
