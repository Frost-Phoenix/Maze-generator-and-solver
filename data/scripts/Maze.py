import pygame as pg
import time, sys
from random import choice, randrange
#------------------------------------------------------
import data.scripts.Piles as P
import data.scripts.Filles as F
from data.scripts.Cell import Cell
from data.scripts.Utils import CELL_SIZE, MAZE_WIDTH, MAZE_HEIGHT


class Maze:

    #----------Init----------#
    def __init__(self, display_surface: pg.Surface, instant_draw: bool, change_selected_editor_cell) -> None: # change_selected_editor_cell: function

        # Variables
        self.display_surface = display_surface
        self.change_selected_editor_cell = change_selected_editor_cell
        self.draw_grid = False
        self.instant_draw = instant_draw
        self.start_pos = None
        self.end_pos = None

        # Cells
        self.cells = []

        # Game initialisation
        self.creat_cells()

    def creat_cells(self) -> None:
        for row in range(MAZE_HEIGHT // CELL_SIZE):
            self.cells.append([])
            for col in range(MAZE_WIDTH // CELL_SIZE):
                self.cells[row].append(Cell((col,row), "wall"))
                
    #----------Generation----------#
    def reset_cells(self) -> None:
        for cell_row in self.cells:
            for cell in cell_row: 
                cell.change_type("wall")
                cell.nb = None

    def place_start_and_end(self) -> None:
        # Place start
        self.start_pos = choice([(1,1), (1,47), (47,1), (47,47)])
        self.cells[self.start_pos[0]][self.start_pos[1]].change_type("start")
        # Place goal
        run = True
        while run:
            pos = (choice(range(1,48)),choice(range(1,48)))
            if self.cells[pos[0]][pos[1]].type == "empty":
                run = False
                self.end_pos = pos
                self.cells[pos[0]][pos[1]].change_type("goal")

    def get_avalibles_neighbour(self, pos: tuple, avalable_cell_type: str, nb_cell_expand: int) -> list:
        if nb_cell_expand == 1: neighbour_pos = [(+1,0),(0,+1),(-1,0),(0,-1)]
        elif nb_cell_expand == 2: neighbour_pos = [[(+1,0), (+2,0)],[(0,+1), (0,+2)],[(-1,0), (-2,0)],[(0,-1), (0,-2)]]
        avalable_cells = []

        for n in neighbour_pos:
            if nb_cell_expand == 1:
                if 1 <= pos[0] + n[0] <= (MAZE_WIDTH // CELL_SIZE - 2) and 1 <= pos[1] + n[1] <= (MAZE_HEIGHT // CELL_SIZE - 2):
                    for _type in avalable_cell_type:
                        if self.cells[pos[0] + n[0]][pos[1] + n[1]].type == _type:
                            avalable_cells.append((pos[0] + n[0], pos[1] + n[1]))
            elif nb_cell_expand == 2:
                if 1 <= pos[0] + n[1][0] <= (MAZE_WIDTH // CELL_SIZE - 2) and 1 <= pos[1] + n[1][1] <= (MAZE_HEIGHT // CELL_SIZE - 2):
                    if self.cells[pos[0] + n[1][0]][pos[1] + n[1][1]].type == avalable_cell_type:
                        avalable_cells.append([(pos[0] + n[0][0], pos[1] + n[0][1]), (pos[0] + n[1][0], pos[1] + n[1][1])])

        return avalable_cells

    def generate(self, methode: str) -> None:
        self.reset_cells()

        if methode == "DFS": self.gen_DFS()
        elif methode == "kruskal": self.gen_kruskal()
        elif methode == "prism": self.gen_prism()

        self.place_start_and_end()

    def gen_DFS(self) -> None:
        start_pos = (1,1)
        current_pos = start_pos
        last_pos = [start_pos]
        visited = P.init()
        P.empile(visited, start_pos)

        while not P.est_vide(visited):

            avalable_cells = self.get_avalibles_neighbour(current_pos, "wall", 2)

            if len(avalable_cells) == 0: current_pos = P.depile(visited)
            else:
                next_pos = choice(avalable_cells)
                for pos in next_pos: self.cells[pos[0]][pos[1]].change_type("curent_pos")
                for pos in last_pos: self.cells[pos[0]][pos[1]].change_type("empty")
                P.empile(visited, next_pos[1])
                last_pos = next_pos
                current_pos = next_pos[1]

                if not self.instant_draw: self.update_pygame()

        for pos in last_pos: self.cells[pos[0]][pos[1]].change_type("empty")

    def gen_kruskal(self) -> None:

        def is_finished() -> bool:
            nb = self.cells[1][1].nb

            for r in range(1,int(MAZE_HEIGHT/CELL_SIZE - 1), 2):
                for c in range(1,int(MAZE_WIDTH/CELL_SIZE - 1), 2):
                    if nb != self.cells[r][c].nb: return False
            
            return True
    
        # Creat grid patern
        i = 0
        for r in range(1,int(MAZE_HEIGHT/CELL_SIZE - 1), 2):
            for c in range(1,int(MAZE_WIDTH/CELL_SIZE - 1), 2):
                self.cells[r][c].change_type("empty")
                self.cells[r][c].nb = i
                i += 1

        # All brekable walls
        wall_pos = []
        for r in range(1,int(MAZE_WIDTH/CELL_SIZE - 1)):
            for c in range(1,int(MAZE_WIDTH/CELL_SIZE - 1)):
                if r%2==1 and c%2==0: wall_pos.append((r,c))
                elif r%2==0 and c%2==1: wall_pos.append((r,c))

        # Break the walls
        while not is_finished():
            row, col = choice(wall_pos)
            if col % 2 == 0: nb_cell_1, nb_cell_2 = self.cells[row][col-1].nb, self.cells[row][col+1].nb
            else: nb_cell_1, nb_cell_2 = self.cells[row-1][col].nb, self.cells[row+1][col].nb

            if nb_cell_1 != nb_cell_2:
                self.cells[row][col].change_type("empty")

                for r in range(1,int(MAZE_HEIGHT/CELL_SIZE - 1), 2):
                    for c in range(1,int(MAZE_WIDTH/CELL_SIZE - 1), 2):
                        if self.cells[r][c].nb == nb_cell_2: self.cells[r][c].nb = nb_cell_1

                if not self.instant_draw: self.update_pygame()

            wall_pos.pop(wall_pos.index((row,col)))

    def gen_prism(self) -> None:
        def mark_expand_cells(pos: tuple) -> None:
            avalable_cells_for_expand = self.get_avalibles_neighbour(pos, "wall", 2)
            for cell in avalable_cells_for_expand: 
                turn_cells.append(cell[1])
                self.cells[cell[1][0]][cell[1][1]].change_type("turn")

        start_pos = (randrange(1, MAZE_WIDTH/CELL_SIZE - 1, 2), randrange(1, MAZE_HEIGHT/CELL_SIZE - 1, 2))
        turn_cells = []

        self.cells[start_pos[0]][start_pos[1]].change_type("empty")
        mark_expand_cells(start_pos)

        while len(turn_cells) != 0:
            current_pos = turn_cells.pop(turn_cells.index(choice(turn_cells)))

            avalable_cells_for_connection = self.get_avalibles_neighbour(current_pos, "empty", 2)
            connection_cell = choice(avalable_cells_for_connection)

            self.cells[current_pos[0]][current_pos[1]].change_type("empty")
            self.cells[connection_cell[0][0]][connection_cell[0][1]].change_type("empty")

            mark_expand_cells(current_pos)

            if not self.instant_draw: self.update_pygame()

    #----------Solve----------#
    def reset_solve_cells(self) -> None:
        for cell_row in self.cells:
            for cell in cell_row: 
                if cell.type == "visited" or cell.type == "path" or cell.type == "turn":
                    cell.change_type("empty")
                    cell.nb = None

    def solve(self, method: str) -> None:
        self.reset_solve_cells()

        if method == "A*": self.solve_A_star()
        else: self.solve_BFS_and_DFS(method)

    def solve_BFS_and_DFS(self, method: str) -> None:
        goal_find = False
        if method == "DFS":
            visited_cells = P.init()
            P.empile(visited_cells, [self.start_pos,0])
        elif method == "BFS":
            visited_cells = F.init()
            F.emfile(visited_cells, [self.start_pos,0])

        while not P.est_vide(visited_cells) or not F.est_vide(visited_cells):
            if method == "DFS": pos, distance = P.depile(visited_cells)
            elif method == "BFS": pos, distance = F.defile(visited_cells)

            if not goal_find:
                avalable_cells = self.get_avalibles_neighbour(pos, ["empty","goal"], 1)

                if len(avalable_cells) != 0:
                    for cell in avalable_cells:
                        if self.cells[cell[0]][cell[1]].type == "goal": 
                            if method == "DFS": visited_cells = P.init()
                            elif method == "BFS": visited_cells = F.init()
                            goal_find = True
                        else:
                            self.cells[cell[0]][cell[1]].change_type("turn")
                            self.cells[cell[0]][cell[1]].nb = distance+1
                    
                        if method == "DFS": P.empile(visited_cells, [cell, distance + 1])
                        elif method == "BFS": F.emfile(visited_cells, [cell, distance + 1])

                    if not self.instant_draw: self.update_pygame()

                if self.cells[pos[0]][pos[1]].type == "turn": self.cells[pos[0]][pos[1]].change_type("visited")

            else:
                avalable_cells = self.get_avalibles_neighbour(pos, ["visited", "start"], 1)

                for cell in avalable_cells:
                    if self.cells[cell[0]][cell[1]].type == "start": visited_cells = P.init()
                    elif self.cells[cell[0]][cell[1]].nb < distance:
                        self.cells[cell[0]][cell[1]].change_type("path")
                        if method == "DFS": P.empile(visited_cells, [cell, distance - 1])
                        elif method == "BFS": F.emfile(visited_cells, [cell, distance - 1])
                        break

                if not self.instant_draw: self.update_pygame()

    def solve_A_star(self) -> None:
        def get_neighbour_weight(pos: tuple) -> None:
            avalable_cells = self.get_avalibles_neighbour(pos, ["empty","goal"], 1)
            for cell in avalable_cells:
                if self.cells[cell[0]][cell[1]].type != "goal": self.cells[cell[0]][cell[1]].change_type("turn")

                start_distance = abs(cell[0] - self.start_pos[0]) + abs(cell[1] - self.start_pos[1])
                end_distance = abs(cell[0] - self.end_pos[0]) + abs(cell[1] - self.end_pos[1])
                global_distance = start_distance + end_distance

                self.cells[cell[0]][cell[1]].nb = self.cells[pos[0]][pos[1]].nb + 1
                expand_cells.append({"pos": cell, "cost": global_distance})

        def get_lovest_cell() -> dict:
            vals = [cell["cost"] for cell in expand_cells]
            return expand_cells.pop(vals.index(min(vals)))

        def get_path_cell(pos) -> tuple:
            avalable_cells = self.get_avalibles_neighbour(pos, ["visited","start"], 1)
            vals = [self.cells[cell[0]][cell[1]].nb for cell in avalable_cells]
            return avalable_cells[vals.index(min(vals))]

        print("test")
        expand_cells = [self.start_pos]
        current_pos = None
        self.cells[self.start_pos[0]][self.start_pos[1]].nb = 0
        get_neighbour_weight(expand_cells.pop())

        # Find the goal
        while len(expand_cells) != 0:
            current_pos = get_lovest_cell()["pos"]

            if self.cells[current_pos[0]][current_pos[1]].type == "goal": break
            else:
                self.cells[current_pos[0]][current_pos[1]].change_type("visited")
                get_neighbour_weight(current_pos)

            if not self.instant_draw: self.update_pygame()

        # Find the shortest path
        path_ended = False
        while not path_ended:
            next_cell = get_path_cell(current_pos)

            if self.cells[next_cell[0]][next_cell[1]].type == "start": path_ended = True
            else:
                self.cells[next_cell[0]][next_cell[1]].change_type("path")
                
                current_pos = next_cell

                if not self.instant_draw: self.update_pygame()

    #----------Editor----------#
    def clear_editor(self) -> None:
        for r in range(1,int(MAZE_HEIGHT/CELL_SIZE - 1)):
            for c in range(1,int(MAZE_WIDTH/CELL_SIZE - 1)):
                if self.cells[r][c].type != "start" and self.cells[r][c].type != "goal": self.cells[r][c].change_type("empty")

    def update_editor(self, cell_type: str) -> None:
        x,y = pg.mouse.get_pos()
        row, col = int(y / CELL_SIZE), int(x / CELL_SIZE)
        mouse_state = pg.mouse.get_pressed()

        if (row,col) != self.start_pos and (row,col) != self.end_pos:
            if row > 0 and row < (MAZE_HEIGHT / CELL_SIZE - 1) and col > 0 and col < (MAZE_WIDTH / CELL_SIZE - 1) and (mouse_state[0] or mouse_state[2]):
                if mouse_state[0]: 
                    if cell_type == "wall": self.cells[row][col].change_type("wall")
                    else:
                        if cell_type == "start": 
                            self.cells[self.start_pos[0]][self.start_pos[1]].change_type("empty")
                            self.start_pos = (row,col)
                            self.cells[row][col].change_type("start")
                        elif cell_type == "goal": 
                            self.cells[self.end_pos[0]][self.end_pos[1]].change_type("empty")
                            self.end_pos = (row,col)
                            self.cells[row][col].change_type("goal")
                        self.change_selected_editor_cell("wall")
                if mouse_state[2]: self.cells[row][col].change_type("empty")

    #----------Other----------#
    def update_pygame(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()

        self.draw()
        pg.display.update()
        time.sleep(0.01)

    def draw(self) -> None:
        for cell_row in self.cells: 
            for cell in cell_row: cell.draw(self.display_surface, self.draw_grid)