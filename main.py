from tkinter import Tk, BOTH, Canvas
import time
import random

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

    @property
    def canvas(self):
        return self.__canvas

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__window_running = True
        while self.__window_running == True:
            self.redraw()

    def close(self):
        self.__window_running = False

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line():
    def __init__(self, point_1, point_2):
        if not hasattr(point_1, 'x') or not hasattr(point_1, 'y'):
            raise ValueError("point_1 must have x and y attributes.")
        if not hasattr(point_2, 'x') or not hasattr(point_2, 'y'):
            raise ValueError("point_2 must have x and y attributes.")
        
        self.point_1 = point_1
        self.point_2 = point_2

    def draw(self, window, fill_color="black", width=2):
        if window is not None:
            window.canvas.create_line(self.point_1.x, self.point_1.y, self.point_2.x, self.point_2.y, fill=fill_color, width=width)

    def __repr__(self):
        return f"Line(({self.point_1.x}, {self.point_1.y}) -> ({self.point_2.x}, {self.point_2.y}))"

class Cell():
    def __init__(self, left_top, right_bottom, window=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = left_top.x
        self.__x2 = right_bottom.x
        self.__y1 = left_top.y
        self.__y2 = right_bottom.y
        self.__win = window
        self.mid_point = Point((self.__x1 + self.__x2) / 2, (self.__y1 + self.__y2) / 2)
        self.visited = False

    def draw(self, fill_color="black"):
        if self.has_left_wall:
            left_wall = Line(Point(self.__x1, self.__y1,), Point(self.__x1, self.__y2))
            left_wall.draw(self.__win, fill_color=fill_color)
        else:
            Line(Point(self.__x1, self.__y1,), Point(self.__x1, self.__y2)).draw(self.__win, "#d9d9d9")

        if self.has_top_wall:
            top_wall = Line(Point(self.__x1, self.__y1,), Point(self.__x2, self.__y1))
            top_wall.draw(self.__win, fill_color=fill_color)
        else:
            Line(Point(self.__x1, self.__y1,), Point(self.__x2, self.__y1)).draw(self.__win, "#d9d9d9")

        if self.has_right_wall:
            right_wall = Line(Point(self.__x2, self.__y1,), Point(self.__x2, self.__y2))
            right_wall.draw(self.__win, fill_color=fill_color)
        else:
            Line(Point(self.__x2, self.__y1,), Point(self.__x2, self.__y2)).draw(self.__win, "#d9d9d9")

        if self.has_bottom_wall:
            bottom_wall = Line(Point(self.__x1, self.__y2,), Point(self.__x2, self.__y2))
            bottom_wall.draw(self.__win, fill_color=fill_color)
        else:
            Line(Point(self.__x1, self.__y2,), Point(self.__x2, self.__y2)).draw(self.__win, "#d9d9d9")

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
        self.draw()
        
    def draw_move(self, to_cell, undo=False):
        path = Line(self.mid_point, to_cell.mid_point)
        if undo:
            path.draw(self.__win, "gray")
        else:
            path.draw(self.__win, "red")

class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        window=None,
        seed=None
    ):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = window
        self._cells = []
        
        if seed:
            random.seed(seed)
        self._create_cells()

    def _create_cells(self):
        x = self.__x1
        for n in range(self.__num_cols):
            y = self.__y1
            self._cells.append([])
            for m in range(self.__num_rows):
                self._cells[n].append(Cell(Point(x, y), Point(x + self.__cell_size_x, y + self.__cell_size_y), self.__win))
                self._draw_cell(n, m)
                y += self.__cell_size_y
            x += self.__cell_size_x

    def _draw_cell(self, column, row):
        self._cells[column][row].draw()
        self._animate()

    def _animate(self):
        if self.__win is not None:
            self.__win.redraw()
            time.sleep(0.01)

    def _break_entrance_and_exit(self):
        self._cells[0][0].remove_wall("left")
        self._cells[-1][-1].remove_wall("right")

    def _break_walls_r(self, column, row):
        self._cells[column][row].visited = True
        while True:
            possible_directions = []
            
            # Check left neighbor (only if not leftmost column)
            if column > 0 and not self._cells[column - 1][row].visited:
                possible_directions.append((column - 1, row))
                
            # Check right neighbor (only if not rightmost column)
            if column < self.__num_cols - 1 and not self._cells[column + 1][row].visited:
                possible_directions.append((column + 1, row))
                
            # Check top neighbor (only if not top row)
            if row > 0 and not self._cells[column][row - 1].visited:
                possible_directions.append((column, row - 1))
                
            # Check bottom neighbor (only if not bottom row)
            if row < self.__num_rows - 1 and not self._cells[column][row + 1].visited:
                possible_directions.append((column, row + 1))

            if not possible_directions:
                self._cells[column][row].draw()
                return
            
            # Choose a random direction
            next_cell = random.choice(possible_directions)
            next_column, next_row = next_cell

            # Break walls between current cell and next cell
            if next_column < column:  # Moving left
                self._cells[column][row].remove_wall("left")
                self._cells[next_column][next_row].remove_wall("right")
            elif next_column > column:  # Moving right
                self._cells[column][row].remove_wall("right")
                self._cells[next_column][next_row].remove_wall("left")
            elif next_row < row:  # Moving up
                self._cells[column][row].remove_wall("top")
                self._cells[next_column][next_row].remove_wall("bottom")
            elif next_row > row:  # Moving down
                self._cells[column][row].remove_wall("bottom")
                self._cells[next_column][next_row].remove_wall("top")

            # Recursively visit the next cell
            self._break_walls_r(next_column, next_row)

    def _reset_cells_visited(self):
        for column in self._cells:
            for cell in column:
                cell.visited = False

    def in_bounds(self, column, row):
        return 0 <= column < len(self._cells) and 0 <= row < len(self._cells[column])

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, column, row):
        # Step 1: Animate and mark the current cell as visited
        self._animate()
        current = self._cells[column][row]
        current.visited = True

        # Step 2: Check if we've reached the end cell
        if current == self._cells[-1][-1]:  # Assuming bottom-right corner is the goal
            return True

        # Step 3: Define potential neighbors (but check bounds before accessing)
        potential_neighbours = [
            (column - 1, row, current.has_left_wall),   # Left
            (column + 1, row, current.has_right_wall),  # Right
            (column, row - 1, current.has_top_wall),    # Top
            (column, row + 1, current.has_bottom_wall)  # Bottom
        ]

        # Step 4: Iterate over valid neighbors
        for target_column, target_row, wall in potential_neighbours:
            if self.in_bounds(target_column, target_row):  # Only proceed if within bounds
                target_cell = self._cells[target_column][target_row]
                if not wall and not target_cell.visited:  # Check wall and visitation
                    # Draw a move to the target cell
                    current.draw_move(target_cell)
                    # Recursively attempt to solve from the target cell
                    if self._solve_r(target_column, target_row):
                        return True  # If solving from the target cell succeeds, bubble up True
                    else:
                        # Backtracking: Undo the move if the path didn't lead to the solution
                        current.draw_move(target_cell, undo=True)
        # If none of the neighbors lead to a solution, backtrack
        return False

def main():
    win = Window(800, 600)
    maze_1 = Maze(20, 20, 20, 20, 20, 20, win)
    maze_1._break_entrance_and_exit()
    maze_1._break_walls_r(0, 0)
    maze_1._reset_cells_visited()
    maze_1.solve()
    win.wait_for_close()

if __name__ == "__main__":
    main()