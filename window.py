from tkinter import Tk, BOTH, Canvas



class Window:
    def __init__(self, title, width, height):
        self.__root = Tk()
        self.__root.title(title)
        self.bg_color = "white"
        self.__canvas = Canvas(self.__root, bg=self.bg_color, height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

    def fill_region(self, point0, point1, fill_color):
        self.__canvas.create_rectangle(point0.x, point0.y, point1.x, point1.y, fill=fill_color, stipple="gray50", outline=fill_color, outlinestipple="gray50")