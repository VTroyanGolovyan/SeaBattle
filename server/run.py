from threading import Thread
from socket import *

tcp_socket = socket(AF_INET, SOCK_STREAM)
tcp_socket.bind((gethostbyname('localhost'), 47777))
tcp_socket.listen(1000)

connections = set()


class Player:
    def __init__(self, connection):
        self.connection = connection
        self.map = [[0 for i in range(10)] for i in range(10)]

    def step(self, enemy):
        pass


class GameModel:
    def __init__(self, first_player, second_player):
        self.first_player = first_player
        self.second_player = second_player
        self.turn = 0

    def step(self):
        if self.turn == 0:
            self.turn = 1
            self.first_player.step(self.second_player)
        else:
            self.turn = 0
            self.second_player.step(self.first_player)


class Server(Thread):
    def __init__(self, game_model):
        super().__init__()
        self.game_model = game_model
        self.connections = connections

    def run(self):
        while True:
            self.game_model.step()


while True:
    first_conn = tcp_socket.accept()
    print('connection1')
    second_conn = tcp_socket.accept()
    print('connection2')
    Server(GameModel(Player(first_conn), Player(second_conn)))
