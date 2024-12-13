from state.basic import GameState
import pygame as pg
import logging


logger = logging.getLogger(__name__)


class Answer(GameState):
    def __init__(self):
        super(Answer, self).__init__()
        self.location = 0
        self.user_answer = ""

    def startup(self, persistent):
        self.persist = persistent
        self.location = 0
        self.user_answer = ""
        self.next_state = "SCORE"

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.persist["is_correct"] = False
                if self.user_answer == str(self.persist["answer"]):
                    logger.info("Correct answer")
                    self.persist["is_correct"] = True
                    self.persist["score"] += 1
                else:
                    logger.info("Incorrect answer")
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
        question = ["How many"]
        for key in ["q_color", "q_type"]:
            if self.persist[key]:
                if key == "q_type":
                    question.append(self.persist[key].to_str())
                else:
                    question.append(self.persist[key])
        question.append("was there?")
        self.draw_text(
            surface, " ".join(question),40, self.screen_rect.width / 2, self.screen_rect.height / 3
        )
        self.draw_text(surface, self.user_answer, 20, self.screen_rect.width / 2, self.screen_rect.h / 3 + 60)

