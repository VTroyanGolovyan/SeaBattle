from threading import Thread
import socket
from player import Player

socket.allow_reuse_address = True
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind(('127.0.0.1', 47775))
tcp_socket.listen(1000)


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
