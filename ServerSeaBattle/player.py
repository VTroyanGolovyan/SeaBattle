from dfsSearcher import getNotDestroyed
from shipsGenerator import shipsGenerator
import time


class WaitObject:
    def __init__(self, player):
        self.player = player


class Player:
    def __init__(self, connection, waitList):
        self.connection = connection
        self.map = [[0 for i in range(10)] for i in range(10)]
        self.ships_count = 0
        self.waitList = waitList
        self.enemy = ''
        self.turn = 0

    def process_msg(self):
        data = self.connection.recv(256).decode('utf-8')
        print(data)
        if data.replace(' ', '') == '':
            raise Exception('IncorrectInput')
        data_list = data.split(' ', 1)
        if data_list[0] == 'shot':

            if self.enemy == '':
                return
            if self.turn != 0:
                return

            coords = data_list[1].split(' ')
            result = self.enemy.shot(int(coords[0]), int(coords[1]))
            if result == 0:
                self.send('beside ' + data_list[1])
                self.enemy.send('enemy_beside ' + data_list[1])
            elif result == 1:
                self.send('hit ' + data_list[1])
                self.enemy.send('enemy_hit ' + data_list[1])
                acc = []
                getNotDestroyed(
                    self.enemy.map,
                    int(coords[0]),
                    int(coords[1]),
                    acc
                )
                self.pushArray(acc, 'beside')
                self.enemy.pushArray(acc, 'enemy_beside')
                for el in acc:
                    self.enemy.map[el[0]][el[1]] = 3
                if self.enemy.isAllDie():
                    print('endgame')
                    self.send('win')
                    self.enemy.send('lose')
            if result == 0 and result != 2:
                self.setTurn(1)
                self.enemy.setTurn(0)

        elif data_list[0] == 'new_game':
            self.checkWaitList()

        elif data_list[0] == 'msg':
            self.send('msg you: ' + data_list[1])
            if self.enemy == '':
                return
            self.enemy.send(('msg enemy: ' + data_list[1]))

    def checkWaitList(self):
        if len(self.waitList) == 0:
            self.waitList.append(WaitObject(self))
        else:
            self.enemy = self.waitList[0].player
            del self.waitList[0]
            self.enemy.setEnemy(self)
            self.generate_ships()
            self.enemy.generate_ships()
            time.sleep(0.2)
            self.setTurn(1)
            self.enemy.setTurn(0)
            self.pushShips()
            self.enemy.pushShips()

    def step(self):
        self.turn = 0

    def generate_ships(self):
        for i in range(10):
            for j in range(10):
                self.map[i][j] = 0
        shipsGenerator(self.map)
        self.ships_count = 0
        for i in range(10):
            for j in range(10):
                if self.map[i][j] == 1:
                    self.ships_count += 1

    def isAllDie(self):
        count = 0
        for i in range(10):
            for j in range(10):
                if self.map[i][j] == 2:
                    count += 1
        return count == self.ships_count

    def shot(self, x, y):
        if self.map[x][y] == 1:
            self.map[x][y] = 2
            return 1
        elif self.map[x][y] == 0:
            self.map[x][y] = 3
            return 0
        else:
            return 2

    def send(self, sendString):
        sendString += '#'
        self.connection.send(sendString.encode('utf-8'))

    def setEnemy(self, enemy):
        self.enemy = enemy

    def setTurn(self, turn):
        self.turn = turn
        self.send('turn ' + str(turn))

    def pushShips(self):
        for i in range(10):
            for j in range(10):
                if self.map[i][j] == 1:
                    self.send('set_ship ' + str(i) + ' ' + str(j))

    def pushArray(self, acc, command):
        for el in acc:
            self.send(command + ' ' + str(el[0]) + ' ' + str(el[1]))
