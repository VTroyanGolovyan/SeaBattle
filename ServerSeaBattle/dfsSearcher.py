def check(array, x, y):
    if x >= 10 or y >= 10 or x < 0 or y < 0:
        return True
    return array[x][y] in [0, 2, 3, 7]


def isZero(array, x, y):
    if x >= 10 or y >= 10 or x < 0 or y < 0:
        return False
    return array[x][y] == 0


def is_set(x, y):
    if x >= 10 or y >= 10 or x < 0 or y < 0:
        return False
    return True


def checkPlace(array, x, y):
    res = check(array, x, y)
    for i in range(-1, 2):
        for j in range(-1, 2):
            res = res and check(array, x + i, y + j)
    return res


def dfs(array, x, y, acc):
    if is_set(x, y) and checkPlace(array, x, y):
        if array[x][y] == 2:
            acc.append([x, y])
            temp = array[x][y]
            array[x][y] = 7
            res = True
            res = res and dfs(array, x + 1, y, acc)
            res = res and dfs(array, x - 1, y, acc)
            res = res and dfs(array, x, y + 1, acc)
            res = res and dfs(array, x, y - 1, acc)
            array[x][y] = temp
            return res
        else:
            return array[x][y] != 1 and array[x][y] != 2
    else:
        if is_set(x, y):
            return array[x][y] != 1 and array[x][y] != 2
        else:
            return True


def getNotDestroyed(array, x, y, acc):
    ship = []
    if dfs(array, x, y, ship):
        for el in ship:
            x = el[0]
            y = el[1]
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if isZero(array, x + i, y + j):
                        acc.append([x + i, y + j])
