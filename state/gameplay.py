from state.basic import GameState
import pygame as pg
from gameplay.random_round import RoundGenerator
from graphics.figure import Graphic


class Gameplay(GameState):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.start_ticks = pg.time.get_ticks()
        self.round_time = 15
        self.figures: list[Graphic] = []

    def startup(self, persistent):
        self.persist = persistent
        self.persist["rounds"] += 1
        self.start_ticks = pg.time.get_ticks()
        self.persist["q_type"], self.persist["q_color"], self.persist["answer"], self.figures = RoundGenerator.create_round(3, 3, 12, True, False, True)
        self.next_state = "ANSWER"

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True

    def update(self, dt):
        for figure in self.figures:
            figure.move_ip()
            figure.border_screen(self.screen_rect)
        if self._get_timer_time() > self.round_time:
            self.done = True

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        self.draw_text(surface, str(self.round_time - self._get_timer_time()), 50, 100, 100)
        self.draw_text(surface, str(self.persist["rounds"]), 50, 620, 100)
        for rect in self.figures:
            rect.draw(surface)

    def _get_timer_time(self):
        return (pg.time.get_ticks() - self.start_ticks) // 1000
