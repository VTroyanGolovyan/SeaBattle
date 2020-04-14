from threading import Thread
from socket import *
from player import Player

tcp_socket = socket(AF_INET, SOCK_STREAM)
tcp_socket.bind(('127.0.0.1', 47776))
tcp_socket.listen(1000)

connections = set()


class Server(Thread):
    def __init__(self, player):
        super().__init__()
        self.player = player

    def run(self):
        while True:
            try:
                self.player.process_msg()
            except Exception:
                break


waitList = []

while True:
    first_conn = tcp_socket.accept()
    print('connection')
    Server(Player(first_conn[0], waitList)).start()
