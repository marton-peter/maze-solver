from tkinter import Tk, BOTH, Canvas

class Window():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, width=self.width, height=self.height)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__window_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__window_running = True
        while self.__window_running == True:
            self.redraw()

    def close(self):
        self.__window_running = False

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

    def draw_cell(self, cell, fill_color):
        cell.draw(self.__canvas, fill_color)

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line():
    def __init__(self, point_1, point_2):
        self.point_1 = point_1
        self.point_2 = point_2

    def draw(self, canvas, fill_color):
        canvas.create_line(self.point_1.x, self.point_1.y, self.point_2.x, self.point_2.y, fill=fill_color, width=2)

class Cell():
    def __init__(self, left_top, right_bottom):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = left_top.x
        self.__x2 = right_bottom.x
        self.__y1 = left_top.y
        self.__y2 = right_bottom.y

    def draw(self, canvas, fill_color):
        if self.has_left_wall:
            left_wall = Line(Point(self.__x1, self.__y1,), Point(self.__x1, self.__y2))
            left_wall.draw(canvas, fill_color)
        if self.has_top_wall:
            top_wall = Line(Point(self.__x1, self.__y1,), Point(self.__x2, self.__y1))
            top_wall.draw(canvas, fill_color)
        if self.has_right_wall:
            right_wall = Line(Point(self.__x2, self.__y1,), Point(self.__x2, self.__y2))
            right_wall.draw(canvas, fill_color)
        if self.has_bottom_wall:
            bottom_wall = Line(Point(self.__x1, self.__y2,), Point(self.__x2, self.__y2))
            bottom_wall.draw(canvas, fill_color)

    def remove_wall(self, wall_name):
        if wall_name == 'left':
            self.has_left_wall = False
        elif wall_name == 'right':
            self.has_right_wall = False
        elif wall_name == 'top':
            self.has_top_wall = False
        elif wall_name == 'bottom':
            self.has_bottom_wall = False
        else:
            raise ValueError("Invalid wall name specified. Use 'left', 'right', 'top', or 'bottom'.")

def main():
    win = Window(800, 600)
    p1 = Point(100, 100)
    p2 = Point(200, 200)
    cell_1 = Cell(p1, p2)
    cell_1.remove_wall("top")
    win.draw_cell(cell_1, "black")
    win.wait_for_close()

if __name__ == "__main__":
    main()