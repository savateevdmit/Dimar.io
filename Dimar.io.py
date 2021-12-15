import sys

import pygame
from math import *
from random import *

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QIcon, QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLabel, QFileDialog, QToolButton, QDialog, QScrollBar, \
    QSpinBox, QMessageBox


class Start_window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('start.ui', self)  # Загружаем дизайн
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
                self.cell_size = 50

            def set_view(self, left, top, cell_size):
                self.left += left
                self.top += top
                if self.left < -1 * self.cell_size * self.width + 750 or self.left > 750:
                    self.left -= left
                if self.top < -1 * self.cell_size * self.width + 405 or self.top > 405:
                    self.top -= top
                self.cell_size = cell_size

            def render(self, screen):
                for y in range(self.height):
                    for x in range(self.width):
                        pygame.draw.rect(screen, pygame.Color(200, 200, 200), (
                            x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                            self.cell_size), 1)

            def move(self):
                return self.left, self.top

        if __name__ == '__main__':
            pygame.init()
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

            running = True
            board = Board(100, 100)
            v = 6
            xx = ''
            yy = ''
            x1 = 0
            y1 = 0
            r = 50
            i = 0
            t = False
            s = ''
            m = 1
            b = False
            plr = []
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
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        t = True
                        i = 0
                if (x > r or x < -r) or (y > r or y < -r):
                    board.set_view(0 - (x / z) * v, 0 - (y / z) * v, 50)

                if t:
                    if r > 40:
                        r = r / 2
                        v = v * 1.5
                    t = False

                screen.fill((235, 235, 235))

                board.render(screen)
                pygame.draw.circle(screen, (200, 0, 0), (755, 405), r + 5)
                pygame.draw.circle(screen, (255, 0, 0), (755, 405), r)

                pygame.display.flip()

                pygame.display.flip()
            pygame.quit()


class Info(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('info.ui', self)


class Settings(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('settings.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Start_window()
    ex.show()
    sys.exit(app.exec_())
