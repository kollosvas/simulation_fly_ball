"""Класс Ball"""

import numpy as np


class Ball:
    """Класс описывающий характеристики и поведение шара"""

    def __init__(self, x, y, radius, vx, vy, weight):
        """Конструктор инициализирует позицию, радиус и скорость шара."""
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = vx
        self.vy = vy
        self.weight = weight

    def move(self):
        """Метод перемещает шар, изменяя его координаты на значение скорости."""
        self.x += self.vx
        self.y += self.vy
