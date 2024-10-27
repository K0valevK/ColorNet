from state.basic import GameState
import pygame as pg


class Answer(GameState):
    def __init__(self):
        super(Answer, self).__init__()
        self.location = 0
        self.user_answer = ""

    def startup(self, persistent):
        self.persist = persistent
        self.location = 0
        self.user_answer = ""
        self.next_state = "GAMEPLAY" if self.persist["rounds"] < 5 else "TITLE"

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                if self.user_answer == str(self.persist["answer"]):
                    self.persist["score"] += 1
                self.done = True
            if event.key == pg.K_LEFT:
                self.location = (self.location - 1 + len(self.user_answer) + 1) % (len(self.user_answer) + 1)
            if event.key == pg.K_RIGHT:
                self.location = (self.location + 1 + len(self.user_answer) + 1) % (len(self.user_answer) + 1)
            if event.key == pg.K_BACKSPACE:
                self.user_answer = self.user_answer[:self.location - 1] + self.user_answer[self.location:]
                self.location = (self.location - 1 + len(self.user_answer) + 1) % (len(self.user_answer) + 1)
            if pg.K_0 <= event.key <= pg.K_9:
                self.user_answer = self.user_answer[:self.location] + str(event.key - 48) + self.user_answer[self.location:]
                self.location = (self.location + 1 + len(self.user_answer) + 1) % (len(self.user_answer) + 1)

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        self.draw_text(surface, f"How many {self.persist['q_color']} {self.persist['q_type'].to_str()} was there?", 40, self.screen_rect.width / 2, self.screen_rect.height / 3)
        self.draw_text(surface, self.user_answer, 20, self.screen_rect.width / 2, self.screen_rect.h / 3 + 60)
