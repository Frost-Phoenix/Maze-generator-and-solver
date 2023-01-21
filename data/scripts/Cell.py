import pygame as pg
#------------------------------------------------------
from data.scripts.Utils import CELL_SIZE, CELLS_COLORS


class Cell:

    def __init__(self, pos: tuple, _type: str) -> None:
        
        # Variables
        self.pos = pos
        self.type = _type
        self.last_type = None
        self.is_grid_draw = False
        self.nb = None

    def change_type(self, _type: str) -> None:
        self.type = _type

    def draw(self, window: pg.Surface, draw_grid: bool) -> None:
        if self.last_type != self.type or self.is_grid_draw != draw_grid:
            self.last_type = self.type
            self.is_grid_draw = draw_grid
            if draw_grid: 
                pg.draw.rect(window, "black", (self.pos[0]*CELL_SIZE, self.pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pg.draw.rect(window, CELLS_COLORS[self.type], (self.pos[0]*CELL_SIZE+1, self.pos[1]*CELL_SIZE+1, CELL_SIZE-1, CELL_SIZE-1))
            else:            
                pg.draw.rect(window, CELLS_COLORS[self.type], (self.pos[0]*CELL_SIZE, self.pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))