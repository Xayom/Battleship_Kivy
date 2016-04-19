import random

def randomization(SHIPS, COORDS):
    ANS_LIST = []
    for ship in SHIPS:
        size_of_ship = ship[0]
        amount = ship[1]
        color = ship[2]

        for kol in range(amount):
            while True:
                rand = random.randint(0, len(COORDS) - 1)
                rand1 = random.randint(0, 1)
                x, y = COORDS[rand]

                check = 0
                for i in range(size_of_ship):
                    if (x + i * (rand1 == 0), y + i * (rand1 != 0)) in COORDS:
                        check += 1

                if check == size_of_ship:
                    for i in range(size_of_ship):
                        a = x + i * (rand1 == 0)
                        b = y + i * (rand1 != 0)
                        ANS_LIST.append([(a, b), color, size_of_ship])
                        if (a, b) in COORDS:
                            COORDS.remove((a, b))
                        if ((a + 1, b) in COORDS):
                            COORDS.remove((a + 1, b))
                        if ((a, b + 1) in COORDS):
                            COORDS.remove((a, b + 1))
                        if ((a - 1, b) in COORDS):
                            COORDS.remove((a - 1, b))
                        if ((a, b - 1) in COORDS):
                            COORDS.remove((a, b - 1))
                        if ((a + 1, b - 1) in COORDS):
                            COORDS.remove((a + 1, b - 1))
                        if ((a - 1, b + 1) in COORDS):
                            COORDS.remove((a - 1, b + 1))
                        if ((a - 1, b - 1) in COORDS):
                            COORDS.remove((a - 1, b - 1))
                        if ((a + 1, b + 1) in COORDS):
                            COORDS.remove((a + 1, b + 1))
                    break
    return ANS_LIST