import pygame as pg
import time
from random import choice
#------------------------------------------------------
from data.scripts.Maze import Maze
from data.scripts.Utils import *


class Game:

    def __init__(self, display_surface: pg.Surface) -> None:

        # Variables
        self.display_surface = display_surface
        self.font = pg.font.Font(r"data/font/upheavtt.ttf", 22)
        self.menu = "main"
        self.menu_text = {"main": [], "solve": [], "edit": [], "generate": [], "indicator": [], "other": []}
        self.editor_cell_type = "empty"
        self.maze = Maze(self.display_surface, True, self.change_selected_editor_cell)
        self.maze.generate(choice(["DFS","kruskal","prism"]))
        self.maze.instant_draw = False
        self.creat_menu()

    def creat_menu(self) -> None:

        def add_txt(menu: str, text: str, pos: tuple) -> None:
            if menu == "indicator":
                txt_surface = [self.font.render(text, False, LIGHT_GREEN),self.font.render(text, False, LIGHT_RED)]
                txt_rect = txt_surface[0].get_rect(midleft = pos)
            else: 
                txt_surface = self.font.render(text, False, WHITE)
                txt_rect = txt_surface.get_rect(midleft = pos)
            self.menu_text[menu].append((txt_surface, txt_rect))

        # main menu
        add_txt("main", "S - Solve", (190, 515))
        add_txt("main", "E - Editor", (190, 545))
        add_txt("main", "G - Generate", (190, 575))
        
        # solve menu
        add_txt("solve", "D - DFS", (190, 515))
        add_txt("solve", "B - BFS", (190, 545))
        add_txt("solve", "A - A star", (190, 575))

        # editor menu
        add_txt("edit", "C - Clear", (190, 515))
        add_txt("edit", "S - Start", (190, 545))
        add_txt("edit", "E - End", (190, 575))

        # generation menu
        add_txt("generate", "D - DFS", (190, 515))
        add_txt("generate", "K - Kruskal", (190, 545))
        add_txt("generate", "P - Prism", (190, 575))
        
        # Indicator
        add_txt("indicator", "G - Grid", (40, 530))
        add_txt("indicator", "I - Instant", (40, 560))
        
        # Other 
        add_txt("other", "M - Menu", (350, 545))

    def change_selected_editor_cell(self, _type: str) -> None:
        self.editor_cell_type = _type

    def use_key(self, key: str) -> None:
        s = time.time()
        
        if self.menu != "main":
            if key == "G": self.maze.draw_grid = not self.maze.draw_grid
            elif key == "I": self.maze.instant_draw = not self.maze.instant_draw
            elif key == "M": self.menu = "main"

        if self.menu == "main":
            if key == "S": self.menu = "solve"
            elif key == "E": 
                self.menu = "edit"
                self.maze.reset_solve_cells()
            elif key == "G": self.menu = "generate"

        elif self.menu == "solve":
            if key == "D": self.maze.solve("DFS")
            elif key == "B": self.maze.solve("BFS")
            elif key == "A": self.maze.solve("A*")

        elif self.menu == "edit":
            if key == "C": self.maze.clear_editor()
            elif key == "S": self.change_selected_editor_cell("start")
            elif key == "E": self.change_selected_editor_cell("goal")

        elif self.menu == "generate":
            if key == "D": self.maze.generate("DFS")
            elif key == "K": self.maze.generate("kruskal")
            elif key == "P": self.maze.generate("prism")

        if time.time() - s > 0: print(time.time() - s)

    def update(self) -> None:
        if self.menu == "edit": self.maze.update_editor(self.editor_cell_type)

    def draw(self) -> None:

        def draw_menu() -> None:
            def draw_frame() -> None:
                pg.draw.rect(self.display_surface, (25,25,25), (0, MAZE_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT-MAZE_HEIGHT))
                pg.draw.rect(self.display_surface, (30,30,30), (0, MAZE_HEIGHT, WINDOW_WIDTH, 5))
                pg.draw.rect(self.display_surface, (30,30,30), (0, WINDOW_HEIGHT-5, WINDOW_WIDTH, 5))
                pg.draw.rect(self.display_surface, (30,30,30), (0, MAZE_HEIGHT, 5, 110))
                pg.draw.rect(self.display_surface, (30,30,30), (WINDOW_WIDTH-5, MAZE_HEIGHT, 5, 110))

            def draw_texts() -> None:
                for txt in self.menu_text[self.menu]:    
                    self.display_surface.blit(txt[0], txt[1])

                if self.menu != "main": 
                    # Menu button
                    for txt in self.menu_text["other"]: self.display_surface.blit(txt[0], txt[1])
                    # Grid button
                    if self.maze.draw_grid: self.display_surface.blit(self.menu_text["indicator"][0][0][0], self.menu_text["indicator"][0][1])
                    else: self.display_surface.blit(self.menu_text["indicator"][0][0][1], self.menu_text["indicator"][0][1])
                    # Instant button
                    if self.maze.instant_draw: self.display_surface.blit(self.menu_text["indicator"][1][0][0], self.menu_text["indicator"][1][1])
                    else: self.display_surface.blit(self.menu_text["indicator"][1][0][1], self.menu_text["indicator"][1][1])

            draw_frame()
            draw_texts()

        self.maze.draw()
        draw_menu()