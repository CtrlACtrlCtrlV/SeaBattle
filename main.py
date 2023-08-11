import random
import os

size = 6
monitoring = True

# То как будут выглядеть наши корабли
s_buffer = "О" # Буфер
s_ship = "■" # Пространство
s_space = "О" # Пустое пространство
s_hit = "X" # Подбитый корабль
s_destroyed = "X" # Разрушенный корабль
s_miss = "T" # Промах

ships_list = [[1, 3], [2, 2], [4, 1]]


class Board(object): # Создание класса игрового поля

    def __init__(self):
        self.board = []
        self.spawned = []

    def create(self):
        for row in range(size):
            self.board.append([s_space] * size)

    def random(self): # Функция рандомного спавна кораблей(но не их прорисовки)

        for ship in ships_list:
            for unit in range(ship[0]):

                spawning = True
                while spawning:

                    global refer
                    refer = random.randrange(1)
                    if refer == 0:
                        location_y = random.randrange(size)
                        location_x = random.randrange(size - (ship[1] - 1))
                    else:
                        location_y = random.randrange(size - (ship[1] - 1))
                        location_x = random.randrange(size)

                    offset = 0
                    for testing in range(ship[1]):
                        if refer == 0 and self.board[location_y][location_x + offset] != s_space:
                            continue
                        elif refer == 1 and self.board[location_y + offset][location_x] != s_space:
                            continue
                        offset += 1
                        if offset == ship[1]:
                            spawning = False

                offset = 0
                current_ship = []
                for marker in range(ship[1]):
                    if refer == 0:
                        self.board[location_y][location_x + offset] = s_ship
                        current_ship.append([location_y, location_x + offset])
                    else:
                        self.board[location_y + offset][location_x] = s_ship
                        current_ship.append([location_y + offset, location_x])
                    offset += 1
                self.spawned.append(current_ship)

                for unit_point in current_ship:
                    for buffer_point in ([0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]):
                        b_point_y = unit_point[0] + buffer_point[0]
                        b_point_x = unit_point[1] + buffer_point[1]
                        if b_point_y in range(size) and b_point_x in range(size):
                            if self.board[b_point_y][b_point_x] == s_space:
                                self.board[b_point_y][b_point_x] = s_buffer

    def updating(self, ship): # Буферная зона
        for unit in ship:
            for buffer_point in ([0, 0], [0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]):
                b_point_y = unit[0] + buffer_point[0]
                b_point_x = unit[1] + buffer_point[1]
                if b_point_y in range(size) and b_point_x in range(size):
                    if self.board[b_point_y][b_point_x] == s_buffer:
                        self.board[b_point_y][b_point_x] = s_miss
                    elif self.board[b_point_y][b_point_x] == s_hit:
                        self.board[b_point_y][b_point_x] = s_destroyed


def print_boards(): # отрисовка поля
    print("\n    Ваше поле" + (" " * (size+1)) + "Поле противника")
    print((' |1|2|3|4|5|6|'), end=('' * 2))
    print('   |1|2|3|4|5|6|')
    n = 0
    for i in range(size):
        if monitoring:
            print(str(n+1) + "|" + "|".join(str(i) for i in player.board[n]) + '|', end=(" " * 2))
            print(str(n+1) + "|" + "|".join(str(i) for i in ai.board[n]) + '|')
        else:
            print(str(n) + " - " + " ".join(str(i) for i in player.board[n]).replace(s_buffer, s_space), end=(" " * 2))
            print(str(n) + " - " + " ".join(str(i) for i in ai.board[n]).replace(s_ship, s_space).replace(s_buffer,
                                                                                                          s_space))
        n += 1


def press_ent():
    input("Нажмите ENTER чтобы продолжить.\n")


def state_of_ships(enemy): # Отслежка состояния коробля
    global destroy
    destroy = False
    for d_ship in enemy.spawned:
        damage = 0
        for d_unit in d_ship:
            if enemy.board[d_unit[0]][d_unit[1]] == s_hit:
                damage += 1
        if damage == len(d_ship):
            enemy.updating(d_ship)
            enemy.spawned.remove(d_ship)
            destroy = True


