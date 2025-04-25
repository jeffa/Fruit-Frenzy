#!/usr/bin/env python3
"""
Fruit Frenzy
A simple PyQt5 game where the player controls a basket to catch falling fruits.
"""
import sys
import random
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QColor, QFont

class GameWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.resetGame()
        self.setFocusPolicy(Qt.StrongFocus)
        # Game loop timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateGame)
        self.timer.start(16)  # ~60 FPS
        # Fruit spawn timer
        self.spawn_timer = QTimer(self)
        self.spawn_timer.timeout.connect(self.spawnFruit)
        self.spawn_timer.start(self.spawn_interval)

    def initUI(self):
        self.WINDOW_WIDTH = 400
        self.WINDOW_HEIGHT = 600
        self.setFixedSize(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.setWindowTitle("Fruit Frenzy")
        # Basket settings
        self.basket_width = 80
        self.basket_height = 20
        self.basket_speed = 8
        self.basket_y = self.WINDOW_HEIGHT - self.basket_height - 10
        # Fruit settings
        self.fruit_min_size = 20
        self.fruit_max_size = 30
        self.colors = [QColor("red"), QColor("green"), QColor("yellow"), QColor("magenta"), QColor("orange")]

    def resetGame(self):
        self.basket_x = (400 - 80) / 2
        self.left_pressed = False
        self.right_pressed = False
        self.fruits = []
        self.score = 0
        self.lives = 5
        self.game_over = False
        self.base_speed = 2.0
        self.spawn_interval = 1500

    def spawnFruit(self):
        size = random.randint(self.fruit_min_size, self.fruit_max_size)
        x = random.randint(0, self.WINDOW_WIDTH - size)
        fruit = {
            'x': x,
            'y': 0,
            'size': size,
            'speed': self.base_speed + random.random(),
            'color': random.choice(self.colors)
        }
        self.fruits.append(fruit)
        # Increase difficulty
        self.base_speed += 0.02
        self.spawn_interval = max(300, self.spawn_interval - 10)
        self.spawn_timer.start(self.spawn_interval)

    def updateGame(self):
        if not self.game_over:
            # Move basket
            if self.left_pressed:
                self.basket_x -= self.basket_speed
            if self.right_pressed:
                self.basket_x += self.basket_speed
            self.basket_x = max(0, min(self.basket_x, self.WINDOW_WIDTH - self.basket_width))
            # Update fruits
            to_remove = []
            for fruit in self.fruits:
                fruit['y'] += fruit['speed']
                # Check catch
                if (fruit['y'] + fruit['size'] >= self.basket_y and
                        fruit['x'] + fruit['size'] >= self.basket_x and
                        fruit['x'] <= self.basket_x + self.basket_width):
                    self.score += 1
                    to_remove.append(fruit)
                # Check miss
                elif fruit['y'] > self.WINDOW_HEIGHT:
                    self.lives -= 1
                    to_remove.append(fruit)
                    if self.lives <= 0:
                        self.game_over = True
            for fruit in to_remove:
                if fruit in self.fruits:
                    self.fruits.remove(fruit)
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        # Background
        painter.fillRect(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT, QColor("lightblue"))
        # Basket
        painter.setBrush(QColor("brown"))
        painter.drawRect(int(self.basket_x), self.basket_y, self.basket_width, self.basket_height)
        # Fruits
        for fruit in self.fruits:
            painter.setBrush(fruit['color'])
            painter.drawEllipse(int(fruit['x']), int(fruit['y']), fruit['size'], fruit['size'])
        # Score and lives
        painter.setPen(Qt.black)
        painter.setFont(QFont("Arial", 14))
        painter.drawText(10, 25, f"Score: {self.score}")
        painter.drawText(10, 50, f"Lives: {self.lives}")
        # Game over overlay
        if self.game_over:
            painter.setBrush(QColor(0, 0, 0, 150))
            painter.drawRect(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
            painter.setPen(QColor("white"))
            painter.setFont(QFont("Arial", 32))
            painter.drawText(self.rect(), Qt.AlignCenter, "Game Over")
            painter.setFont(QFont("Arial", 16))
            painter.drawText(self.rect().adjusted(0, 50, 0, 0), Qt.AlignCenter,
                             f"Final Score: {self.score}\nPress Space to Restart")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.left_pressed = True
        elif event.key() == Qt.Key_Right:
            self.right_pressed = True
        elif event.key() == Qt.Key_Space and self.game_over:
            self.resetGame()
        else:
            super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.left_pressed = False
        elif event.key() == Qt.Key_Right:
            self.right_pressed = False
        else:
            super().keyReleaseEvent(event)

def main():
    app = QApplication(sys.argv)
    game = GameWidget()
    game.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()