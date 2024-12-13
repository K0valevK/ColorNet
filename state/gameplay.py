from state.basic import GameState
import random
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
        self.persist["q_type"], self.persist["q_color"], self.persist["answer"], self.figures = self._get_round_by_difficulty()
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
        self.draw_text(surface, str(self._get_remaining_time()), 50, 100, 100)
        self.draw_text(surface, str(self.persist["rounds"]), 50, 620, 100)
        for rect in self.figures:
            rect.draw(surface)

    def _get_timer_time(self):
        return (pg.time.get_ticks() - self.start_ticks) // 1000

    def _get_remaining_time(self):
        remaining_time = self.round_time - self._get_timer_time()
        return remaining_time if remaining_time >= 0 else 0

    def _get_round_by_difficulty(self):
        if self.persist["mode"] == "standard":
            if self.persist["difficulty"] == 1:
                return RoundGenerator.create_round(1, 2, 6, True, False, True, False)
            elif self.persist["difficulty"] == 2:
                return RoundGenerator.create_round(1, 2, 8, True, False, True, False)
            elif self.persist["difficulty"] == 3:
                return RoundGenerator.create_round(2, 2, 8, False, False, True, False)
            elif self.persist["difficulty"] == 4:
                return RoundGenerator.create_round(2, 3, 10, False, False, True, False)
            elif self.persist["difficulty"] == 5:
                return RoundGenerator.create_round(3, 3, 12, False, False, False, False)
        return RoundGenerator.create_round(
            random.randint(2, 3),
            random.randint(2, 3),
            random.randint(6, 12),
            random.choice([True, False]),
            random.choice([True, False]),
            random.choice([True, False]),
        )
