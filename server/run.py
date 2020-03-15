from threading import Thread
from socket import *
from random import randint

tcp_socket = socket(AF_INET, SOCK_STREAM)
tcp_socket.bind((gethostbyname('localhost'), 47777))
tcp_socket.listen(1000)

connections = set()


class Player:
    def __init__(self, connection):
        self.connection = connection
        self.map = [[0 for i in range(10)] for i in range(10)]

    def step(self, enemy):
        data = self.connection.recv(256).decode('utf-8')
        print(data)
        data_list = data.split(' ', 1)
        coords = data_list[1].split(' ', 1)
        if enemy.shot(int(coords[0]), int(coords[1])):
            enemy.get_conn().send('myhit '.encode('utf-8') + data_list[1].encode('utf-8'))
            self.connection.send('hit '.encode('utf-8') + data_list[1].encode('utf-8'))
        else:
            self.connection.send('past '.encode('utf-8') + data_list[1].encode('utf-8'))
            enemy.get_conn().send(data.encode('utf-8'))

    def generate_ships(self):
        for i in range(25):
            self.map[randint(0, 9)][randint(0, 9)] = 1

    def shot(self, x, y):
        if self.map[x][y] == 1:
            self.map[x][y] = 2
            return True
        else:
            return False

    def get_conn(self):
        return self.connection


class GameModel:
    def __init__(self, first_player, second_player):
        self.first_player = first_player
        self.second_player = second_player
        first_player.generate_ships()
        second_player.generate_ships()
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
    Server(GameModel(Player(first_conn[0]), Player(second_conn[0]))).start()
