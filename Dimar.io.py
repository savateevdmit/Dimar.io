import os
import sqlite3
import sys
import time
from math import *
from random import *

import pygame
import pyglet
from PyQt5 import uic
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.font.init()
pygame.mixer.music.load("sounds/Фон1.mp3")
FPS = 30
COLOR = [((250, 0, 0), (200, 0, 0))]
COLORS = [((255, 80, 36), (240, 48, 0)), ((255, 136, 0), (224, 90, 0)), ((95, 230, 32), (74, 186, 22)),
          ((0, 255, 255), (29, 172, 214)), ((153, 102, 204), (120, 81, 169)), ((153, 50, 204), (114, 0, 163)),
          ((254, 40, 162), (224, 0, 123)), ((176, 63, 53), (128, 32, 32)), ((255, 186, 0), (255, 153, 0)),
          ((191, 255, 0), (150, 250, 0)), ((255, 163, 67), (247, 121, 10)), ((243, 71, 35), (248, 0, 0))]
MODE = ['normal']


class Start_window(QMainWindow):
    def __init__(self):
        super().__init__()
        COLOR.append(((250, 0, 0), (200, 0, 0)))
        uic.loadUi('Ui files/start.ui', self)  # Загружаем дизайн
        self.showFullScreen()

        pygame.mixer.music.play(-1)
        self.toolButton.clicked.connect(self.click)
        self.toolButton_2.clicked.connect(self.settings)
        self.toolButton_3.clicked.connect(self.info)

    def info(self):
        self.inf = Info()
        self.inf.show()

    def settings(self):
        self.set = Settings()
        self.set.show()

    def click(self):
        play = True
        self.name = self.lineEdit.text()
        if len(self.name) > 9:
            play = False
            self.message('Длина имени не может быть больше 9 символов!')

        elif len(self.name) == 0:
            self.name = 'Guest'

        if play:
            self.play()

    def exit(self):
        if len(str(round((self.end - self.start) // 60))) == 1 and len(str(round((self.end - self.start) % 60))) == 1:
            if self.end - self.start >= 60:
                self.label_3.setText(
                    str(f'0{round((self.end - self.start) // 60)}:0{round((self.end - self.start) % 60)}'))
            else:
                self.label_3.setText(str(f'00:0{round(self.end - self.start)}'))
        elif len(str(round((self.end - self.start) // 60))) == 2 and len(str(round((self.end - self.start) % 60))) == 1:
            if self.end - self.start >= 60:
                self.label_3.setText(
                    str(f'{round((self.end - self.start) // 60)}:0{round((self.end - self.start) % 60)}'))
            else:
                self.label_3.setText(str(f'00:0{round(self.end - self.start)}'))
        elif len(str(round((self.end - self.start) // 60))) == 1 and len(str(round((self.end - self.start) % 60))) == 2:
            if self.end - self.start >= 60:
                self.label_3.setText(
                    str(f'0{round((self.end - self.start) // 60)}:{round((self.end - self.start) % 60)}'))
            else:
                self.label_3.setText(str(f'00:{round(self.end - self.start)}'))
        elif len(str(round((self.end - self.start) // 60))) == 2 and len(str(round((self.end - self.start) % 60))) == 2:
            if self.end - self.start >= 60:
                self.label_3.setText(
                    str(f'{round((self.end - self.start) // 60)}:{round((self.end - self.start) % 60)}'))
            else:
                self.label_3.setText(str(f'00:{round(self.end - self.start)}'))
        self.label_2.setText(str(self.name))
        self.label_4.setText(str(self.food))
        self.label_5.setText(str(round(self.max_score)))
        self.toolButton_3.clicked.connect(self.replay)
        self.toolButton_4.clicked.connect(self.menu)
        name, time, food, score, win = self.label_2.text(), round(
            self.end - self.start), self.label_4.text(), self.label_5.text(), self.win
        self.insert_varible_into_table(name, time, food, score, win)

    def insert_varible_into_table(self, name, time, food, score, win):  # добавление в базу данных
        sqlite_connection = sqlite3.connect('Rating.db')
        cursor = sqlite_connection.cursor()

        sqlite_insert_with_param = """INSERT INTO History
                                      (Name, Time, Food, Score, Win)
                                      VALUES (?, ?, ?, ?, ?);"""

        data_tuple = (name, time, food, score, win)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlite_connection.commit()

        cursor.close()

        if sqlite_connection:
            sqlite_connection.close()

    def replay(self):
        self.play()

    def cancel(self):
        self.hide()

    def menu(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        uic.loadUi('Ui files/start.ui', self)  # Загружаем дизайн
        self.showFullScreen()
        pygame.mixer.music.load("sounds/Фон1.mp3")
        pygame.mixer.music.play(-1)
        self.toolButton.clicked.connect(self.click)
        self.toolButton_2.clicked.connect(self.settings)
        self.toolButton_3.clicked.connect(self.info)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            Start_window.hide()

    def message(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        msg.setWindowTitle('Dimar.io')
        icon = QIcon()
        icon.addFile(u"Application Icons/icon.png", QSize(), QIcon.Normal, QIcon.Off)
        msg.setWindowIcon(icon)
        msg.exec_()

    def play(self):
        uic.loadUi('Ui files/game_over.ui', self) # потом убрать
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        pygame.mixer.music.stop()
        global x, x1, y1, width1, high1, bb, intersection_coordinates, list_of_coordinates, boost, ww, hh, koord, y, z

        class Board:
            def __init__(self, width, height):
                self.width = width
                self.height = height
                self.board = [[0] * width for _ in range(height)]
                self.left = randrange(-4250, width)
                self.top = randrange(-4300, high)
                self.cell_size = 75

            def set_view(self, left, top, cell_size, a, v, b, w, w1, sb):
                # print((left, top, cell_size, a))
                # print()
                # print('----------------------------')
                self.cell_size = cell_size
                for i in range(len(a)):
                    a[i][0] += left
                    a[i][1] += top
                for i in range(len(v)):
                    v[i][0] += left
                    v[i][1] += top
                for i in range(len(b)):
                    b[i][0] += left
                    b[i][1] += top
                for i in range(len(w)):
                    w[i][-2] += left
                    w[i][-1] += top
                for i in range(len(w1)):
                    w1[i][-3] += left
                    w1[i][-2] += top
                for i in range(len(sb)):
                    sb[i][0] += left
                    sb[i][1] += top
                self.left += left
                self.top += top
                if self.left < -1 * self.cell_size * self.width + width or self.left > width:
                    self.left -= left
                    for i in range(len(a)):
                        a[i][0] -= left
                    for i in range(len(v)):
                        v[i][0] -= left
                    for i in range(len(b)):
                        b[i][0] -= left
                    for i in range(len(w)):
                        w[i][-2] -= left
                    for i in range(len(w1)):
                        w1[i][-3] -= left
                    for i in range(len(sb)):
                        sb[i][0] -= left
                if self.top < -1 * self.cell_size * self.width + high or self.top > high:
                    self.top -= top
                    for i in range(len(a)):
                        a[i][1] -= top
                    for i in range(len(v)):
                        v[i][1] -= top
                    for i in range(len(b)):
                        b[i][1] -= top
                    for i in range(len(w)):
                        w[i][-1] -= top
                    for i in range(len(w1)):
                        w1[i][-2] -= top
                    for i in range(len(sb)):
                        sb[i][1] -= top
                return a, v, b, w, w1, sb

            def set_view_2(self, k, s, a, v, b):
                left = self.left - width
                top = self.top - high
                left *= k
                top *= k
                left += width
                top += high
                self.top = top
                self.left = left
                for i in range(len(a)):
                    a[i][0] = (k * (a[i][0] - width)) + width
                    a[i][1] = (k * (a[i][1] - high)) + high
                for i in range(len(v)):
                    v[i][0] = (k * (v[i][0] - width)) + width
                    v[i][1] = (k * (v[i][1] - high)) + high
                for i in range(len(b)):
                    b[i][0] = (k * (b[i][0] - width)) + width
                    b[i][1] = (k * (b[i][1] - high)) + high
                if self.left < width - 100 * size:
                    self.left = width - 100 * size
                elif self.left > width:
                    self.left = width
                if self.top < high - 100 * size:
                    self.top = high - 100 * size
                elif self.top > high:
                    self.top = high
                return a, v, b

            def render(self, screen):
                for y in range(self.height):
                    for x in range(self.width):
                        if -75 < x * self.cell_size + self.left < width * 2 and -75 < y * self.cell_size + self.top < high * 2:
                            pygame.draw.rect(screen, pygame.Color(200, 200, 200), (
                                x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                self.cell_size), 1)

            def move(self):
                return self.left, self.top

        def pointss(s, r):
            return [[randrange(board.move()[0], s * 100 + board.move()[0]),  # создание еды
                     randrange(board.move()[1], s * 100 + board.move()[1]),
                     (randrange(0, 255), randrange(0, 255), randrange(0, 255)), r] for _ in range(3000)]

        def bot(s):
            b = []
            for _ in range(number_of_bots):
                a = randrange(20, 350)
                b.append([randrange(board.move()[0], s * 100 + board.move()[0]),  # создание еды
                          randrange(board.move()[1], s * 100 + board.move()[1]),
                          (choice(COLORS)), True, 12 * 0.997 ** (a - 20), a])
            return b

        def delenie(x, y, z):
            return [x, y, z]

        def rr(r):
            return r

        class Virus:
            def __init__(self, name):
                self.name = name

            def load_image(name):
                fullname = os.path.join('Application Icons', name)
                image = pygame.image.load(fullname)
                image = image.convert_alpha()
                return image

        if __name__ == '__main__':
            self.start = time.monotonic()
            clock = pygame.time.Clock()

            size = width, height = 1550, 810
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            width, high = pygame.display.get_surface().get_size()
            width, high = width // 2, high // 2
            running = True
            board = Board(100, 100)
            sound_shift = pygame.mixer.Sound("Sounds/Shift.ogg")
            sound_w = pygame.mixer.Sound("Sounds/Выстрел W.ogg")
            sound_eat = pygame.mixer.Sound("Sounds/Поедание_планктона.ogg")
            sound_eat_bot = pygame.mixer.Sound("Sounds/Съел_бота.ogg")
            sound_virus = pygame.mixer.Sound("Sounds/Вирус.ogg")
            sound_shift2 = pygame.mixer.Sound("Sounds/Прибавление.ogg")
            sound_time = pygame.mixer.Sound("Sounds/Таймер.ogg")
            sound_baraban = pygame.mixer.Sound("Sounds/барабан.ogg")
            sound_win = pyglet.media.load('Sounds/победа.mp3', streaming=False)
            sound_end = pyglet.media.load('Sounds/Конец.mp3')
            animation_set = [pygame.image.load('Application Icons/3.png'),
                             pygame.image.load('Application Icons/2.png'),
                             pygame.image.load('Application Icons/1.png')]
            animation_counter = 0
            v = 12
            r = 30
            r_points = 10
            i = 0
            m = 1
            counter = 0
            b = False
            bb = False
            viruss = True
            eat_virus = False
            animation = False
            if MODE[0] == 'hide_and_seek':
                animation = True
            plr = []
            self.win = 0
            size = 100
            width1, high1 = 0, 0
            points = pointss(size, r_points)
            del_points = []
            kf = 0
            self.food = 0
            self.max_score = 0
            kff = 20
            shift = False
            number_of_bots = 0
            if MODE[0] == 'hide_and_seek':
                number_of_bots = 2
            else:
                number_of_bots = 30

            if MODE[0] == 'hard':
                number_of_bots = 20
                aaa = False
                bbb = False
            r_v = {}
            move = True
            w = []
            aaa, bbb = True, True
            virus = []
            number_of_viruses = randrange(30, 45)
            image1 = pygame.transform.scale(Virus.load_image("virus.png"), (180, 180))
            del_virus = []
            bots = bot(size)
            del_bots = []
            kf1 = 0
            eaten = 0
            kff1 = 15
            self.score = 0
            del_pointsb = []
            virus_radius = 70
            c = False
            s_im = 180
            w_bots = []
            del_virusb = []
            sbots = []
            del_shift = []
            wr = 22
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            sound_end.play()
                            self.end = time.monotonic()
                            uic.loadUi('Ui files/game_over.ui', self)
                            self.show()
                            # sound_end.play()
                            time.sleep(0.3)
                            self.exit()
                            running = False

                        if event.key == pygame.K_w and r >= 50 and self.score >= 15:
                            sound_w.play()
                            aaaaa = r
                            b = True
                            kff1 = (232 + r) // 11.5
                            koord = delenie(x, y, z)
                            r = sqrt((pi * (r ** 2) - pi * (20 ** 2)) / pi)
                            w.append([koord, kf1, kff1, 22, width, high])
                            self.score -= (aaaaa - r)
                        elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT or event.key == pygame.K_SPACE:
                            if r >= 40 and not shift:
                                sound_shift.play()
                                self.score /= 2
                                koord = delenie(x, y, z)
                                shift = True
                                r /= 2

                            # v = r_v[int(r)]
                            r1 = rr(r)
                    if event.type == pygame.MOUSEMOTION:
                        x, y = event.pos
                        x1, y1 = x, y
                        x -= width
                        y -= high
                        z = sqrt(x ** 2 + y ** 2)
                    del_points = []
                if len(points) < 3000:
                    points.append([randrange(int(board.move()[0]), int(size * 100 + board.move()[0])),
                                   randrange(int(board.move()[1]), int(size * 100 + board.move()[1])),
                                   (randrange(0, 255), randrange(0, 255), randrange(0, 255)), r_points])
                if (x > 50 or x < -50) or (y > 50 or y < -50):
                    move = False
                    if not animation:
                        points, virus, bots, w, w_bots, sbots = board.set_view(0 - (x / z) * v, 0 - (y / z) * v, size,
                                                                               points, virus, bots, w, w_bots, sbots)
                    width1 -= (x / z) * v
                    high1 -= (y / z) * v

                for i in range(len(virus)):
                    if (width - r < virus[i][0] < width + r and high - r < virus[i][1] < high + r) and r >= virus[i][
                        -1]:
                        sound_virus.play()
                        del_virus.append(virus[i])
                        virus[i][-3] = False
                        virus.append([randrange(int(board.move()[0]), int(size * 100 + board.move()[0])),
                                      randrange(int(board.move()[1]), int(size * 100 + board.move()[1])), (0, 0, 0),
                                      True, True, 70])
                        r *= 0.35
                        v /= 0.93
                        self.score *= 0.35
                        for i in range(randrange(20, 30)):
                            w.append(
                                [delenie(randrange(-20, 20), randrange(-20, 20),
                                         sqrt(randrange(-20, 20) ** 2 + randrange(-20, 20) ** 2)), 0,
                                 (232 + r) // 15.47, 22, width, high])
                        b = True
                for i in range(len(points)):
                    if (width - r < points[i][0] < width + r and high - r < points[i][1] < high + r) and r >= points[i][
                        -1]:
                        sound_eat.set_volume(0.2)
                        sound_eat.play()
                        del_points.append(points[i])
                        self.score += points[i][-1] / 20
                for i in range(len(bots)):
                    if (width - r < bots[i][0] < width + r and high - r < bots[i][1] < high + r) and abs(
                            width - bots[i][0]) < 0.5 * r and abs(high - bots[i][1]) < 0.5 * r and r > bots[i][
                        -1] * 1.05:
                        sound_eat_bot.play()
                        eaten += 1
                        del_bots.append(bots[i])
                        self.score += bots[i][-1] / 20

                    elif r * 1.05 < bots[i][-1] and bots[i][0] - bots[i][-1] < width < bots[i][0] + bots[i][-1] and \
                            bots[i][1] - bots[i][-1] < high < bots[i][1] + bots[i][-1] and abs(
                        bots[i][0] - width) < 0.5 * bots[i][-1] and abs(bots[i][1] - high) < 0.5 * bots[i][-1]:
                        self.end = time.monotonic()
                        sound_end.play()
                        uic.loadUi('Ui files/game_over.ui', self)
                        self.show()
                        time.sleep(0.2)
                        self.exit()
                        running = False

                for i in del_points:
                    if r >= 150:
                        if size > 40:
                            size *= (pi * (r ** 2)) * 1.001 / ((pi * (r ** 2)) + (pi * (i[-1] ** 2)))
                            r_points *= size / (
                                    size / ((pi * (r ** 2)) * 1.001 / ((pi * (r ** 2)) + (pi * (i[-1] ** 2)))))
                            k = size / (size / ((pi * (r ** 2)) * 1.001 / ((pi * (r ** 2)) + (pi * (i[-1] ** 2)))))

                            v *= (pi * (r ** 2)) * 1.001 / ((pi * (r ** 2)) + (pi * (i[-1] ** 2)))
                        else:
                            size *= 0.999
                            r_points *= 0.999
                            k = 0.999
                            v *= 0.999
                        s_im *= k
                        wr *= k
                        image1 = pygame.transform.scale(Virus.load_image("virus.png"), (int(s_im), int(s_im)))
                        points, virus, bots = board.set_view_2(k, size, points, virus, bots)
                        virus_radius *= k

                        for h in range(len(bots)):
                            bots[h][-1] *= k
                        for g in range(len(points)):
                            if 0 < points[g][0] < width * 2 and 0 < points[g][1] < high * 2:
                                pygame.draw.circle(screen, points[g][2][0], (points[g][0], points[g][1]), r_points)
                    elif r < 150:
                        r = sqrt(((pi * (r ** 2)) + (pi * (i[-1] ** 2))) / pi)
                        # virus_radius *= k
                        v *= 0.999

                    try:
                        del points[points.index(i)]
                    except Exception as e:
                        pass
                self.food += len(del_points)
                del_points = []

                for i in del_virus:

                    try:
                        del virus[virus.index(i)]
                    except Exception as e:
                        pass
                del_virus = []
                for i in del_bots:
                    if r >= 150:
                        size *= (pi * (r ** 2)) * 1.001 / ((pi * (r ** 2)) + (pi * (i[-1] ** 2))) * 1.1
                        r_points *= size / (size / ((pi * (r ** 2)) * 1.001 / ((pi * (r ** 2)) + (pi * (i[-1] ** 2)))))
                        k = size / (size / ((pi * (r ** 2)) * 1.001 / ((pi * (r ** 2)) + (pi * (i[-1] ** 2)))))
                        points, virus, bots = board.set_view_2(k, size, points, virus, bots)
                        v *= (pi * (r ** 2)) / ((pi * (r ** 2)) + (pi * (i[-1] ** 2)))
                        wr *= k
                        s_im *= k
                        for h in range(len(bots)):
                            bots[h][-1] *= size / (
                                    size / ((pi * (r ** 2)) * 1.001 / ((pi * (r ** 2)) + (pi * (i[-1] ** 2)))))
                    elif r < 150:
                        # virus_radius *= k
                        v *= 0.999
                        r = sqrt(((pi * (r ** 2)) + (pi * (i[-1] ** 2))) / pi)


                    try:
                        del bots[bots.index(i)]
                    except Exception as e:
                        pass
                del_bots = []
                screen.fill((235, 235, 235))
                board.render(screen)
                try:
                    for i in range(len(points)):
                        if points[i][-1] == 22:  # TODO отнимать от points[i][2] 55
                            pygame.draw.circle(screen, COLOR[0][1], (points[i][0], points[i][1]), wr + 1)
                            pygame.draw.circle(screen, COLOR[0][0], (points[i][0], points[i][1]), wr - 4)
                        elif points[i][-1] == 23:
                            pygame.draw.circle(screen, points[i][2][1], (points[i][0], points[i][1]), wr)
                            pygame.draw.circle(screen, points[i][2][0], (points[i][0], points[i][1]), wr - 4)
                        else:
                            if len(points[i][2]) == 2:
                                pygame.draw.circle(screen, points[i][2][1], (points[i][0], points[i][1]), wr + 1)
                                pygame.draw.circle(screen, points[i][2][0], (points[i][0], points[i][1]), wr - 4)
                            else:
                                pygame.draw.circle(screen, points[i][2], (points[i][0], points[i][1]), r_points)

                except:
                    print(points[i][2])
                    running = False
                    pass
                for i in range(len(virus)):
                    if points[i][-1] == virus_radius:
                        pygame.draw.circle(screen, (0, 0, 0), (points[i][0] + 75, points[i][1] + 75), virus_radius)
                try:
                    if b:
                        l, t = board.move()
                        for i in w:
                            if i[1] < 1000000 and i[2] > 0:  # 0
                                # pygame.draw.circle(screen, (200, 0, 0),
                                #                ((i[0][0] / i[0][2]) * i[1] + width, i[0][1] / i[0][2] * i[1] + high),
                                #                26)
                                pygame.draw.circle(screen, (COLOR[0][1]),
                                                   ((i[0][0] / i[0][2]) * i[1] + i[-2],
                                                    i[0][1] / i[0][2] * i[1] + i[-1]),
                                                   wr + 1)
                                pygame.draw.circle(screen, (COLOR[0][0]),
                                                   ((i[0][0] / i[0][2]) * i[1] + i[-2],
                                                    i[0][1] / i[0][2] * i[1] + i[-1]),
                                                   wr - 4)
                                i[1] += i[2]
                                if (i[0][0] / i[0][2]) * i[1] + i[-2] > l + size * 100:
                                    i[0][0] = i[0][2] * (l + size * 100 - i[-2]) / i[1]
                                elif (i[0][0] / i[0][2]) * i[1] + i[-2] < l:
                                    i[0][0] = i[0][2] * (l - i[-2]) / i[1]
                                if i[0][1] / i[0][2] * i[1] + i[-1] > t + size * 100:
                                    i[0][1] = i[0][2] * (t + size * 100 - i[-1]) / i[1]
                                elif i[0][1] / i[0][2] * i[1] + i[-1] < t:
                                    i[0][1] = i[0][2] * (t - i[-1]) / i[1]

                                i[2] -= 0.5
                            else:
                                i[1] = 0
                                i[2] = 15

                            if i[2] == 0:
                                points.append(
                                    [(i[0][0] / i[0][2]) * i[1] + i[-2], i[0][1] / i[0][2] * i[1] + i[-1],
                                     (COLOR[0][0]),
                                     False, 22])
                                del w[w.index(i)]

                except ZeroDivisionError:
                    pass

                try:
                    if c:
                        l, t = board.move()
                        for i in w_bots:
                            if i[1] < 1000000 and i[2] > 0:  # 0
                                # pygame.draw.circle(screen, i[-1],
                                #                ((i[0][0] / i[0][2]) * i[1] + width, i[0][1] / i[0][2] * i[1] + high),
                                #                26)
                                pygame.draw.circle(screen, i[-1][1],
                                                   ((i[0][0] / i[0][2]) * i[1] + i[-3],
                                                    i[0][1] / i[0][2] * i[1] + i[-2]),
                                                   wr)
                                pygame.draw.circle(screen, i[-1][0],
                                                   ((i[0][0] / i[0][2]) * i[1] + i[-3],
                                                    i[0][1] / i[0][2] * i[1] + i[-2]),
                                                   wr - 4)
                                i[1] += i[2]
                                if (i[0][0] / i[0][2]) * i[1] + i[-3] > l + size * 100:
                                    i[0][0] = i[0][2] * (l + size * 100 - i[-3]) / i[1]
                                elif (i[0][0] / i[0][2]) * i[1] + i[-3] < l:
                                    i[0][0] = i[0][2] * (l - i[-3]) / i[1]
                                if i[0][1] / i[0][2] * i[1] + i[-2] > t + size * 100:
                                    i[0][1] = i[0][2] * (t + size * 100 - i[-2]) / i[1]
                                elif i[0][1] / i[0][2] * i[1] + i[-2] < t:
                                    i[0][1] = i[0][2] * (t - i[-2]) / i[1]

                                i[2] -= 0.5
                            else:
                                i[1] = 0
                                i[2] = 15

                            if i[2] == 0:
                                points.append(
                                    [(i[0][0] / i[0][2]) * i[1] + i[-3], i[0][1] / i[0][2] * i[1] + i[-2], i[-1],
                                     False, i[-4]])
                                del w_bots[w_bots.index(i)]

                except ZeroDivisionError:
                    pass

                if shift:
                    l, t = board.move()
                    r2 = r1
                    if kf < 700 and kff > -20.5:  # 0

                        for i in range(len(points)):
                            if (koord[0] / koord[2]) * kf + width - r2 < points[i][0] < (
                                    koord[0] / koord[2]) * kf + width + r2 and koord[1] / koord[2] * kf + high - r2 < \
                                    points[i][1] < koord[1] / koord[2] * kf + high + r2:
                                del_points.append(points[i])
                                sound_eat.set_volume(0.2)
                                sound_eat.play()
                                self.score += points[i][-1] / 20
                        for i in del_points:

                            r2 += (sqrt(((pi * (r2 ** 2)) + (pi * (i[-1] ** 2))) / pi) - r2) / 2
                            try:
                                del points[points.index(i)]
                            except:
                                pass
                        self.food += len(del_points)

                        for i in range(len(virus)):
                            if (koord[0] / koord[2]) * kf + width - r2 < virus[i][0] < (
                                    koord[0] / koord[2]) * kf + width + r2 and koord[1] / koord[2] * kf + high - r2 < \
                                    virus[i][1] < koord[1] / koord[2] * kf + high + r2:
                                del_virus.append(virus[i])
                                virus[i][-3] = False
                                virus.append([randrange(int(board.move()[0]), int(size * 100 + board.move()[0])),
                                              randrange(int(board.move()[1]), int(size * 100 + board.move()[1])),
                                              (0, 0, 0),
                                              True, True, 70])
                                r *= 0.35
                                v /= 0.85
                                self.score *= 0.35
                                for i in range(randrange(20, 30)):
                                    w.append(
                                        [delenie(randrange(-20, 20), randrange(-20, 20),
                                                 sqrt(randrange(-20, 20) ** 2 + randrange(-20, 20) ** 2)), 0,
                                         (232 + r) // 15.47, width, high])
                                b = True
                        for i in del_virus:
                            r2 += (sqrt(((pi * (r2 ** 2)) + (pi * (i[-1] ** 2))) / pi) - r2) / 2
                            try:
                                del virus[virus.index(i)]
                            except:
                                pass
                        for i in range(len(bots)):
                            if (koord[0] / koord[2]) * kf + width - r2 < bots[i][0] < (
                                    koord[0] / koord[2]) * kf + width + r2 and koord[1] / koord[2] * kf + high - r2 < \
                                    bots[i][1] < koord[1] / koord[2] * kf + high + r2 and r2 > bots[i][-1] * 1.05 and \
                                    abs((koord[0] / koord[2]) * kf + width - bots[i][0]) < 0.5 * r2 and abs(
                                koord[1] / koord[2] * kf + high - bots[i][1]) < 0.5 * r2:
                                del_bots.append(bots[i])
                                self.score += bots[i][-1] / 20
                        for i in del_bots:
                            r2 += (sqrt(((pi * (r2 ** 2)) + (pi * (i[-1] ** 2))) / pi) - r2) / 4
                            try:
                                del bots[bots.index(i)]
                            except:
                                pass

                        if (koord[0] / koord[2]) * kf + width > l + size * 100:
                            koord[0] = koord[2] * (l + size * 100 - width) / kf
                        elif (koord[0] / koord[2]) * kf + width < l:
                            koord[0] = koord[2] * (l - width) / kf
                        if koord[1] / koord[2] * kf + high > t + size * 100:
                            koord[1] = koord[2] * (t + size * 100 - high) / kf
                        elif koord[1] / koord[2] * kf + high < t:
                            koord[1] = koord[2] * (t - high) / kf
                        pygame.draw.circle(screen, COLOR[0][1],
                                           ((koord[0] / koord[2]) * kf + width, koord[1] / koord[2] * kf + high),
                                           r2 + 5)
                        pygame.draw.circle(screen, COLOR[0][0],
                                           ((koord[0] / koord[2]) * kf + width, koord[1] / koord[2] * kf + high), r2)
                        if kff == -8.5:
                            sound_shift2.play()
                        kf += kff
                        kff -= 0.5
                    else:
                        shift = False
                        self.score *= 2
                        kf = 0
                        kff = 20
                        r += r2

                if r >= virus_radius:
                    eat_virus = True
                    for i in virus:
                        if i[-3]:
                            screen.blit(image1, (i[0], i[1]))

                if viruss:
                    for i in range(number_of_viruses):
                        virus.append([randrange(int(board.move()[0]), int(size * 100 + board.move()[0])),
                                      randrange(int(board.move()[1]), int(size * 100 + board.move()[1])), (0, 0, 0),
                                      True, True, virus_radius])
                        viruss = False

                for u in range(len(bots)):
                    if 0 < bots[u][0] + bots[u][-1] and bots[u][0] - bots[u][-1] < width * 2 and 0 < bots[u][1] + \
                            bots[u][-1] and bots[u][1] - bots[u][-1] < high * 2 and bots[u][-1] <= r:
                        for i in range(len(points)):
                            if (bots[u][0] - bots[u][-1] < points[i][0] < bots[u][0] + bots[u][-1] and bots[u][1] -
                                bots[u][-1] < points[i][1] < bots[u][1] + r) and bots[u][-1] >= \
                                    points[i][-1]:
                                del_pointsb.append(points[i])
                        for i in del_pointsb:
                            bots[u][-1] = sqrt(((pi * (bots[u][-1] ** 2)) + (pi * (i[-1] ** 2))) / pi)
                            bots[u][-2] *= 0.997
                            del points[points.index(i)]
                        for i in range(len(virus)):
                            if (bots[u][0] - bots[u][-1] < virus[i][0] < bots[u][0] + bots[u][-1] and bots[u][1] -
                                bots[u][-1] < virus[i][1] < bots[u][1] + r) and bots[u][-1] >= \
                                    virus[i][-1]:
                                del_virusb.append(virus[i])
                                virus[i][-3] = False
                                virus.append([randrange(int(board.move()[0]), int(size * 100 + board.move()[0])),
                                              randrange(int(board.move()[1]), int(size * 100 + board.move()[1])),
                                              (0, 0, 0),
                                              True, True, 70])
                                bots[u][-1] *= 0.35
                                bots[u][-2] /= 0.95
                                for i in range(randrange(20, 30)):
                                    w_bots.append(
                                        [delenie(randrange(-20, 20), randrange(-20, 20),
                                                 sqrt(randrange(-20, 20) ** 2 + randrange(-20, 20) ** 2)), 0,
                                         (232 + r) // 15.47, 23, bots[u][0], bots[u][1], bots[u][2]])
                                c = True
                        for i in del_virusb:

                            try:
                                del virus[virus.index(i)]
                            except Exception as e:
                                pass
                        for i in range(len(bots)):
                            aaa = False
                            bbb = False
                            if 0 < bots[u][0] + bots[i][-1] and bots[i][0] - bots[i][-1] < width * 2 and 0 < bots[i][
                                1] + \
                                    bots[i][-1] and bots[i][1] - bots[i][-1] < high * 2 and i != u and bots[u][-1] < \
                                    bots[i][-1]:
                                bbb = True
                                break
                            elif 0 < bots[u][0] + bots[i][-1] and bots[i][0] - bots[i][-1] < width * 2 and 0 < bots[i][
                                1] + \
                                    bots[i][-1] and bots[i][1] - bots[i][-1] < high * 2 and i != u and bots[u][-1] > \
                                    bots[i][-1]:
                                aaa = True
                                break
                        for g in range(len(bots)):
                            if (bots[u][0] - bots[u][-1] < bots[g][0] < bots[u][0] + bots[u][-1] and bots[u][1] -
                                bots[u][-1] < bots[g][1] < bots[u][1] + bots[u][-1]) and abs(
                                bots[u][0] - bots[g][0]) < 0.5 * bots[u][-1] and abs(
                                bots[u][1] - bots[g][1]) < 0.5 * bots[u][-1] and bots[u][-1] > bots[g][
                                -1] * 1.05 and u != g:
                                del_bots.append(g)
                                bots[u][-1] = sqrt(((pi * (bots[u][-1] ** 2)) + (pi * (bots[g][-1] ** 2))) / pi)
                                bots[u][-2] *= 0.997

                        try:
                            if aaa:
                                z1 = sqrt(abs(bots[u][0] - bots[i][0]) ** 2 + abs(bots[u][1] - bots[i][1]) ** 2)
                                bots[u][0] += ((abs(bots[u][0] - bots[i][0]) / z1) * bots[u][-2]) * (
                                        bots[i][0] - bots[u][0]) / abs(
                                    bots[i][0] - bots[u][0]) * 1
                                bots[u][1] += ((abs(bots[u][1] - bots[i][1]) / z1) * bots[u][-2]) * (
                                        bots[i][1] - bots[u][1]) / abs(
                                    bots[i][1] - bots[u][1]) * 1
                            elif bbb:
                                z1 = sqrt(abs(bots[u][0] - bots[i][0]) ** 2 + abs(bots[u][1] - bots[i][1]) ** 2)
                                bots[u][0] += ((abs(bots[u][0] - bots[i][0]) / z1) * bots[u][-2]) * (
                                        bots[i][0] - bots[u][0]) / abs(
                                    bots[i][0] - bots[u][0]) * -1
                                bots[u][1] += ((abs(bots[u][1] - bots[i][1]) / z1) * bots[u][-2]) * (
                                        bots[i][1] - bots[u][1]) / abs(
                                    bots[i][1] - bots[u][1]) * -1
                            else:
                                z1 = sqrt(abs(bots[u][0] - width) ** 2 + abs(bots[u][1] - high) ** 2)
                                bots[u][0] += ((abs(bots[u][0] - width) / z1) * bots[u][-2]) * (
                                        width - bots[u][0]) / abs(
                                    width - bots[u][0]) * -1
                                bots[u][1] += ((abs(bots[u][1] - high) / z1) * bots[u][-2]) * (high - bots[u][1]) / abs(
                                    high - bots[u][1]) * -1



                        except:
                            pass
                        del_virusb = []
                        pygame.draw.circle(screen, bots[u][2][1], (bots[u][0], bots[u][1]), bots[u][-1] + 6)
                        pygame.draw.circle(screen, bots[u][2][0], (bots[u][0], bots[u][1]), bots[u][-1])
                        del_pointsb = []
                        l, t = board.move()
                        if l + size * 100 < bots[u][0]:
                            bots[u][0] = l + size * 100
                        elif bots[u][0] < l:
                            bots[u][0] = l
                        if t + size * 100 < bots[u][1]:
                            bots[u][1] = t + size * 100
                        elif bots[u][1] < t:
                            bots[u][1] = t
                        if sqrt(abs((high - bots[u][1]) ** 2 + (width - bots[u][0]) ** 2)) < 700 and bots[u][-3] and \
                                bots[u][-1] / 2 == r * 0.98:
                            sbots.append(
                                [bots[u][0], bots[u][1], bots[u][2], 1.6, u, bots[u][-2] * 1.2, bots[u][-1] / 2])
                            bots[u][-1] /= 2
                            flagb = True
                            bots[u][-3] = False
                    elif r >= bots[u][-1]:
                        bots[u][-3] = True

                if self.score > self.max_score:
                    self.max_score = self.score

                if len(bots) == 0:
                    self.end = time.monotonic()
                    sound_win.play()
                    uic.loadUi('Ui files/win.ui', self)
                    self.show()
                    self.win = 1
                    time.sleep(0.3)
                    self.exit()
                    running = False

                pygame.draw.circle(screen, COLOR[0][1], (width, high), r + 5)
                pygame.draw.circle(screen, COLOR[0][0], (width, high), r)

                text = pygame.font.Font('Bubbleboddy-Neue-trial.ttf', int(r // 2.5)).render(self.name, True,
                                                                                            [255, 255, 255])
                text1 = pygame.font.Font('Bubbleboddy-Neue-trial.ttf', int(r // 3.5)).render(str(round(self.score)),
                                                                                             True,
                                                                                             [255, 255, 255])
                screen.blit(text, (width - (int(len(self.name) * int(r // 5.2))) // 2, high - int(r // 2.2)))
                screen.blit(text1, (width - (int(len(self.name) * int(r // 19))) // 2, high - int(r // 30)))
                del_bots = []
                for u in range(len(bots)):
                    aaa = False
                    bbb = False
                    if 0 < bots[u][0] + bots[u][-1] and bots[u][0] - bots[u][-1] < width * 2 and 0 < bots[u][1] + \
                            bots[u][-1] and bots[u][1] - bots[u][-1] < high * 2 and bots[u][-1] > r:
                        for i in range(len(points)):
                            if (bots[u][0] - bots[u][-1] < points[i][0] < bots[u][0] + bots[u][-1] and bots[u][1] -
                                bots[u][-1] < points[i][1] < bots[u][1] + r) and bots[u][-1] >= \
                                    points[i][-1]:
                                del_pointsb.append(points[i])
                        for i in del_pointsb:
                            bots[u][-1] = sqrt(((pi * (bots[u][-1] ** 2)) + (pi * (i[-1] ** 2))) / pi)
                            bots[u][-2] *= 0.997
                            del points[points.index(i)]
                        for i in range(len(virus)):
                            if (bots[u][0] - bots[u][-1] < virus[i][0] < bots[u][0] + bots[u][-1] and bots[u][1] -
                                bots[u][-1] < virus[i][1] < bots[u][1] + r) and bots[u][-1] >= \
                                    virus[i][-1]:
                                del_virusb.append(virus[i])
                                virus[i][-3] = False
                                virus.append([randrange(int(board.move()[0]), int(size * 100 + board.move()[0])),
                                              randrange(int(board.move()[1]), int(size * 100 + board.move()[1])),
                                              (0, 0, 0),
                                              True, True, 70])
                                bots[u][-1] *= 0.35
                                bots[u][-2] /= 0.95
                                for i in range(randrange(20, 30)):
                                    w_bots.append(
                                        [delenie(randrange(-20, 20), randrange(-20, 20),
                                                 sqrt(randrange(-20, 20) ** 2 + randrange(-20, 20) ** 2)), 0,
                                         (232 + r) // 15.47, 23, bots[u][0], bots[u][1], bots[u][2]])
                                c = True
                        for i in del_virusb:
                            try:
                                del virus[virus.index(i)]
                            except Exception as e:
                                pass
                        del_virusb = []
                        for i in range(len(bots)):
                            if 0 < bots[u][0] + bots[i][-1] and bots[i][0] - bots[i][-1] < width * 2 and 0 < bots[i][
                                1] + \
                                    bots[i][-1] and bots[i][1] - bots[i][-1] < high * 2 and i != u and bots[u][-1] < \
                                    bots[i][-1]:
                                bbb = True
                                break
                            elif 0 < bots[u][0] + bots[i][-1] and bots[i][0] - bots[i][-1] < width * 2 and 0 < bots[i][
                                1] + \
                                    bots[i][-1] and bots[i][1] - bots[i][-1] < high * 2 and i != u and bots[u][-1] > \
                                    bots[i][-1] and r < bots[i][-1]:
                                aaa = True
                                break

                        for g in range(len(bots)):
                            if (bots[u][0] - bots[u][-1] < bots[g][0] < bots[u][0] + bots[u][-1] and bots[u][1] -
                                bots[u][-1] < bots[g][1] < bots[u][1] + bots[u][-1]) and abs(
                                bots[u][0] - bots[g][0]) < 0.5 * bots[u][-1] and abs(
                                bots[u][1] - bots[g][1]) < 0.5 * bots[u][-1] and bots[u][-1] > bots[g][
                                -1] * 1.05 and u != g:
                                del_bots.append(g)
                                bots[u][-1] = sqrt(((pi * (bots[u][-1] ** 2)) + (pi * (bots[g][-1] ** 2))) / pi)
                                bots[u][-2] *= 0.995

                            # elif bots[u][-1] * 1.05 < bots[g][-1] and bots[g][0] - bots[g][-1] < bots[u][0] < bots[g][0] + bots[g][
                            #     -1] and \
                            #         bots[g][1] - bots[g][-1] < bots[u][1] < bots[g][1] + bots[g][-1] and abs(
                            #     bots[g][0] - bots[u][0]) < 0.5 * bots[g][-1] and abs(bots[g][1] - bots[u][1]) < 0.5 * bots[g][-1]:
                            #     del_bots.append(u)
                            #     bots[g][-1] = sqrt(((pi * (bots[g][-1] ** 2)) + (pi * (bots[u][-1] ** 2))) / pi)
                            #     bots[g][-2] *= 0.997

                        try:
                            if MODE[0] == 'hard':
                                aaa = bbb = False
                            if aaa:
                                z1 = sqrt(abs(bots[u][0] - bots[i][0]) ** 2 + abs(bots[u][1] - bots[i][1]) ** 2)
                                bots[u][0] += ((abs(bots[u][0] - bots[i][0]) / z1) * bots[u][-2]) * (
                                        bots[i][0] - bots[u][0]) / abs(
                                    bots[i][0] - bots[u][0]) * 1
                                bots[u][1] += ((abs(bots[u][1] - bots[i][1]) / z1) * bots[u][-2]) * (
                                        bots[i][1] - bots[u][1]) / abs(
                                    bots[i][1] - bots[u][1]) * 1
                            elif bbb:
                                z1 = sqrt(abs(bots[u][0] - bots[i][0]) ** 2 + abs(bots[u][1] - bots[i][1]) ** 2)
                                bots[u][0] += ((abs(bots[u][0] - bots[i][0]) / z1) * bots[u][-2]) * (
                                        bots[i][0] - bots[u][0]) / abs(
                                    bots[i][0] - bots[u][0]) * -1
                                bots[u][1] += ((abs(bots[u][1] - bots[i][1]) / z1) * bots[u][-2]) * (
                                        bots[i][1] - bots[u][1]) / abs(
                                    bots[i][1] - bots[u][1]) * -1
                            else:
                                z1 = sqrt(abs(bots[u][0] - width) ** 2 + abs(bots[u][1] - high) ** 2)
                                bots[u][0] += ((abs(bots[u][0] - width) / z1) * bots[u][-2]) * (
                                        width - bots[u][0]) / abs(
                                    width - bots[u][0]) * 1
                                bots[u][1] += ((abs(bots[u][1] - high) / z1) * bots[u][-2]) * (high - bots[u][1]) / abs(
                                    high - bots[u][1]) * 1



                        except:
                            pass
                        pygame.draw.circle(screen, bots[u][2][1], (bots[u][0], bots[u][1]), bots[u][-1] + 6)
                        pygame.draw.circle(screen, bots[u][2][0], (bots[u][0], bots[u][1]), bots[u][-1])
                        del_pointsb = []
                        l, t = board.move()
                        if l + size * 100 < bots[u][0]:
                            bots[u][0] = l + size * 100
                        elif bots[u][0] < l:
                            bots[u][0] = l
                        if t + size * 100 < bots[u][1]:
                            bots[u][1] = t + size * 100
                        elif bots[u][1] < t:
                            bots[u][1] = t
                        if sqrt(abs((high - bots[u][1]) ** 2 + (width - bots[u][0]) ** 2)) < 500 and bots[u][-3] and \
                                bots[u][-1] / 2 > r * 1.3:
                            if not aaa and not bbb:
                                sbots.append(
                                    [bots[u][0], bots[u][1], bots[u][2], 1.6, u, bots[u][-2] * 1.2, bots[u][-1] / 2])
                                bots[u][-1] /= 2
                                flagb = True
                                bots[u][-3] = False
                    elif r < bots[u][-1]:
                        bots[u][-3] = True
                try:
                    for g in del_bots:
                        del bots[g]
                except:
                    pass
                del_bots = []

                try:
                    for u in range(len(sbots)):
                        www = False
                        for i in range(len(points)):
                            if (sbots[u][0] - sbots[u][-1] < points[i][0] < sbots[u][0] + sbots[u][-1] and sbots[u][
                                1] -
                                sbots[u][-1] < points[i][1] < sbots[u][1] + r) \
                                    and sbots[u][-1] >= \
                                    points[i][-1]:
                                del_pointsb.append(points[i])
                        for i in del_pointsb:
                            sbots[u][-1] = sqrt(((pi * (sbots[u][-1] ** 2)) + (pi * (i[-1] ** 2))) / pi)
                            sbots[u][-2] *= 0.997
                            del points[points.index(i)]
                        for i in range(len(virus)):
                            if (sbots[u][0] - sbots[u][-1] < virus[i][0] < sbots[u][0] + sbots[u][-1] and sbots[u][
                                1] -
                                sbots[u][-1] < virus[i][1] < sbots[u][1] + r) and sbots[u][-1] >= \
                                    virus[i][-1]:
                                del_virusb.append(virus[i])
                                virus[i][-3] = False
                                virus.append([randrange(int(board.move()[0]), int(size * 100 + board.move()[0])),
                                              randrange(int(board.move()[1]), int(size * 100 + board.move()[1])),
                                              (0, 0, 0),
                                              True, True, 70])
                                sbots[u][-1] *= 0.35
                                sbots[u][-2] /= 0.95
                                for i in range(randrange(20, 30)):
                                    w_bots.append(
                                        [delenie(randrange(-20, 20), randrange(-20, 20),
                                                 sqrt(randrange(-20, 20) ** 2 + randrange(-20, 20) ** 2)), 0,
                                         (232 + r) // 15.47, 23, sbots[u][0], sbots[u][1], sbots[u][2]])
                                c = True
                        for i in del_virusb:
                            try:
                                del virus[virus.index(i)]
                            except Exception as e:
                                pass
                        del_virusb = []
                        pygame.draw.circle(screen, sbots[u][2][1], (sbots[u][0], sbots[u][1]), sbots[u][-1] + 6)
                        pygame.draw.circle(screen, sbots[u][2][0], (sbots[u][0], sbots[u][1]), sbots[u][-1])
                        del_pointsb = []

                        if sbots[u][3] > 1:
                            z4 = sqrt(abs(sbots[u][0] - width) ** 2 + abs(sbots[u][1] - high) ** 2)
                            if sbots[u][-1] > r:
                                sbots[u][0] += ((abs(sbots[u][0] - width) / z4) * sbots[u][-2] * sbots[u][3]) * (
                                    width - sbots[u][0]) / abs(
                                width - sbots[u][0])
                                sbots[u][1] += ((abs(sbots[u][1] - high) / z4) * sbots[u][-2] * sbots[u][3]) * (
                                    high - sbots[u][1]) / abs(
                                high - sbots[u][1])
                            else:
                                z4 = sqrt(abs(sbots[u][0] - bots[sbots[u][4]][0]) ** 2 + abs(
                                    sbots[u][1] - bots[sbots[u][4]][1]) ** 2)
                                sbots[u][0] += ((abs(sbots[u][0] - bots[sbots[u][4]][0]) / z4) * sbots[u][-2]) * 3.7 * (
                                        bots[sbots[u][4]][0] - sbots[u][0]) / abs(
                                    sbots[u][4] - sbots[u][0])
                                sbots[u][1] += ((abs(sbots[u][1] - bots[sbots[u][4]][1]) / z4) * sbots[u][-2] * 3.7) * (
                                        bots[sbots[u][4]][1] - sbots[u][1]) / abs(
                                    sbots[u][5] - sbots[u][1])
                        else:
                            z4 = sqrt(abs(sbots[u][0] - bots[sbots[u][4]][0]) ** 2 + abs(
                                sbots[u][1] - bots[sbots[u][4]][1]) ** 2)
                            sbots[u][0] += ((abs(sbots[u][0] - bots[sbots[u][4]][0]) / z4) * sbots[u][-2]) * 3.7 * (
                                    bots[sbots[u][4]][0] - sbots[u][0]) / abs(
                                sbots[u][4] - sbots[u][0])
                            sbots[u][1] += ((abs(sbots[u][1] - bots[sbots[u][4]][1]) / z4) * sbots[u][-2] * 3.7) * (
                                    bots[sbots[u][4]][1] - sbots[u][1]) / abs(
                                sbots[u][5] - sbots[u][1])
                        l, t = board.move()
                        if l + size * 100 < sbots[u][0]:
                            sbots[u][0] = l + size * 100
                        elif sbots[u][0] < l:
                            sbots[u][0] = l
                        if t + size * 100 < sbots[u][1]:
                            sbots[u][1] = t + size * 100
                        elif sbots[u][1] < t:
                            sbots[u][1] = t
                        if sbots[u][3] > 0:
                            sbots[u][3] -= 0.005
                        if bots[sbots[u][4]][0] - bots[sbots[u][4]][-1] < sbots[u][0] < bots[sbots[u][4]][0] + \
                                bots[sbots[u][4]][-1] and \
                                bots[sbots[u][4]][1] - bots[sbots[u][4]][-1] < sbots[u][1] < bots[sbots[u][4]][1] + \
                                bots[sbots[u][4]][-1] and sbots[u][3] < 1:
                            del_shift.append(u)
                        if width - r < sbots[u][0] < width + r and \
                                high - r < sbots[u][1] < high + \
                                r and r > sbots[u][-1]:
                            r = sqrt(((pi * (r ** 2)) + (pi * (sbots[u][-1] ** 2))) / pi)
                            v *= 0.997
                            self.score += sbots[u][-1] / 20
                            del_shift.append(u)
                            www = True
                        elif r * 1.02 < sbots[u][-1] and sbots[u][0] - sbots[u][-1] < width < sbots[u][0] + sbots[u][
                            -1] and sbots[u][1] - sbots[u][-1] < high < sbots[u][1] + sbots[u][-1] and abs(
                            sbots[u][0] - width) < 0.5 * sbots[u][-1] and abs(sbots[u][1] - high) < 0.5 * sbots[u][
                            -1]:
                            self.end = time.monotonic()
                            sound_end.play()
                            uic.loadUi('Ui files/game_over.ui', self)
                            self.show()
                            time.sleep(0.2)
                            self.exit()
                            running = False
                        for g in range(len(bots)):
                            if bots[sbots[u][4]][0] - bots[g][-1] < sbots[u][0] < width + r and \
                                    bots[g][1] - bots[g][-1] < sbots[u][1] < bots[g][1] + \
                                    bots[g][-1] and sbots[u][3] < 1 and sbots[u][4] != g:
                                sbots[u][-1] = sqrt(((pi * (sbots[u][-1] ** 2)) + (pi * (bots[g][-1] ** 2))) / pi)
                                del_bots.append(g)
                    for i in del_shift:
                        if not www:
                            bots[sbots[i][4]][-1] += sbots[i][-1]
                        del sbots[i]
                    for i in del_bots:
                        del bots[i]
                    del_bots = []
                    del_shift = []

                except:
                    pass

                if r < virus_radius:
                    for i in virus:
                        if i[-2] and i[-3]:
                            screen.blit(image1, (i[0], i[1]))

                if MODE[0] == 'normal':
                    counter += 1
                    if counter < 180:
                        text = pygame.font.Font('Bubbleboddy-Neue-trial.ttf', 40).render('Standart mod:', True,
                                                                                         (101, 101, 101))
                        text1 = pygame.font.Font('Bubbleboddy-Neue-trial.ttf', 30).render(
                            'Останьтесь последним выжившим!',
                            True,
                            (101, 101, 101))
                        screen.blit(text, (860, 170))
                        screen.blit(text1, (745, 222))

                elif MODE[0] == 'hard':
                    counter += 1
                    if counter < 180:
                        text = pygame.font.Font('Bubbleboddy-Neue-trial.ttf', 40).render('Survival mod:', True,
                                                                                         (101, 101, 101))
                        text1 = pygame.font.Font('Bubbleboddy-Neue-trial.ttf', 30).render(
                            'Боты охотятся только на вас, постарайтесь выжить!',
                            True,
                            (101, 101, 101))
                        screen.blit(text, (870, 170))
                        screen.blit(text1, (640, 222))

                elif MODE[0] == 'hide_and_seek':
                    counter += 1
                    if animation:
                        try:
                            sound_time.play()
                            screen.blit(animation_set[animation_counter], (910, 300))
                            animation_counter += 1
                            if animation_counter == 4:
                                animation = False
                        except:
                            sound_baraban.set_volume(0.6)
                            sound_baraban.play()
                            animation = False
                            pass

                    if counter < 180:
                        text = pygame.font.Font('Bubbleboddy-Neue-trial.ttf', 40).render('Hide and seek mood:',
                                                                                         True,
                                                                                         (101, 101, 101))
                        text1 = pygame.font.Font('Bubbleboddy-Neue-trial.ttf', 30).render(
                            'Найдите 2 спрятавшихся игроков на карте',
                            True,
                            (101, 101, 101))


                        screen.blit(text, (815, 170))
                        screen.blit(text1, (700, 222))

                text3 = pygame.font.Font('Bubbleboddy-Neue-trial.ttf', 30).render(f'Alive - {len(bots) + 1}', True,
                                                                                  (101, 101, 101))
                screen.blit(text3, (1770, 35))
                text3 = pygame.font.Font('Bubbleboddy-Neue-trial.ttf', 30).render(f'Eaten - {eaten}', True,
                                                                                  (101, 101, 101))
                screen.blit(text3, (1770, 80))

                pygame.display.flip()
                if animation:
                    clock.tick(1)
                else:
                    clock.tick(FPS)
            pygame.quit()


class Info(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('Ui files/info.ui', self)
        self.toolButton_3.clicked.connect(self.rules)

        sqlite_connection = sqlite3.connect('Rating.db')
        cursor = sqlite_connection.cursor()
        name_time_food_score_win = cursor.execute(
            "select * from History").fetchall()
        all_time = 0
        all_food = 0
        max_score = 0
        win_score = 0
        for i in name_time_food_score_win:
            all_time += i[1]
            all_food += i[2]
            if i[3] > max_score:
                max_score = i[3]
            if i[-1] == 1:
                win_score += 1
        self.label_2.setText(str(f'{time.strftime("%H.%M", time.gmtime(all_time))} hour'))
        self.label_3.setText(str(len(name_time_food_score_win)))
        self.label_4.setText(str(all_food))
        self.label_5.setText(str(max_score))
        try:
            self.label_6.setText(str(f'{round((win_score / len(name_time_food_score_win) * 100))}%'))
        except:
            self.label_6.setText(str(f'0%'))

    def rules(self):
        self.rul = Rules()
        self.rul.show()


class Settings(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('Ui files/settings.ui', self)

        if MODE[0] == 'hide_and_seek':
            self.radioButton_6.setChecked(True)
        elif MODE[0] == 'hard':
            self.radioButton_5.setChecked(True)
        elif MODE[0] == 'normal':
            self.radioButton_4.setChecked(True)
        elif COLOR[0] == ((250, 0, 0), (200, 0, 0)):
            self.radioButton.setChecked(True)
        elif COLOR[0] == ((0, 250, 0), (0, 200, 0)):
            self.radioButton.setChecked(True)
        elif COLOR[0] == ((0, 0, 250), (0, 0, 200)):
            self.radioButton.setChecked(True)

        self.radioButton.setChecked(True)
        self.radioButton.toggled.connect(self.red)
        self.radioButton_2.toggled.connect(self.green)
        self.radioButton_3.toggled.connect(self.blue)

        self.radioButton_4.toggled.connect(self.norm)
        self.radioButton_5.toggled.connect(self.hard)
        self.radioButton_6.toggled.connect(self.hide_and_seek)

        self.toolButton.clicked.connect(self.save)

    def norm(self):
        MODE.clear()
        MODE.append('normal')

    def hard(self):
        MODE.clear()
        MODE.append('hard')

    def hide_and_seek(self):
        MODE.clear()
        MODE.append('hide_and_seek')

    def red(self):
        red = ((250, 0, 0), (200, 0, 0))
        COLOR.clear()
        COLOR.append(red)

    def green(self):
        green = ((0, 250, 0), (0, 200, 0))
        COLOR.clear()
        COLOR.append(green)

    def blue(self):
        blue = ((0, 0, 250), (0, 0, 200))
        COLOR.clear()
        COLOR.append(blue)

    def save(self):
        self.hide()


class Rules(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('Ui files/rules.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Start_window()
    form.show()
    sys.exit(app.exec())