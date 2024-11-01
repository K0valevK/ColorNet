from state.basic import GameState
import pygame as pg


class ScoreScreen(GameState):
    def __init__(self):
        super(ScoreScreen, self).__init__()
        self.start_ticks = pg.time.get_ticks()
        self.round_time = 5

    def startup(self, persistent):
        self.persist = persistent
        self.start_ticks = pg.time.get_ticks()
        self.next_state = "GAMEPLAY" if self.persist["rounds"] < 5 else "TITLE"

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True

    def update(self, dt):
        if self._get_timer_time() > self.round_time:
            self.done = True

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        answer_str = "You are Correct" if self.persist["is_correct"] else "You are wrong"
        self.draw_text(surface, str(self._get_remaining_time()), 50, 100, 100)
        self.draw_text(surface, answer_str, 40, self.screen_rect.width / 2, self.screen_rect.height / 3)
        self.draw_text(surface, f"Current score: {self.persist['score']}", 20, self.screen_rect.width / 2, self.screen_rect.height / 3 + 40)

    def _get_timer_time(self):
        return (pg.time.get_ticks() - self.start_ticks) // 1000

    def _get_remaining_time(self):
        remaining_time = self.round_time - self._get_timer_time()
        return remaining_time if remaining_time >= 0 else 0
