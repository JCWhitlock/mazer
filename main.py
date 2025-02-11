from window import Window
from primitives import Point,Line,Cell
from maze import Maze
from util import recursionlimit



def main():
    with recursionlimit(5000):

        win = Window("Maze Solver",800,600)
        maze = Maze(5,5,59,79,10,10,win)
        # maze.break_entrance_and_exit()
        

        maze.print_statistics(maze.solve())

        win.wait_for_close()

main()