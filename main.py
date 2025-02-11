from window import Window
from primitives import Point,Line,Cell
from maze import Maze
from util import recursionlimit

#  7746924695169332207   32.887
#  9015897716523660400   23.213
#  6988938901544645069   26.924
#  851631408580752459    24.285
#


def main():
    with recursionlimit(5000):

        win = Window("Maze Solver",1600,1200)
        maze = Maze(5,5,59,79,20,20,win,7746924695169332207)
        # maze.break_entrance_and_exit()
        

        maze.print_statistics(maze.solve(),True)

        win.wait_for_close()

main()