def ai_pass(): # Ход компьютера
    ai_guessing = True
    while ai_guessing:

        ai_intuition = random.randrange(size * 5)

        if ai_intuition == 0:
            ai_int_ship = random.randrange(len(player.spawned))
            ai_int_unit = random.randrange(len(player.spawned[ai_int_ship]))
            ai_guess_y = player.spawned[ai_int_ship][ai_int_unit][0]
            ai_guess_x = player.spawned[ai_int_ship][ai_int_unit][1]

        else:
            ai_guess_y = random.randrange(size)
            ai_guess_x = random.randrange(size)

        if player.board[ai_guess_y][ai_guess_x] == s_ship:
            player.board[ai_guess_y][ai_guess_x] = s_hit
            state_of_ships(player)
            if destroy:
                print("\nБот уничтожил ваше судно (X: %s, Y: %s)." % (ai_guess_x, ai_guess_y))
            else:
                print("\nБот повредил ваше судно (X: %s, Y: %s)." % (ai_guess_x, ai_guess_y))
            break

        elif player.board[ai_guess_y][ai_guess_x] == s_space or player.board[ai_guess_y][ai_guess_x] == s_buffer:
            player.board[ai_guess_y][ai_guess_x] = s_miss
            print("\nБот выстрелил мимо (X: %s, Y: %s)." % (ai_guess_x, ai_guess_y))
            break

        else:
            continue


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


print("Добро пожаловать в игру \"Морской Бой\"\n")
press_ent()

ai = Board()
ai.create()
ai.random()

while True: # Цикл игры пока не (останавливается в конце игры)
    clear()
    print('Если поле не появилось перезагрузите игру.')
    player = Board()
    player.create()
    player.random()
    print_boards()
    print("Если вас не устраивает расположение вашего поля нажмите ENTER для генерации нового.")
    regenerate = input("Если вы готовы напишите \"да\"")
    if str(regenerate.lower()) != "да":
        continue
    else:
        break

print("\nОкей Начинаем! Готовьтесь!\n")
press_ent()

game = True
while game:

    clear()
    ai_pass()
    print_boards()

    guessing = True
    while guessing:

        print("\nКораблей противника осталось: " + str(len(ai.spawned)) + ". ", end="")
        print("Кораблей осталось у вас: " + str(len(player.spawned)) + ".")

        guess_x = input("Выберите Y (столбик) для стрельбы: ")
        guess_y = input("Выберите X (строчка) для стрельбы: ")

        if not guess_x.isdigit() or not guess_y.isdigit():
            print("\nВы ввели неверные координаты пожалуйста введите новые.")
            continue

        guess_x = int(guess_x) - 1 # Костыль) ибо 123, а не 012
        guess_y = int(guess_y) - 1

        if not (guess_x in range(size)) or not (guess_y in range(size)):
            print("\nЭта клетка слишком далеко, чтобы поразить ее! Выберите другую.")
            continue

        elif ai.board[guess_y][guess_x] == s_ship:
            ai.board[guess_y][guess_x] = s_hit
            state_of_ships(ai)
            if destroy:
                print("\nВы уничтожили судно противника!", end=" ")
            else:
                print("\nВы повредили судно противника!", end=" ")
            press_ent()
            break

        elif ai.board[guess_y][guess_x] == s_space or ai.board[guess_y][guess_x] == s_buffer:
            ai.board[guess_y][guess_x] = s_miss
            print("\nВы промахнулись(.", end=" ")
            press_ent()

        else:
            print("\nВы уже выстрелили в этот квадрат пожалуйста выберите другую")
            continue
        break

    if len(ai.spawned) == 0:
        input("ВЫ ПОБЕДИТЕЛЬ! ВЫ УНИЧТОИЛИ ВСЕ СУДНА ПРОТИВНИКА! Нажмите ENTER чтобы завершить игру.")
        break

    if len(player.spawned) == 0:
        print("ВЫ ПРОИГРАЛИ! ПРОТИВНИК УНИЧТОЖИЛ ВСЕ ВАШИ СУДНА")
        input("Судна оставшиеся у противника: " + str(len(ai.spawned)) + ".")
        break