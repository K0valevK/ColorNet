import sys
import pygame as pg
from game import Game
from state import gameplay, title


if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((1280, 720))
    states = {"SPLASH": title.SplashScreen(),
              "GAMEPLAY": gameplay.Gameplay()}
    game = Game(screen, states, "SPLASH")
    game.run()
    pg.quit()
    sys.exit()
