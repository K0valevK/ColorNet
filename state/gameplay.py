from state.basic import GameState
import pygame as pg
from random import randint


class Gameplay(GameState):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.figures = [[pg.Rect((randint(0, 1280), randint(0, 720)), (128, 128)), 1] for _ in range(5)]

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True

    def update(self, dt):
        for rect in self.figures:
            rect[0].move_ip(rect[1], 0)
            if (rect[0].right > self.screen_rect.right
                    or rect[0].left < self.screen_rect.left):
                rect[1] *= -1
                rect[0].clamp_ip(self.screen_rect)

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        for rect in self.figures:
            pg.draw.rect(surface, pg.Color("red"), rect[0])
