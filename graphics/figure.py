from abc import ABC, abstractmethod
from dataclasses import dataclass
from operator import add
import pygame as pg


@dataclass
class Figure(ABC):
    @abstractmethod
    def move_ip(self, x_velocity, y_velocity):
        ...

    @abstractmethod
    def clamp_ip(self, rect):
        ...

    @abstractmethod
    def left(self):
        ...

    @abstractmethod
    def right(self):
        ...

    @abstractmethod
    def top(self):
        ...

    @abstractmethod
    def bottom(self):
        ...

    @abstractmethod
    def draw(self, surface, color):
        ...

    @staticmethod
    def to_str():
        return "figures"


@dataclass
class Rectangle(Figure):
    composition: pg.Rect

    def __init__(self, x_pos, y_pos, width=40, height=40):
        self.composition = pg.Rect(x_pos, y_pos, width, height)

    def move_ip(self, x_velocity, y_velocity):
        self.composition.move_ip(x_velocity, y_velocity)

    def clamp_ip(self, rect):
        self.composition.clamp_ip(rect)

    def left(self):
        return self.composition.left

    def right(self):
        return self.composition.right

    def top(self):
        return self.composition.top

    def bottom(self):
        return self.composition.bottom

    def draw(self, surface, color):
        pg.draw.rect(surface, color, self.composition)

    @staticmethod
    def to_str():
        return "rectangles"


@dataclass
class Triangle(Figure):
    point_1: list[int, int]
    point_2: list[int, int]
    point_3: list[int, int]

    def __init__(self, x_pos, y_pos, width=40, height=40):
        self.point_1 = [x_pos, y_pos]
        self.point_2 = [x_pos + width / 2, y_pos - height]
        self.point_3 = [x_pos + width, y_pos]


    def move_ip(self, x_velocity, y_velocity):
        for i in range(1, 3 + 1):
            setattr(self, f"point_{i}", list(map(add, getattr(self, f"point_{i}"), [x_velocity, y_velocity])))

    def clamp_ip(self, rect):
        ...

    def left(self):
        return self.point_1[0]

    def right(self):
        return self.point_3[0]

    def top(self):
        return self.point_2[1]

    def bottom(self):
        return self.point_1[1]

    def draw(self, surface, color):
        pg.draw.polygon(surface, color, (self.point_1, self.point_2, self.point_3))

    @staticmethod
    def to_str():
        return "triangles"


@dataclass
class Circle(Figure):
    x_position: int
    y_position: int
    radius: int

    def __init__(self, x_pos, y_pos, width=40, height=40):
        self.x_position = x_pos + width / 2
        self.y_position = y_pos + width / 2
        self.radius = width / 2

    def move_ip(self, x_velocity, y_velocity):
        self.x_position += x_velocity
        self.y_position += y_velocity

    def clamp_ip(self, rect):
        ...

    def left(self):
        return self.x_position - self.radius

    def right(self):
        return self.x_position + self.radius

    def top(self):
        return self.y_position - self.radius

    def bottom(self):
        return self.y_position + self.radius

    def draw(self, surface, color):
        pg.draw.circle(surface, color, (self.x_position, self.y_position), self.radius)

    @staticmethod
    def to_str():
        return "circles"


@dataclass
class Graphic:
    figure: Figure
    color: pg.Color
    x_velocity: float = 1.0
    y_velocity: float = 1.0

    def __init__(self, figure_type, x_pos, y_pos, size, color, x_velocity=1.0, y_velocity=1.0):
        self.figure = figure_type(x_pos, y_pos, size, size)
        self.color = color
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity

    def move_ip(self):
        self.figure.move_ip(self.x_velocity, self.y_velocity)

    def clamp_ip(self, rect):
        self.figure.clamp_ip(rect)

    def border_screen(self, rect):
        if self.figure.left() < rect.left or rect.right < self.figure.right():
            self.x_velocity *= -1
            self.clamp_ip(rect)
        if self.figure.top() < rect.top or rect.bottom < self.figure.bottom():
            self.y_velocity *= -1
            self.clamp_ip(rect)

    def draw(self, surface):
        self.figure.draw(surface, self.color)
