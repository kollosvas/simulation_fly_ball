"""Класс QuadTree"""

from PySide6.QtCore import QRectF


class QuadTree:
    """Класс описывающий квадродеревья"""

    def __init__(self, boundary, capacity):
        # Конструктор инициализирует граничную область и ёмкость квадродерева.
        self.boundary = boundary
        self.capacity = capacity
        self.balls = []
        self.divided = False
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None

    def subdivide(self):
        """Метод делит текущий узел на четыре подузла."""
        x, y, w, h = (
            self.boundary.x(),
            self.boundary.y(),
            self.boundary.width() / 2,
            self.boundary.height() / 2,
        )
        self.northeast = QuadTree(QRectF(x + w, y, w, h), self.capacity)
        self.northwest = QuadTree(QRectF(x, y, w, h), self.capacity)
        self.southeast = QuadTree(QRectF(x + w, y + h, w, h), self.capacity)
        self.southwest = QuadTree(QRectF(x, y + h, w, h), self.capacity)
        self.divided = True

    def insert(self, ball):
        """Метод вставляет шар в квадродерево, если он находится в пределах граничной области."""
        if not self.boundary.contains(ball.x, ball.y):
            return False

        if len(self.balls) < self.capacity:
            self.balls.append(ball)
            return True

        if not self.divided:
            self.subdivide()

        return (
            self.northeast.insert(ball)
            or self.northwest.insert(ball)
            or self.southeast.insert(ball)
            or self.southwest.insert(ball)
        )

    def query(self, area, found):
        """Метод ищет шары в заданной области и добавляет их в список 'found'."""
        if not self.boundary.intersects(area):
            return

        for ball in self.balls:
            if area.contains(ball.x, ball.y):
                found.append(ball)

        if self.divided:
            self.northwest.query(area, found)
            self.northeast.query(area, found)
            self.southwest.query(area, found)
            self.southeast.query(area, found)
