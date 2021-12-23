import pygame
from math import *
from random import *
import os
import sqlite3
import sys

from PIL import Image
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QIcon, QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLabel, QFileDialog, QToolButton, QDialog, QScrollBar, \
    QSpinBox, QMessageBox

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
        class Board:
            def __init__(self, width, height):
                self.width = width
                self.height = height
                self.board = [[0] * width for _ in range(height)]
                self.left = randrange(-4250, width)
                self.top = randrange(-4300, high)
                self.cell_size = 75

            def set_view(self, left, top, cell_size, a):
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
                     (randrange(0, 255), randrange(0, 255), randrange(0, 255)), r] for _ in range(2000)]

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
            plr = []
            size = 100
            points = pointss(size, r)
            del_points = []
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                    if event.type == pygame.MOUSEMOTION:
                        x, y = event.pos
                        x -= width
                        y -= high
                        z = sqrt(x ** 2 + y ** 2)

                    del_points = []
                if len(points) < 2000:
                    points.append([randrange(int(board.move()[0]), int(size * 100 + board.move()[0])),
                                   randrange(int(board.move()[1]), int(size * 100 + board.move()[1])),
                                   (randrange(0, 255), randrange(0, 255), randrange(0, 255)), r_points])
                if (x > 50 or x < -50) or (y > 50 or y < -50):
                    points = board.set_view(0 - (x / z) * v, 0 - (y / z) * v, size, points)

                for i in range(len(points)):
                    if width - r < points[i][0] < width + r and high - r < points[i][1] < high + r:
                        del_points.append(points[i])
                for i in del_points:
                    del points[points.index(i)]

                    if r >= 150:
                        size *= (pi * (r ** 2)) * 1.001 / ((pi * (r ** 2)) + (pi * (r_points ** 2)))
                        r_points *= size / (size / ((pi * (r ** 2)) * 1.001 / ((pi * (r ** 2)) + (pi * (r_points ** 2)))))
                        k = size / (size / ((pi * (r ** 2)) * 1.001 / ((pi * (r ** 2)) + (pi * (r_points ** 2)))))
                        points = board.set_view_2(k, size, points)
                        v *= (pi * (r ** 2)) / ((pi * (r ** 2)) + (pi * (r_points ** 2))) * 1.001
                        for i in range(len(points)):
                            if 0 < points[i][0] < width * 2 and 0 < points[i][1] < high * 2:
                                pygame.draw.circle(screen, points[i][2], (points[i][0], points[i][1]), points[i][3])
                    elif r < 150:
                        r = sqrt(((pi * (r ** 2)) + (pi * (r_points ** 2))) / pi) * 1.001
                        v *= size / (size / ((pi * (r ** 2)) / ((pi * (r ** 2)) + (pi * (r_points ** 2)))))
                del_points = []
                screen.fill((235, 235, 235))
                board.render(screen)
                for i in range(len(points)):
                    pygame.draw.circle(screen, points[i][2], (points[i][0], points[i][1]), r_points)

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
