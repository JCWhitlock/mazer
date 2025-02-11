from tkinter import Tk, BOTH, Canvas

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point0, point1):
        self.p0 = point0
        self.p1 = point1
    
    def draw(self, canvas, fill_color):
        canvas.create_line(self.p0.x, self.p0.y, self.p1.x, self.p1.y, fill=fill_color, width=2)

class Cell:
    def __init__(self, point0, point1, window):
        self.__x0 = point0.x
        self.__x1 = point1.x
        self.__y0 = point0.y
        self.__y1 = point1.y
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__window = window
        self.visited = False
        self.false_path = True
        self._first_draw = True
    
    def get_center_point(self):
        return Point((self.__x0 + self.__x1) // 2, (self.__y0 + self.__y1) // 2)

    def get_wall_count(self):
        return (1 if self.has_top_wall else 0) + (1 if self.has_bottom_wall else 0) + (1 if self.has_left_wall else 0) + (1 if self.has_right_wall else 0)

    def draw(self, color):
        offset = 0
        if not self._first_draw:
            offset = 1
        self.__window.draw_line(Line(Point(self.__x0 + offset,self.__y0), Point(self.__x1 - offset,self.__y0)), color if self.has_top_wall else self.__window.bg_color)
        self.__window.draw_line(Line(Point(self.__x1,self.__y0 + offset),Point(self.__x1,self.__y1 - offset)), color if self.has_right_wall else self.__window.bg_color)
        self.__window.draw_line(Line(Point(self.__x0 + offset,self.__y1),Point(self.__x1 - offset,self.__y1)), color if self.has_bottom_wall else self.__window.bg_color)
        self.__window.draw_line(Line(Point(self.__x0,self.__y0 + offset),Point(self.__x0,self.__y1 - offset)), color if self.has_left_wall else self.__window.bg_color)
        self._first_draw = False

    def draw_move(self, to_cell, undo=False):
        color = "red"
        if undo:
            color = "gray"
        self.__window.draw_line(Line(self.get_center_point(), to_cell.get_center_point()), color)
    