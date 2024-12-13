from state.basic import GameState
import pygame as pg
import logging


logger = logging.getLogger(__name__)


class DifficultyChoice(GameState):
    def __init__(self):
        super(DifficultyChoice, self).__init__()
        self.persist["rounds"] = 0
        self.next_state = "GAMEPLAY"
        self._key_commands = self._init_key_commands()
        self._options = ["standard", "endless", "return"]
        self._cursor_position = 0
        self._standard_diff = 1

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            command = self._key_commands.get(event.key)
            if command:
                command()

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        self._draw_menu(surface)
        self.draw_text(surface, "*", 20, self.screen_rect.width / 2 - 100, self.screen_rect.height / 3 + 70 + self._cursor_position * 40)
        self.draw_text(surface, str(self._standard_diff), 30, self.screen_rect.width / 2 + 90, self.screen_rect.height / 3 + 60)

    def _init_key_commands(self):
        return {
            pg.K_RETURN: self._press_enter,
            pg.K_ESCAPE: self._quit_key,
            pg.K_UP: self._cursor_up,
            pg.K_DOWN: self._cursor_down,
            pg.K_RIGHT: self._cursor_right,
            pg.K_LEFT: self._cursor_left
        }

    def _draw_menu(self, surface):
        self.draw_text(surface, "Choose Game Mode", 40, self.screen_rect.width / 2, self.screen_rect.height / 3)
        for i in range(len(self._options)):
            self.draw_text(surface, self._options[i], 30, self.screen_rect.width / 2, self.screen_rect.height / 3 + 60 + i * 40)

    def _press_enter(self):
        if self._cursor_position == 0:
            logger.info("Chosen standard mode with difficulty %d", self._standard_diff)
            self.next_state = "GAMEPLAY"
            self.persist["mode"] = "standard"
            self.persist["difficulty"] = self._standard_diff
            self.persist["rounds"] = 0
            self.persist["score"] = 0
            self.done = True
        elif self._cursor_position == 1:
            logger.info("Chosen endless mode")
            self.next_state = "GAMEPLAY"
            self.persist["mode"] = "endless"
            self.persist["rounds"] = 0
            self.persist["score"] = 0
            self.done = True
        elif self._cursor_position == 2:
            self._quit_key()

    def _cursor_up(self):
        self._cursor_position = (self._cursor_position - 1 + len(self._options)) % len(self._options)

    def _cursor_down(self):
        self._cursor_position = (self._cursor_position + 1 + len(self._options)) % len(self._options)

    def _cursor_right(self):
        if self._cursor_position == 0:
            self._standard_diff = (self._standard_diff + 5) % 5 + 1

    def _cursor_left(self):
        if self._cursor_position == 0:
            self._standard_diff = (self._standard_diff + 3) % 5 + 1

    def _quit_key(self):
        self.next_state = "TITLE"
        self.done = True
