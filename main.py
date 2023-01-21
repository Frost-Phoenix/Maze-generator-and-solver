import pygame as pg
import sys
#------------------------------------------------------
from data.scripts.Game import Game  
from data.scripts.Utils import WINDOW_WIDTH, WINDOW_HEIGHT


def main() -> None:

    pg.init()

    pg.display.set_caption("Labyrinth solver")
    window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    window.fill((15,15,15))
    clock = pg.time.Clock()

    # Game variable
    FPS = 60
    game = Game(window)

    game_runing = True
    while game_runing:

        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            
            if event.type == pg.KEYDOWN:
                if event.key >= 97 and event.key <= 122: game.use_key(chr(event.key).upper())


        game.update()
        game.draw()

        pg.display.set_caption("Labyrinth solver : " + str(int(clock.get_fps())) + " fps")

        pg.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
