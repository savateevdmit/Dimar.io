import sys
from math import *
from random import *

import pygame
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from shapely.geometry import LineString
from shapely.geometry import Point

FPS = 30


class Start_window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Ui files/start.ui', self)  # Загружаем дизайн
        self.showFullScreen()
        self.toolButton.clicked.connect(self.click)
        self.toolButton_2.clicked.connect(self.settings)
        self.toolButton_3.clicked.connect(self.info)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            Start_window.hide()

    def info(self):
        self.inf = Info()
        self.inf.show()

    def settings(self):
        self.set = Settings()
        self.set.show()

    def click(self):
        global x, x1, y1, width1, high1, bb, intersection_coordinates, list_of_coordinates, boost, ww, hh, koord, y, z

        class Board:
            def __init__(self, width, height):
                self.width = width
                self.height = height
                self.board = [[0] * width for _ in range(height)]
                self.left = randrange(-4250, width)
                self.top = randrange(-4300, high)
                self.cell_size = 75

            def set_view(self, left, top, cell_size, a):
                # print((left, top, cell_size, a))
                # print()
                # print('----------------------------')
                self.cell_size = cell_size
                for i in range(len(a)):
                    a[i][0] += left
                    a[i][1] += top
                self.left += left
                self.top += top
                if self.left < -1 * self.cell_size * self.width + width or self.left > width:
                    self.left -= left
                    for i in range(len(a)):
                        a[i][0] -= left
                if self.top < -1 * self.cell_size * self.width + high or self.top > high:
                    self.top -= top
                    for i in range(len(a)):
                        a[i][1] -= top
                return a

            def set_view_2(self, k, s, a):
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
                return a

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

        def delenie(x, y, z):
            return [x, y, z]

        def rr(r):
            return r

        if __name__ == '__main__':
            clock = pygame.time.Clock()
            pygame.init()
            size = width, height = 1550, 810
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            width, high = pygame.display.get_surface().get_size()
            width, high = width // 2, high // 2
            running = True
            board = Board(100, 100)
            v = 12
            r = 20
            r_points = 10
            i = 0
            m = 1
            b = False
            bb = False
            plr = []
            size = 100
            width1, high1 = 0, 0
            dropout_range = 350
            points = pointss(size, r_points)
            del_points = []
            kf = 0
            kff = 15
            flag = False
            r_v = {}
            move = True
            w = []
            shift = []
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                        if event.key == pygame.K_w and r >= 50:
                            b = True
                            koord = delenie(x, y, z)
                            r = sqrt((pi * (r ** 2) - pi * (20 ** 2)) / pi)
                            w.append([koord, kf, kff, True])
                        elif event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                            if r >= 40:
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
                    points = board.set_view(0 - (x / z) * v, 0 - (y / z) * v, size, points)
                    width1 -= (x / z) * v
                    high1 -= (y / z) * v

                for i in range(len(points)):
                    if width - r < points[i][0] < width + r and high - r < points[i][1] < high + r:
                        del_points.append(points[i])

                for i in del_points:
                    if r >= 150:
                        size *= (pi * (r ** 2)) * 1.001 / ((pi * (r ** 2)) + (pi * (i[-1] ** 2)))
                        r_points *= size / (size / ((pi * (r ** 2)) * 1.001 / ((pi * (r ** 2)) + (pi * (i[-1] ** 2)))))
                        k = size / (size / ((pi * (r ** 2)) * 1.001 / ((pi * (r ** 2)) + (pi * (i[-1] ** 2)))))
                        points = board.set_view_2(k, size, points)
                        v *= (pi * (r ** 2)) / ((pi * (r ** 2)) + (pi * (i[-1] ** 2)))
                        for g in range(len(points)):
                            if 0 < points[g][0] < width * 2 and 0 < points[g][1] < high * 2:
                                pygame.draw.circle(screen, points[g][2], (points[g][0], points[g][1]), 10)
                    elif r < 150:
                        r = sqrt(((pi * (r ** 2)) + (pi * (i[-1] ** 2))) / pi)
                        v *= 0.995

                    try:
                        del points[points.index(i)]
                    except Exception as e:
                        pass
                del_points = []
                screen.fill((235, 235, 235))
                board.render(screen)

                if b:
                    for i in w:
                        if i[1] < 300 and i[2] > 0:  # 0
                            pygame.draw.circle(screen, (200, 0, 0),
                                               ((i[0][0] / i[0][2]) * i[1] + width, i[0][1] / i[0][2] * i[1] + high),
                                               26)
                            pygame.draw.circle(screen, (255, 0, 0),
                                               ((i[0][0] / i[0][2]) * i[1] + width, i[0][1] / i[0][2] * i[1] + high), 21)
                            i[1] += i[2]
                            i[2] -= 0.5
                        else:
                            i[3] = False
                            i[1] = 0
                            i[2] = 15

                        if i[2] == 0:
                            points.append([(i[0][0] / i[0][2]) * i[1] + width, i[0][1] / i[0][2] * i[1] + high, (255, 0, 0), 22])
                            del w[w.index(i)]
                    for i in w:
                        if i[3]:
                            b = True
                        else:
                            b = False

                for i in range(len(points)):
                    if points[i][3] == 22:
                        pygame.draw.circle(screen, (200, 0, 0), (points[i][0], points[i][1]),
                                           27)  # TODO отнимать от points[i][2] 55
                        pygame.draw.circle(screen, points[i][2], (points[i][0], points[i][1]), points[i][3])
                    else:
                        pygame.draw.circle(screen, points[i][2], (points[i][0], points[i][1]), r_points)

                if flag:
                    if kf < 300 and kff > -15.5:  # 0
                        for i in range(len(points)):
                            if (koord[0] / koord[2]) * kf + width - r1 < points[i][0] < (
                                    koord[0] / koord[2]) * kf + width + r1 and koord[1] / koord[2] * kf + high - r1 < \
                                    points[i][1] < koord[1] / koord[2] * kf + high + r1:
                                del_points.append(points[i])
                        for i in del_points:
                            r2 = r1
                            r1 += (sqrt(((pi * (r1 ** 2)) + (pi * (i[-1] ** 2))) / pi) - r2) / 2
                            try:
                                del points[points.index(i)]
                            except:
                                pass
                        pygame.draw.circle(screen, (200, 0, 0),
                                           ((koord[0] / koord[2]) * kf + width, koord[1] / koord[2] * kf + high),
                                           r1 + 5)
                        pygame.draw.circle(screen, (255, 0, 0),
                                           ((koord[0] / koord[2]) * kf + width, koord[1] / koord[2] * kf + high), r1)
                        kf += kff
                        kff -= 0.5
                    else:

                        flag = False
                        kf = 0
                        kff = 15
                        r += r1

                pygame.draw.circle(screen, (200, 0, 0), (width, high), r + 5)
                pygame.draw.circle(screen, (255, 0, 0), (width, high), r)
                pygame.display.flip()
                clock.tick(FPS)
            pygame.quit()


class Info(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('Ui files/info.ui', self)


class Settings(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('Ui files/settings.ui', self)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Start_window()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
