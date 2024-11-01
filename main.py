import sys
import pygame as pg
from engine import Game
from state import gameplay, title, enter_answer, score


if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((1280, 720))
    states = {"TITLE": title.TitleScreen(),
              "GAMEPLAY": gameplay.Gameplay(),
              "ANSWER": enter_answer.Answer(),
              "SCORE": score.ScoreScreen()}
    game = Game(screen, states, "TITLE")
    game.run()
    pg.quit()
    sys.exit()
