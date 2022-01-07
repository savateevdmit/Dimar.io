import sys, os
from math import *
from random import *

import pygame
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox

pygame.font.init()

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
        play = True
        name = self.lineEdit.text()
        if len(name) > 9:
            play = False
            self.message('Длина имени не может быть больше 9 символов!')

        elif len(name) == 0:
            play = False
            self.message('Введите имя!')

        if play:
            self.play()

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
        name = self.lineEdit.text()
        global x, x1, y1, width1, high1, bb, intersection_coordinates, list_of_coordinates, boost, ww, hh, koord, y, z

        class Board:
            def __init__(self, width, height):
                self.width = width
                self.height = height
                self.board = [[0] * width for _ in range(height)]
                self.left = randrange(-4250, width)
                self.top = randrange(-4300, high)
                self.cell_size = 75

            def set_view(self, left, top, cell_size, a, v, b):
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
                if self.top < -1 * self.cell_size * self.width + high or self.top > high:
                    self.top -= top
                    for i in range(len(a)):
                        a[i][1] -= top
                    for i in range(len(v)):
                        v[i][1] -= top
                    for i in range(len(b)):
                        b[i][1] -= top
                return a, v, b

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
            return [[randrange(board.move()[0], s * 100 + board.move()[0]),  # создание еды
                     randrange(board.move()[1], s * 100 + board.move()[1]),
                     (randrange(0, 255), randrange(0, 255), randrange(0, 255)), randrange(20, 350)] for _ in range(20)]

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
            kff = 20
            flag = False
            r_v = {}
            move = True
            w = []
            virus = []
            number_of_viruses = randrange(40, 70)
            image1 = pygame.transform.scale(Virus.load_image("virus.png"), (150, 150))
            del_virus = []
            bots = bot(size)
            del_bots = []
            kf1 = 0
            kff1 = 15
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
                            w.append([koord, kf1, kff1, True])
                        elif event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                            if r >= 40 and not flag:
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
                    points, virus, bots = board.set_view(0 - (x / z) * v, 0 - (y / z) * v, size, points, virus, bots)
                    width1 -= (x / z) * v
                    high1 -= (y / z) * v

                for i in range(len(virus)):
                    if (width - r < virus[i][0] < width + r and high - r < virus[i][1] < high + r) and r >= virus[i][-1]:
                        del_virus.append(virus[i])
                        virus[i][-3] == False
                        virus.append([randrange(int(board.move()[0]), int(size * 100 + board.move()[0])),
                                      randrange(int(board.move()[1]), int(size * 100 + board.move()[1])), (0, 0, 0),
                                      True, True, 70])
                        koord = delenie(x, y, z)
                        for i in range(randrange(5, 10)):
                            r -= 5
                            w.append(
                                [delenie(randrange(-20, 20), randrange(-20, 20),
                                         sqrt(randrange(-20, 20) ** 2 + randrange(-20, 20) ** 2)), 0, 10, True])
                        b = True
                for i in range(len(points)):
                    if (width - r < points[i][0] < width + r and high - r < points[i][1] < high + r) and r >= points[i][-1]:
                        del_points.append(points[i])
                for i in range(len(bots)):
                    if (width - r < bots[i][0] < width + r and high - r < bots[i][1] < high + r) and abs(width - bots[i][0]) < 0.5 * r and abs(high - bots[i][1]) < 0.5 * r and r > bots[i][-1] * 1.05:
                        del_bots.append(bots[i])

                    elif r * 1.05 < bots[i][-1] and bots[i][0] - bots[i][-1] < width < bots[i][0] + bots[i][-1] and bots[i][1] - bots[i][-1] < high < bots[i][1] + bots[i][-1] and abs(bots[i][0] - width) < 0.5 * bots[i][-1] and abs(bots[i][1] - high) < 0.5 * bots[i][-1]:
                        running = False

                for i in del_points:
                    if r >= 150:
                        if size > 40:
                            size *= (pi * (r ** 2)) / ((pi * (r ** 2)) + (pi * (i[-1] ** 2)))
                            r_points *= size / (
                                        size / ((pi * (r ** 2)) / ((pi * (r ** 2)) + (pi * (i[-1] ** 2)))))
                            k = size / (size / ((pi * (r ** 2)) / ((pi * (r ** 2)) + (pi * (i[-1] ** 2)))))

                            v *= (pi * (r ** 2)) / ((pi * (r ** 2)) + (pi * (i[-1] ** 2)))
                        else:
                            size *= 0.99999
                            r_points *= 0.99999
                            k = 0.99999
                            v *= 0.99999
                        points, virus, bots = board.set_view_2(k, size, points, virus, bots)

                        for h in range(len(bots)):
                            bots[h][-1] *= k
                        for g in range(len(points)):
                            if 0 < points[g][0] < width * 2 and 0 < points[g][1] < high * 2:
                                pygame.draw.circle(screen, points[g][2], (points[g][0], points[g][1]), r_points)
                    elif r < 150:
                        r = sqrt(((pi * (r ** 2)) + (pi * (i[-1] ** 2))) / pi)
                        v *= 0.999

                    try:
                        del points[points.index(i)]
                    except Exception as e:
                        pass
                del_points = []

                for i in del_virus:
                    if r >= 150:
                        size *= (pi * (r ** 2)) * 1.001 / ((pi * (r ** 2)) + (pi * (i[-1] ** 2))) * 1.1
                        r_points *= size / (size / ((pi * (r ** 2)) * 1.001 / ((pi * (r ** 2)) + (pi * (i[-1] ** 2)))))
                        k = size / (size / ((pi * (r ** 2)) * 1.001 / ((pi * (r ** 2)) + (pi * (i[-1] ** 2)))))
                        points, virus, bots = board.set_view_2(k, size, points, virus, bots)
                        for h in range(len(bots)):
                            bots[h][-1] *= size / (size / ((pi * (r ** 2)) * 1.001 / ((pi * (r ** 2)) + (pi * (i[-1] ** 2)))))
                        v *= (pi * (r ** 2)) / ((pi * (r ** 2)) + (pi * (i[-1] ** 2)))
                    elif r < 150:

                        v *= 0.999

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
                        v *= 0.999
                        r = sqrt(((pi * (r ** 2)) + (pi * (i[-1] ** 2))) / pi)

                    try:
                        del bots[bots.index(i)]
                    except Exception as e:
                        pass
                del_bots = []
                screen.fill((235, 235, 235))
                board.render(screen)

                for i in range(len(points)):
                    if points[i][-1] == 22:
                        pygame.draw.circle(screen, (200, 0, 0), (points[i][0], points[i][1]),
                                           27)  # TODO отнимать от points[i][2] 55
                        pygame.draw.circle(screen, points[i][2], (points[i][0], points[i][1]), points[i][-1])
                    else:
                        pygame.draw.circle(screen, points[i][2], (points[i][0], points[i][1]), r_points)
                for i in range(len(virus)):
                    if points[i][-1] == 70:
                        pygame.draw.circle(screen, (0, 0, 0), (points[i][0] + 75, points[i][1] + 75), 70)
                try:
                    if b:
                        for i in w:
                            if i[1] < 300 and i[2] > 0:  # 0
                                pygame.draw.circle(screen, (200, 0, 0),
                                               ((i[0][0] / i[0][2]) * i[1] + width, i[0][1] / i[0][2] * i[1] + high),
                                               26)
                                pygame.draw.circle(screen, (255, 0, 0),
                                               ((i[0][0] / i[0][2]) * i[1] + width, i[0][1] / i[0][2] * i[1] + high),
                                               21)
                                i[1] += i[2]
                                i[2] -= 0.5
                            else:
                                i[3] = False
                                i[1] = 0
                                i[2] = 15

                            if i[2] == 0:
                                points.append(
                                    [(i[0][0] / i[0][2]) * i[1] + width, i[0][1] / i[0][2] * i[1] + high, (250, 0, 0),
                                    False, 22])
                                del w[w.index(i)]
                        for i in w:
                            if i[3]:
                                b = True
                            else:
                                b = False

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
                        for i in del_bots:
                            r2 += (sqrt(((pi * (r2 ** 2)) + (pi * (i[-1] ** 2))) / pi) - r2) / 4
                            try:
                                del bots[bots.index(i)]
                            except:
                                pass
                        pygame.draw.circle(screen, (200, 0, 0),
                                           ((koord[0] / koord[2]) * kf + width, koord[1] / koord[2] * kf + high),
                                           r2 + 5)
                        pygame.draw.circle(screen, (255, 0, 0),
                                           ((koord[0] / koord[2]) * kf + width, koord[1] / koord[2] * kf + high), r2)
                        kf += kff
                        kff -= 0.5
                    else:

                        flag = False
                        kf = 0
                        kff = 20
                        r += r2

                if r >= 70:
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
                                      True, True, 70])
                        viruss = False

                for u in range(len(bots)):
                    if 0 < bots[u][0] + bots[u][-1] and bots[u][0] - bots[u][-1] < width * 2 and 0 < bots[u][1] + bots[u][-1] and bots[u][1] - bots[u][-1] < high * 2 and bots[u][-1] < r:
                        pygame.draw.circle(screen, bots[u][2], (bots[u][0], bots[u][1]), bots[u][-1])

                pygame.draw.circle(screen, (200, 0, 0), (width, high), r + 5)
                pygame.draw.circle(screen, (255, 0, 0), (width, high), r)

                text = pygame.font.Font('Bubbleboddy-Neue-trial.ttf', int(r // 2.5)).render(name, True, [0, 0, 0])
                text1 = pygame.font.Font('Bubbleboddy-Neue-trial.ttf', int(r // 3.5)).render(str(round(r) - 30), True,
                                                                                             [0, 0, 0])
                screen.blit(text, (width - (int(len(name) * int(r // 5.2))) // 2, high - int(r // 2.2)))
                screen.blit(text1, (width - (int(len(name) * int(r // 19))) // 2, high - int(r // 30)))

                for g in range(len(bots)):
                    if 0 < bots[g][0] + bots[g][-1] and bots[g][0] - bots[g][-1] < width * 2 and 0 < bots[g][1] + bots[g][-1] and bots[g][1] - bots[g][-1] < high * 2 and bots[g][-1] > r:
                        pygame.draw.circle(screen, bots[g][2], (bots[g][0], bots[g][1]), bots[g][-1])

                if r < 70:
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