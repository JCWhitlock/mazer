import sys
import time
import random
from primitives import Cell,Point
from window import Window

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win,
        seed=None,
        random_goals=False
    ):
        self.x = x1
        self.y = y1
        self.rows = num_rows
        self.cols = num_cols
        self.cell_width = cell_size_x
        self.cell_height = cell_size_y
        self._win = win
        self._cells = []
        self.maze_seed = seed
        if seed is not None:
            random.seed(seed)
        else:
            self.maze_seed = random.randint(0, sys.maxsize)
            random.seed(self.maze_seed)
        self._create_cells()
        self._break_entrance_and_exit(random_goals)
        self._break_walls_r(self.start_point.x,self.start_point.y)
        self._reset_cells_visited()

    def _reset_cells_visited(self):
        for col in range(len(self._cells)):
            for row in range(len(self._cells[col])):
                self._cells[col][row].visited = False
    
    def _create_cells(self):
        for col in range(0,self.cols):
            self._cells.append([])
            for row in range(0,self.rows):
                cell_origin_x = self.x + (col * self.cell_width)
                cell_origin_y = self.y + (row * self.cell_height)
                self._cells[col].append(Cell(Point(cell_origin_x, cell_origin_y), Point(cell_origin_x + self.cell_width, cell_origin_y + self.cell_height), self._win))
        for col in range(len(self._cells)):
            for row in range(len(self._cells[col])):
                self._draw_cell(col,row,0)
        self._gen_touchedcount = 0
        self._gen_endtouched = False
        self._solve_multiplechoice = 0
    
    def _draw_cell(self, col, row, timing=0.01):
        cell = self._cells[col][row]
        cell.draw("black")
        self._animate(timing)
    
    def _animate(self, timing=0.01):
        self._win.redraw()
        time.sleep(timing)

    def _break_entrance_and_exit(self, rand=False):
        cols = len(self._cells)
        rows = len(self._cells[0])
        self.start_point = Point(0,0)
        self.end_point = Point(self.cols-1,self.rows-1)
        if rand:
            self.start_point.x = random.randrange(self.cols)
            self.end_point.x = random.randrange(self.cols)
        self._cells[self.start_point.x][self.start_point.y].has_top_wall = False
        self._cells[self.end_point.x][self.end_point.y].has_bottom_wall = False
        self._draw_cell(self.start_point.x,self.start_point.y)
        self._draw_cell(self.end_point.x,self.end_point.y)
    
    def _up_coords(self, i, j):
        return (i, j-1, "up")
    
    def _down_coords(self, i, j):
        return (i, j+1, "down")

    def _left_coords(self,i,j):
        return (i-1, j, "left")

    def _right_coords(self,i,j):
        return (i+1, j, "right")

    def _cell_ref(self, coords):
        return self._cells[coords[0]][coords[1]]

    def _break_walls_r(self, i, j):
        # print(f"calling break walls {i},{j}")
        self._cells[i][j].visited = True
        if i == self.end_point.x and j == self.end_point.y:
            self._gen_endtouched = True
        elif self._gen_endtouched != True:
            self._gen_touchedcount += 1
        while True:
            moves = []
            # test left
            if i > 0 and self._cell_ref(self._left_coords(i,j)).visited == False:
                moves.append(self._left_coords(i,j))
            # test right
            if i < self.cols - 1 and self._cell_ref(self._right_coords(i,j)).visited == False:
                moves.append(self._right_coords(i,j))
            # test up
            if j > 0 and self._cell_ref(self._up_coords(i,j)).visited == False:
                moves.append(self._up_coords(i,j))
            # test down
            if j < self.rows - 1 and self._cell_ref(self._down_coords(i,j)).visited == False:
                moves.append(self._down_coords(i,j))   

            if len(moves) == 0:
                self._draw_cell(i,j, 0.0025)
                return

            selection = random.randrange(len(moves))
            next_coord = moves[selection]

            # print(f"breaking {next_coord}")

            match next_coord[2]:
                case "up":
                    self._cells[i][j].has_top_wall = False
                    self._cell_ref(next_coord).has_bottom_wall = False
                case "down":
                    self._cells[i][j].has_bottom_wall = False
                    self._cell_ref(next_coord).has_top_wall = False
                case "left":
                    self._cells[i][j].has_left_wall = False
                    self._cell_ref(next_coord).has_right_wall = False
                case "right":
                    self._cells[i][j].has_right_wall = False
                    self._cell_ref(next_coord).has_left_wall = False
             
            self._break_walls_r(next_coord[0], next_coord[1])
            
    def solve(self):
        return self._solve_r(self.start_point.x, self.start_point.y)

    def print_statistics(self, was_solved, mark_branches=False):
        print(f"Maze Was Solved = {was_solved}")
        visited_cells = 0
        bad_cells = 0
        good_path_length = 0
        good_path_branches = 0
        total_cells = self.rows * self.cols
        for col in range(len(self._cells)):
            for row in range(len(self._cells[col])):
                cell = self._cells[col][row]
                walls = cell.get_wall_count()

                if cell.visited:
                    visited_cells += 1
                if cell.false_path:
                    bad_cells += 1
                else:
                    good_path_length += 1
                    if col == self.start_point.x and row == self.start_point.y and walls < 2:
                        good_path_branches += 1
                        if mark_branches:
                            cell.fill_with_color("green")
                    elif (col != self.end_point.x or row != self.end_point.y) and walls < 2:
                        good_path_branches += 1
                        if mark_branches:
                            cell.fill_with_color("green")
                     
        
        mp_ratio = good_path_length / total_cells
        conf_rating = (visited_cells - good_path_length) / good_path_length

        print(f"Generated Maze Seed: {self.maze_seed}")
        print(f"Total Cell Count = {total_cells}")
        print(f"MazeGen Touched Cells before End Cell = {self._gen_touchedcount}")
        print(f"Visited Cell Count = {visited_cells}")
        print(f"Correct Path Length = {good_path_length}")
        print(f"Wrong Cells Visited = {visited_cells - good_path_length}")

        print(f"Multiple Choice Branches in Solution = {good_path_branches}")

        print(f"Main Path Ratio = {mp_ratio}")
        print(f"Confusion Rating = {conf_rating}")

        score = ((total_cells // 1000) + (good_path_branches // 2)) * conf_rating
        print(f"Difficulty Score = {score}")
        if score < 5:
            print("VERY EASY")
        elif score < 10:
            print("EASY")
        elif score < 20:
            print("MEDIUM")
        elif score < 50:
            print("HARD")
        else:
            print("VERY HARD")



    def _solve_r(self,i,j):
        self._animate(0.005)
        self._cells[i][j].visited = True
        if i == self.end_point.x and j == self.end_point.y:
            self._cells[i][j].false_path = False
            return True
        moves = []
        curr_cell = self._cells[i][j]
        
        if self.end_point.x - i > self.end_point.y - j:
            if i > self.end_point.x:
                # test left
                if i > 0 and curr_cell.has_left_wall == False and self._cell_ref(self._left_coords(i,j)).visited == False:
                    moves.append(self._left_coords(i,j))
            else:
                # test right
                if i < self.cols - 1 and curr_cell.has_right_wall == False and self._cell_ref(self._right_coords(i,j)).visited == False:
                    moves.append(self._right_coords(i,j))
            # test down
            if j < self.rows - 1 and curr_cell.has_bottom_wall == False and self._cell_ref(self._down_coords(i,j)).visited == False:
                moves.append(self._down_coords(i,j))
        else:
            # test down
            if j < self.rows - 1 and curr_cell.has_bottom_wall == False and self._cell_ref(self._down_coords(i,j)).visited == False:
                moves.append(self._down_coords(i,j))
            if i > self.end_point.x:
                # test left
                if i > 0 and curr_cell.has_left_wall == False and self._cell_ref(self._left_coords(i,j)).visited == False:
                    moves.append(self._left_coords(i,j))
            else:
                # test right
                if i < self.cols - 1 and curr_cell.has_right_wall == False and self._cell_ref(self._right_coords(i,j)).visited == False:
                    moves.append(self._right_coords(i,j))
        # test up
        if j > 0 and curr_cell.has_top_wall == False and self._cell_ref(self._up_coords(i,j)).visited == False:
            moves.append(self._up_coords(i,j))
        if i <= self.end_point.x:
            # test left
            if i > 0 and curr_cell.has_left_wall == False and self._cell_ref(self._left_coords(i,j)).visited == False:
                moves.append(self._left_coords(i,j))
        else:
            # test right
            if i < self.cols - 1 and curr_cell.has_right_wall == False and self._cell_ref(self._right_coords(i,j)).visited == False:
                moves.append(self._right_coords(i,j))
        
        # if len(moves) > 1:
        #    self._solve_multiplechoice += 1
        
        for move in moves:
            curr_cell.draw_move(self._cell_ref(move))
            result = self._solve_r(move[0],move[1])
            if result:
                self._cell_ref(move).false_path = False
                if self._cell_ref(move).get_wall_count() < 2:
                    self._solve_multiplechoice += 1
                # curr_cell.draw_move(self._cell_ref(move))
                return True
            
            else:
                curr_cell.draw_move(self._cell_ref(move), True)
        
        # if len(moves) > 1:
        #    self._solve_multiplechoice -= 1

        return False



