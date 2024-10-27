from state.basic import GameState
import pygame as pg


class TitleScreen(GameState):
    def __init__(self):
        super(TitleScreen, self).__init__()
        self.persist["rounds"] = 0
        self.next_state = "GAMEPLAY"
        self._key_commands = self._init_key_commands()
        self._options = ["start", "options", "quit"]
        self._cursor_position = 0

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

    def _init_key_commands(self):
        return {
            pg.K_RETURN: self._press_enter,
            pg.K_ESCAPE: self._quit_key,
            pg.K_UP: self._cursor_up,
            pg.K_DOWN: self._cursor_down
        }

    def _draw_menu(self, surface):
        self.draw_text(surface, "Main Menu", 40, self.screen_rect.width / 2, self.screen_rect.height / 3)
        for i in range(len(self._options)):
            self.draw_text(surface, self._options[i], 30, self.screen_rect.width / 2, self.screen_rect.height / 3 + 60 + i * 40)

    def _press_enter(self):
        if self._cursor_position == 0:
            self.next_state = "GAMEPLAY"
            self.persist["rounds"] = 0
            self.persist["score"] = 0
            self.done = True
        elif self._cursor_position == 1:
            self.done = True
        elif self._cursor_position == 2:
            self.quit = True

    def _cursor_up(self):
        self._cursor_position = (self._cursor_position - 1 + len(self._options)) % len(self._options)

    def _cursor_down(self):
        self._cursor_position = (self._cursor_position + 1 + len(self._options)) % len(self._options)

    def _quit_key(self):
        self.quit = True
