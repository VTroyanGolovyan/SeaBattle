from random import randint


def check(array, x, y):
    if x >= 10:
        return False
    if y >= 10:
        return False
    if x < 0:
        return False
    if y < 0:
        return False
    return array[x][y] != 0


def checkLineShip(array, x, start, size):
    for i in range(size):
        res = array[x][start + i] != 0
        res = res or check(array, x, start + i)
        res = res or check(array, x, start + i + 1)
        res = res or check(array, x, start + i - 1)
        res = res or check(array, x + 1, start + i)
        res = res or check(array, x - 1, start + i)
        res = res or check(array, x - 1, start + i - 1)
        res = res or check(array, x - 1, start + i + 1)
        res = res or check(array, x + 1, start + i - 1)
        res = res or check(array, x + 1, start + i + 1)
        if res:
            return False
    return True


def checkColumnShip(array, start, y, size):
    for i in range(size):
        res = array[start + i][y] != 0
        res = res or check(array, start + i, y)
        res = res or check(array, start + i + 1, y)
        res = res or check(array, start + i - 1, y)
        res = res or check(array, start + i, y + 1)
        res = res or check(array, start + i, y - 1)
        res = res or check(array, start + i - 1, y - 1)
        res = res or check(array, start + i + 1, y - 1)
        res = res or check(array, start + i - 1, y + 1)
        res = res or check(array, start + i + 1, y + 1)
        if res:
            return False
    return True


def columnGen(array, i, size):
    move = randint(0, 9 - size - 1)
    for j in range(move, 9 - size + 1):
        if checkColumnShip(array, j, i, size):
            setColumnShip(array, j, i, size)
            return True
    return False


def setColumnShip(array, x, y, size):
    for i in range(size):
        array[x + i][y] = 1


def setLineShip(array, x, y, size):
    for i in range(size):
        array[x][y + i] = 1


def rowGen(array, i, size):
    move = randint(0, 9 - size - 1)
    for j in range(move, 9 - size + 1):
        if checkLineShip(array, i, j, size):
            setLineShip(array, i, j, size)
            return True
    return False


def genShip(array, size, number):
    if randint(0, 1) == 0:
        return rowGen(array, number, size)
    else:
        return columnGen(array, number, size)


def shipsGenerator(array):
    for i in range(1, 4):
        for j in range(5 - i):
            while True:
                number = randint(0, 9)
                if genShip(array, i, number):
                    break
    print(array)
