def check(array, x, y):
    if x >= 10:
        return True
    if y >= 10:
        return True
    if x < 0:
        return True
    if y < 0:
        return True
    return array[x][y] in [0, 2, 3, 7]


def isZero(array, x, y):
    if x >= 10:
        return False
    if y >= 10:
        return False
    if x < 0:
        return False
    if y < 0:
        return False
    return array[x][y] == 0


def isset(x, y):
    if x >= 10:
        return False
    if y >= 10:
        return False
    if x < 0:
        return False
    if y < 0:
        return False
    return True


def checkPlace(array, x, y):
    res = check(array, x, y)
    res = res and check(array, x, y)
    res = res and check(array, x, y + 1)
    res = res and check(array, x, y - 1)
    res = res and check(array, x + 1, y)
    res = res and check(array, x - 1, y)
    res = res and check(array, x - 1, y - 1)
    res = res and check(array, x - 1, y + 1)
    res = res and check(array, x + 1, y - 1)
    res = res and check(array, x + 1, y + 1)
    return res


def dfs(array, x, y, acc):
    if isset(x, y) and checkPlace(array, x, y):
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
            return True
    else:
        if isset(x, y):
            if array[x][y] == 1:
                return False
            else:
                return True
        else:
            return True


def getNotDestroyed(array, x, y, acc):
    ship = []
    if dfs(array, x, y, ship):
        for el in ship:
            x = el[0]
            y = el[1]
            if isZero(array, x, y + 1):
                acc.append([x, y + 1])
            if isZero(array, x, y - 1):
                acc.append([x, y - 1])
            if isZero(array, x + 1, y):
                acc.append([x + 1, y])
            if isZero(array, x - 1, y):
                acc.append([x - 1, y])
            if isZero(array, x - 1, y - 1):
                acc.append([x - 1, y - 1])
            if isZero(array, x - 1, y + 1):
                acc.append([x - 1, y + 1])
            if isZero(array, x + 1, y - 1):
                acc.append([x + 1, y - 1])
            if isZero(array, x + 1, y + 1):
                acc.append([x + 1, y + 1])
