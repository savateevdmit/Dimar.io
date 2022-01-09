import sqlite3
import sys, os
import time
from math import *
from random import *


import pygame
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox

pygame.font.init()

FPS = 30
COLOR = []


class Start_window(QMainWindow):
    def __init__(self):
        super().__init__()
        COLOR.append(((250, 0, 0), (200, 0, 0)))
        uic.loadUi('Ui files/start.ui', self)  # Загружаем дизайн
        self.showFullScreen()
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
                self.label_3.setText(str(f'0{round((self.end - self.start) // 60)}:0{round((self.end - self.start) % 60)}'))
            else:
                self.label_3.setText(str(f'00:0{round(self.end - self.start)}'))
        elif len(str(round((self.end - self.start) // 60))) == 2 and len(str(round((self.end - self.start) % 60))) == 1:
            if self.end - self.start >= 60:
                self.label_3.setText(str(f'{round((self.end - self.start) // 60)}:0{round((self.end - self.start) % 60)}'))
            else:
                self.label_3.setText(str(f'00:0{round(self.end - self.start)}'))
        elif len(str(round((self.end - self.start) // 60))) == 1 and len(str(round((self.end - self.start) % 60))) == 2:
            if self.end - self.start >= 60:
                self.label_3.setText(str(f'0{round((self.end - self.start) // 60)}:{round((self.end - self.start) % 60)}'))
            else:
                self.label_3.setText(str(f'00:{round(self.end - self.start)}'))
        elif len(str(round((self.end - self.start) // 60))) == 2 and len(str(round((self.end - self.start) % 60))) == 2:
            if self.end - self.start >= 60:
                self.label_3.setText(str(f'{round((self.end - self.start) // 60)}:{round((self.end - self.start) % 60)}'))
            else:
                self.label_3.setText(str(f'00:{round(self.end - self.start)}'))
        self.label_2.setText(str(self.name))
        self.label_4.setText(str(self.food))
        self.label_5.setText(str(round(self.max_score)))
        self.toolButton_3.clicked.connect(self.replay)
        self.toolButton_4.clicked.connect(self.menu)
        name, time, food, score = self.label_2.text(), round(self.end - self.start), self.label_4.text(), self.label_5.text()
        self.insert_varible_into_table(name, time, food, score)

    def insert_varible_into_table(self, name, time, food, score):  # добавление в базу данных
        sqlite_connection = sqlite3.connect('Rating.db')
        cursor = sqlite_connection.cursor()

        sqlite_insert_with_param = """INSERT INTO History
                              (Name, Time, Food, Score)
                              VALUES (?, ?, ?, ?);"""

        data_tuple = (name, time, food, score)
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
        uic.loadUi('Ui files/start.ui', self)  # Загружаем дизайн
        self.showFullScreen()
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
        # icon = QIcon()
        # icon.addFile(u"Application Icons/log.png", QSize(), QIcon.Normal, QIcon.Off)
        # msg.setWindowIcon(icon)
        msg.exec_()

    def play(self):
        uic.loadUi('Ui files/game_over.ui', self)
        # self.exit()
        global x, x1, y1, width1, high1, bb, intersection_coordinates, list_of_coordinates, boost, ww, hh, koord, y, z

        class Board:
            def __init__(self, width, height):
                self.width = width
                self.height = height
                self.board = [[0] * width for _ in range(height)]
                self.left = randrange(-4250, width)
                self.top = randrange(-4300, high)
                self.cell_size = 75

            def set_view(self, left, top, cell_size, a, v, b, w, w1):
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
                return a, v, b, w, w1

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
            for _ in range(25):
                a = randrange(20, 350)
                b.append([randrange(board.move()[0], s * 100 + board.move()[0]),  # создание еды
                     randrange(board.move()[1], s * 100 + board.move()[1]),
                     (randrange(0, 255), randrange(0, 255), randrange(0, 255)), 12 * 0.997 ** (a - 20), a])
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
            pygame.init()
            size = width, height = 1550, 810
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            width, high = pygame.display.get_surface().get_size()
            width, high = width // 2, high // 2
            running = True
            board = Board(100, 100)
            v = 12
            r = 30
            r_points = 10
            i = 0
            m = 1
            b = False
            bb = False
            viruss = True
            eat_virus = False
            plr = []
            size = 100
            width1, high1 = 0, 0
            dropout_range = 350
            points = pointss(size, r_points)
            del_points = []
            kf = 0
            self.food = 0
            self.max_score = 0
            kff = 20
            flag = False
            r_v = {}
            move = True
            w = []
            virus = []
            number_of_viruses = randrange(40, 70)
            image1 = pygame.transform.scale(Virus.load_image("virus.png"), (180, 180))
            del_virus = []
            bots = bot(size)
            del_bots = []
            kf1 = 0
            kff1 = 15
            self.score = 0
            del_pointsb = []
            virus_radius = 90
            c = False
            s_im = 180
            w_bots = []
            del_virusb = []
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            uic.loadUi('Ui files/game_over.ui', self)
                            self.end = time.monotonic()
                            self.exit()
                            running = False
                        if event.key == pygame.K_w and r >= 50 and self.score >= 15:
                            aaaaa = r
                            b = True
                            kff1 = (232 + r) // 11.5
                            koord = delenie(x, y, z)
                            r = sqrt((pi * (r ** 2) - pi * (20 ** 2)) / pi)
                            w.append([koord, kf1, kff1, width, high])
                            self.score -= (aaaaa - r)
                        elif event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                            if r >= 40 and not flag:
                                self.score /= 2

                                koord = delenie(x, y, z)
                                flag = True
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
                    points, virus, bots, w, w_bots = board.set_view(0 - (x / z) * v, 0 - (y / z) * v, size, points, virus, bots, w, w_bots)
                    width1 -= (x / z) * v
                    high1 -= (y / z) * v

                for i in range(len(virus)):
                    if (width - r < virus[i][0] < width + r and high - r < virus[i][1] < high + r) and r >= virus[i][-1]:
                        del_virus.append(virus[i])
                        virus[i][-3] = False
                        virus.append([randrange(int(board.move()[0]), int(size * 100 + board.move()[0])),
                                      randrange(int(board.move()[1]), int(size * 100 + board.move()[1])), (0, 0, 0),
                                      True, True, 70])
                        koord = delenie(x, y, z)
                        r *= 0.35
                        v /= 0.85
                        self.score *= 0.35
                        for i in range(randrange(20, 30)):

                            w.append(
                                [delenie(randrange(-20, 20), randrange(-20, 20),
                                         sqrt(randrange(-20, 20) ** 2 + randrange(-20, 20) ** 2)), 0, (232 + r) // 15.47, width, high])
                        b = True
                for i in range(len(points)):
                    if (width - r < points[i][0] < width + r and high - r < points[i][1] < high + r) and r >= points[i][-1]:
                        del_points.append(points[i])
                        self.score += points[i][-1] / 20
                for i in range(len(bots)):
                    if (width - r < bots[i][0] < width + r and high - r < bots[i][1] < high + r) and abs(width - bots[i][0]) < 0.5 * r and abs(high - bots[i][1]) < 0.5 * r and r > bots[i][-1] * 1.05:
                        del_bots.append(bots[i])
                        self.score += bots[i][-1] / 20

                    elif r * 1.05 < bots[i][-1] and bots[i][0] - bots[i][-1] < width < bots[i][0] + bots[i][-1] and bots[i][1] - bots[i][-1] < high < bots[i][1] + bots[i][-1] and abs(bots[i][0] - width) < 0.5 * bots[i][-1] and abs(bots[i][1] - high) < 0.5 * bots[i][-1]:
                        uic.loadUi('Ui files/game_over.ui', self)
                        self.end = time.monotonic()
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
                        image1 = pygame.transform.scale(Virus.load_image("virus.png"), (round(s_im), round(s_im)))
                        points, virus, bots = board.set_view_2(k, size, points, virus, bots)
                        virus_radius *= k

                        for h in range(len(bots)):
                            bots[h][-1] *= k
                        for g in range(len(points)):
                            if 0 < points[g][0] < width * 2 and 0 < points[g][1] < high * 2:
                                pygame.draw.circle(screen, points[g][2], (points[g][0], points[g][1]), r_points)
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
                        for h in range(len(bots)):
                            bots[h][-1] *= size / (size / ((pi * (r ** 2)) * 1.001 / ((pi * (r ** 2)) + (pi * (i[-1] ** 2)))))
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
                #
                for i in range(len(points)):
                    if points[i][-1] == 22: # TODO отнимать от points[i][2] 55
                        pygame.draw.circle(screen, points[i][2], (points[i][0], points[i][1]), points[i][-1])
                    else:
                        pygame.draw.circle(screen, points[i][2], (points[i][0], points[i][1]), r_points)
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
                                pygame.draw.circle(screen, (COLOR[0][0]),
                                               ((i[0][0] / i[0][2]) * i[1] + i[-2], i[0][1] / i[0][2] * i[1] + i[-1]),
                                               21)
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
                                    [(i[0][0] / i[0][2]) * i[1] + i[-2], i[0][1] / i[0][2] * i[1] + i[-1], (COLOR[0][0]),
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
                                pygame.draw.circle(screen, i[-1],
                                               ((i[0][0] / i[0][2]) * i[1] + i[-3], i[0][1] / i[0][2] * i[1] + i[-2]),
                                               21)
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
                                    False, 22])
                                del w_bots[w_bots.index(i)]

                except ZeroDivisionError:
                    pass

                if flag:
                    r2 = r1
                    if kf < 700 and kff > -20.5:  # 0

                        for i in range(len(points)):
                            if (koord[0] / koord[2]) * kf + width - r2 < points[i][0] < (
                                    koord[0] / koord[2]) * kf + width + r2 and koord[1] / koord[2] * kf + high - r2 < \
                                    points[i][1] < koord[1] / koord[2] * kf + high + r2:
                                del_points.append(points[i])
                                self.score += points[i][-1] / 20
                        for i in del_points:

                            r2 += (sqrt(((pi * (r2 ** 2)) + (pi * (i[-1] ** 2))) / pi) - r2) / 2
                            try:
                                del points[points.index(i)]
                            except:
                                pass

                        for i in range(len(virus)):
                            if (koord[0] / koord[2]) * kf + width - r2 < virus[i][0] < (
                                    koord[0] / koord[2]) * kf + width + r2 and koord[1] / koord[2] * kf + high - r2 < \
                                    virus[i][1] < koord[1] / koord[2] * kf + high + r2:
                                del_virus.append(virus[i])
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
                                    abs((koord[0] / koord[2]) * kf + width - bots[i][0]) < 0.5 * r2 and abs(koord[1] / koord[2] * kf + high - bots[i][1]) < 0.5 * r2:
                                del_bots.append(bots[i])
                                self.score += bots[i][-1] / 20
                        for i in del_bots:
                            r2 += (sqrt(((pi * (r2 ** 2)) + (pi * (i[-1] ** 2))) / pi) - r2) / 4
                            try:
                                del bots[bots.index(i)]
                            except:
                                pass
                        pygame.draw.circle(screen, COLOR[0][1],
                                           ((koord[0] / koord[2]) * kf + width, koord[1] / koord[2] * kf + high),
                                           r2 + 5)
                        pygame.draw.circle(screen, COLOR[0][0],
                                           ((koord[0] / koord[2]) * kf + width, koord[1] / koord[2] * kf + high), r2)
                        kf += kff
                        kff -= 0.5
                    else:

                        flag = False
                        self.score *= 2
                        kf = 0
                        kff = 20
                        r += r2

                if r >= virus_radius:
                    eat_virus = True
                    for i in virus:
                        if i[-3]:
                            screen.blit(image1, (i[0], i[1]))
                        else:
                            del i
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
                                koord = delenie(x, y, z)
                                bots[u][-1] *= 0.35
                                bots[u][-2] /= 0.95
                                for i in range(randrange(20, 30)):
                                    w_bots.append(
                                        [delenie(randrange(-20, 20), randrange(-20, 20),
                                                 sqrt(randrange(-20, 20) ** 2 + randrange(-20, 20) ** 2)), 0,
                                         (232 + r) // 15.47, bots[u][0], bots[u][1], bots[u][2]])
                                c = True
                        for i in del_virusb:

                            try:
                                del virus[virus.index(i)]
                            except Exception as e:
                                pass
                        del_virusb = []
                        pygame.draw.circle(screen, bots[u][2], (bots[u][0], bots[u][1]), bots[u][-1])
                        del_pointsb = []
                        z1 = sqrt(abs(bots[u][0] - width) ** 2 + abs(bots[u][1] - high) ** 2)
                        bots[u][0] += ((abs(bots[u][0] - width) / z1) * bots[u][-2]) * (width - bots[u][0]) / abs(
                            width - bots[u][0]) * -1
                        bots[u][1] += ((abs(bots[u][1] - high) / z1) * bots[u][-2]) * (high - bots[u][1]) / abs(
                            high - bots[u][1]) * -1
                        l, t = board.move()
                        if l + size * 100 < bots[u][0]:
                            bots[u][0] = l + size * 100
                        elif bots[u][0] < l:
                            bots[u][0] = l
                        if t + size * 100 < bots[u][1]:
                            bots[u][1] = t + size * 100
                        elif bots[u][1] < t:
                            bots[u][1] = t

                if self.score > self.max_score:
                    self.max_score = self.score

                pygame.draw.circle(screen, COLOR[0][1], (width, high), r + 5)
                pygame.draw.circle(screen, COLOR[0][0], (width, high), r)

                text = pygame.font.Font('Bubbleboddy-Neue-trial.ttf', int(r // 2.5)).render(self.name, True, [255, 255, 255])
                text1 = pygame.font.Font('Bubbleboddy-Neue-trial.ttf', int(r // 3.5)).render(str(round(self.score)), True,
                                                                                             [255, 255, 255])
                screen.blit(text, (width - (int(len(self.name) * int(r // 5.2))) // 2, high - int(r // 2.2)))
                screen.blit(text1, (width - (int(len(self.name) * int(r // 19))) // 2, high - int(r // 30)))

                for u in range(len(bots)):
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
                                koord = delenie(x, y, z)
                                bots[u][-1] *= 0.35
                                bots[u][-2] /= 0.95
                                for i in range(randrange(20, 30)):
                                    w_bots.append(
                                        [delenie(randrange(-20, 20), randrange(-20, 20),
                                                 sqrt(randrange(-20, 20) ** 2 + randrange(-20, 20) ** 2)), 0,
                                         (232 + r) // 15.47, bots[u][0], bots[u][1], bots[u][2]])
                                c = True
                        for i in del_virusb:
                            try:
                                del virus[virus.index(i)]
                            except Exception as e:
                                pass
                        del_virusb = []
                        pygame.draw.circle(screen, bots[u][2], (bots[u][0], bots[u][1]), bots[u][-1])
                        del_pointsb = []
                        z1 = sqrt(abs(bots[u][0] - width) ** 2 + abs(bots[u][1] - high) ** 2)
                        bots[u][0] += ((abs(bots[u][0] - width) / z1) * bots[u][-2]) * (width - bots[u][0]) / abs(
                            width - bots[u][0]) * 1
                        bots[u][1] += ((abs(bots[u][1] - high) / z1) * bots[u][-2]) * (high - bots[u][1]) / abs(
                            high - bots[u][1]) * 1
                        l, t = board.move()
                        if l + size * 100 < bots[u][0]:
                            bots[u][0] = l + size * 100
                        elif bots[u][0] < l:
                            bots[u][0] = l
                        if t + size * 100 < bots[u][1]:
                            bots[u][1] = t + size * 100
                        elif bots[u][1] < t:
                            bots[u][1] = t

                if r < virus_radius:
                    for i in virus:
                        if i[-2] and i[-3]:
                            screen.blit(image1, (i[0], i[1]))
                        elif not i[-3]:
                            del i
                pygame.display.flip()
                clock.tick(FPS)
            pygame.quit()


class Info(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('Ui files/info.ui', self)

        sqlite_connection = sqlite3.connect('Rating.db')
        cursor = sqlite_connection.cursor()
        name_time_food_score = cursor.execute(
            "select * from History").fetchall()
        all_time = 0
        all_food = 0
        max_score = 0
        for i in name_time_food_score:
            all_time += i[1]
            all_food += i[2]
            if i[-1] > max_score:
                max_score = i[-1]
        self.label_2.setText(str(f'{round(all_time / 3600, 2)} hour'))
        self.label_3.setText(str(len(name_time_food_score)))
        self.label_4.setText(str(all_food))
        self.label_5.setText(str(max_score))


class Settings(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('Ui files/settings.ui', self)
        self.radioButton.toggled.connect(self.red)
        self.radioButton_2.toggled.connect(self.green)
        self.radioButton_3.toggled.connect(self.blue)
        self.toolButton.clicked.connect(self.save)

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


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Start_window()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())