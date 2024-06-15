"""Модуль моделирования полетов шаров"""

import random
import numpy as np
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer, QRectF, Signal
from PySide6.QtGui import QPainter, QColor, QPen, Qt

from classes.ball import Ball
from classes.quadtree import QuadTree


class CollisionSimulation(QWidget):
    """Моделирование столкновений"""

    window_resized = Signal(int, int)

    def __init__(self):
        super().__init__()
        self.balls = []
        self.quad_tree = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(16)  # Обновление каждые 16 миллисекунд (около 60 FPS).

    def generate_balls(
        self, num_balls, min_radius, max_radius, width, height, min_speed, max_speed
    ):
        """Метод генерирует заданное количество шаров с случайными параметрами."""
        self.balls.clear()
        for _ in range(num_balls):
            radius = random.randint(min_radius, max_radius)
            x = random.uniform(radius, width - radius)
            y = random.uniform(radius, height - radius)
            vx = random.uniform(min_speed, max_speed) * random.choice([-1, 1])
            vy = random.uniform(min_speed, max_speed) * random.choice([-1, 1])
            weight = np.pi * (radius**2)
            self.balls.append(Ball(x, y, radius, vx, vy, weight))

        self.quad_tree = QuadTree(QRectF(0, 0, width, height))

    def update_simulation(self):
        """Метод обновляет состояние моделирования на каждом шаге таймера."""
        if self.quad_tree is not None:
            self.quad_tree = QuadTree(QRectF(0, 0, self.width(), self.height()))
            for ball in self.balls:
                self.quad_tree.insert(ball)

            checked_pairs = set()
            for ball in self.balls:
                ball.move()
                if ball.x - ball.radius < 0:
                    ball.x = ball.radius
                    ball.vx *= -1
                elif ball.x + ball.radius > self.width():
                    ball.x = self.width() - ball.radius
                    ball.vx *= -1
                if ball.y - ball.radius < 0:
                    ball.y = ball.radius
                    ball.vy *= -1
                elif ball.y + ball.radius > self.height():
                    ball.y = self.height() - ball.radius
                    ball.vy *= -1

                range = QRectF(
                    ball.x - ball.radius,
                    ball.y - ball.radius,
                    ball.radius * 2,
                    ball.radius * 2,
                )
                found = []
                self.quad_tree.query(range, found)

                for other in found:
                    if (
                        ball != other
                        and (ball, other) not in checked_pairs
                        and (other, ball) not in checked_pairs
                    ):
                        self.resolve_collision(ball, other)
                        checked_pairs.add((ball, other))

        self.repaint()  # Перерисовка виджета.

    def resolve_collision(self, ball1, ball2):
        """Метод разрешает столкновение между двумя шарами."""
        dx = ball1.x - ball2.x
        dy = ball1.y - ball2.y
        distance = np.hypot(dx, dy)

        if distance == 0:
            return

        # Направление нормали
        nx = dx / distance
        ny = dy / distance

        # Относительная скорость
        dvx = ball1.vx - ball2.vx
        dvy = ball1.vy - ball2.vy

        # Скорость вдоль нормали
        vn = dvx * nx + dvy * ny

        if vn > 0:
            return

        # Массы шаров
        weight1 = ball1.weight
        weight2 = ball2.weight

        # Импульс вдоль нормали
        impulse = 2 * vn / (weight1 + weight2)

        ball1.vx -= impulse * weight2 * nx
        ball1.vy -= impulse * weight2 * ny
        ball2.vx += impulse * weight1 * nx
        ball2.vy += impulse * weight1 * ny

    def paintEvent(self, event):
        """Метод отрисовки виджета."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor(226, 139, 0)))

        if self.quad_tree is not None:
            self.draw_quad_tree(painter, self.quad_tree)

        painter.setPen(Qt.NoPen)
        for ball in self.balls:
            painter.setBrush(QColor(255, 255, 255))
            painter.drawEllipse(
                ball.x - ball.radius,
                ball.y - ball.radius,
                ball.radius * 2,
                ball.radius * 2,
            )

    def draw_quad_tree(self, painter, qt):
        """Рекурсивный метод отрисовки квадродерева."""
        if qt is None:
            return

        painter.drawRect(qt.boundary)
        if qt.divided:
            self.draw_quad_tree(painter, qt.northeast)
            self.draw_quad_tree(painter, qt.northwest)
            self.draw_quad_tree(painter, qt.southeast)
            self.draw_quad_tree(painter, qt.southwest)

    def resizeEvent(self, event):
        """Метод вызывается при изменении размера окна."""
        super().resizeEvent(event)
        self.window_resized.emit(self.width(), self.height())
