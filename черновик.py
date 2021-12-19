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
                self.left = randrange(-4250, 750)
                self.top = randrange(-4300, 405)
                self.cell_size = 75

            def set_view(self, left, top, cell_size, a):
                self.cell_size = cell_size
                for i in range(len(a)):
                    a[i][0] += left
                    a[i][1] += top
                self.left += left
                self.top += top
                if self.left < -1 * self.cell_size * self.width + 750 or self.left > 750:
                    self.left -= left
                    for i in range(len(a)):
                        a[i][0] -= left
                if self.top < -1 * self.cell_size * self.width + 405 or self.top > 405:
                    self.top -= top
                    for i in range(len(a)):
                        a[i][1] -= top

                return a

            def set_view_2(self, a, b, s):
                print(self.left, self.top)
                self.left += s * 2 - a
                self.top += s * 2 - b
                print(self.left, self.top)

            def render(self, screen):
                for y in range(self.height):
                    for x in range(self.width):
                        pygame.draw.rect(screen, pygame.Color(200, 200, 200), (
                            x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                            self.cell_size), 1)

            def move(self):
                return self.left, self.top

        def pointss(s):

            return [[randrange(board.move()[0], s * 100 + board.move()[0]),
                     randrange(board.move()[1], s * 100 + board.move()[1]),
                     (randrange(0, 255), randrange(0, 255), randrange(0, 255))] for _ in range(1000)]

        if __name__ == '__main__':
            pygame.init()
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

            running = True
            board = Board(100, 100)
            v = 8
            r = 50
            r_points = 10
            i = 0
            m = 1
            b = False
            plr = []
            size = 100
            points = pointss(size)
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
                        x -= 755
                        y -= 405
                        z = sqrt(x ** 2 + y ** 2)
                    for i in range(len(points)):
                        if 750 - r < points[i][0] < 750 + r and 405 - r < points[i][1] < 405 + r:
                            del_points.append(points[i])
                    for i in del_points:
                        del points[points.index(i)]
                        if r >= 150:
                            size -= 0.3
                            r_points *= 0.98
                            board.set_view_2(-2, -2, size)
                            for i in range(len(points)):
                                pygame.draw.circle(screen, points[i][2], (points[i][0], points[i][1]), r_points)
                        elif r < 150:
                            r += 0.5
                        print(r, size)

                    del_points = []
                if len(points) < 1000:
                    points.append([randrange(int(board.move()[0]), int(size * 100 + board.move()[0])),
                                   randrange(int(board.move()[1]), int(size * 100 + board.move()[1])),
                                   (randrange(0, 255), randrange(0, 255), randrange(0, 255))])
                if (x > 50 or x < -50) or (y > 50 or y < -50):
                    points = board.set_view(0 - (x / z) * v, 0 - (y / z) * v, size, points)

                screen.fill((235, 235, 235))
                board.render(screen)
                for i in range(len(points)):
                    pygame.draw.circle(screen, points[i][2], (points[i][0], points[i][1]), r_points)

                pygame.draw.circle(screen, (200, 0, 0), (755, 405), r + 5)
                pygame.draw.circle(screen, (255, 0, 0), (755, 405), r)

                pygame.display.flip()

                pygame.display.flip()
            pygame.quit()

class Info(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('Ui files/info.ui', self)


class Settings(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('Ui files/settings.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Start_window()
    ex.show()
    sys.exit(app.exec_())