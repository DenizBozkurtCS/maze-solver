from graphics import Line, Point


# Walls are 1-2-3-4 as in top-left-bottom-right
class Cell:
    def __init__(self, win=None):
        self.has_top_wall = True
        self.has_left_wall = True
        self.has_bottom_wall = True
        self.has_right_wall = True
        self.visited = False
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2

        top_wall = Line(Point(x1, y1), Point(x2, y1))
        left_wall = Line(Point(x1, y1), Point(x1, y2))
        bottom_wall = Line(Point(x1, y2), Point(x2, y2))
        right_wall = Line(Point(x2, y1), Point(x2, y2))
        if self.has_top_wall:
            self._win.draw_line(top_wall)
        else:
            self._win.draw_line(top_wall, "white")
        if self.has_left_wall:
            self._win.draw_line(left_wall)
        else:
            self._win.draw_line(left_wall, "white")
        if self.has_bottom_wall:
            self._win.draw_line(bottom_wall)
        else:
            self._win.draw_line(bottom_wall, "white")
        if self.has_right_wall:
            self._win.draw_line(right_wall)
        else:
            self._win.draw_line(right_wall, "white")

    def draw_move(self, to_cell, undo=False):
        if self._win is None:
            return

        mid_x1 = (self._x1 + self._x2) // 2
        mid_y1 = (self._y1 + self._y2) // 2
        mid_x2 = (to_cell._x1 + to_cell._x2) // 2
        mid_y2 = (to_cell._y1 + to_cell._y2) // 2
        line = Line(Point(mid_x1, mid_y1), Point(mid_x2, mid_y2))
        if undo:
            self._win.draw_line(line, "gray")
        else:
            self._win.draw_line(line, "red")
