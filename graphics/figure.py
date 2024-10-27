from abc import ABC, abstractmethod
from dataclasses import dataclass
import pygame as pg


@dataclass
class Figure(ABC):
    composition = None

    @abstractmethod
    def __init__(self, x_pos, y_pos):
        ...

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

    def __init__(self, x_pos, y_pos):
        self.composition = pg.Rect(x_pos, y_pos, 40, 40)

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
class Graphic:
    figure: Figure
    color: pg.Color
    x_velocity: float = 1.0
    y_velocity: float = 1.0

    def __init__(self, figure_type, x_pos, y_pos, color):
        self.figure = figure_type(x_pos, y_pos)
        self.color = color

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
