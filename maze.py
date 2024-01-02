from cell import Cell
import random
import time


class Maze:
    def __init__(
        self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        if seed:
            self._seed = random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)

        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cell(0, 0)
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True

        while True:
            next_index_list = []

            if i > 0 and not self._cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))

            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))

            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))

            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))

            if len(next_index_list) == 0:
                self._draw_cell(i, j)
                break

            next_cell = random.choice(next_index_list)
            if next_cell[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            if next_cell[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i - 1][j].has_left_wall = False
            if next_cell[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i - 1][j].has_bottom_wall = False
            if next_cell[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i - 1][j].has_top_wall = False

            self._break_walls_r(next_cell[0], next_cell[1])

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        result = self._solve_r(0, 0)
        return result

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True

        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        cell = self._cells[i][j]

        if i > 0 and not cell.has_left_wall and not self._cells[i - 1][j].visited:
            cell.draw_move(self._cells[i - 1][j])
            result = self._solve_r(i - 1, j)
            if result:
                return result
            else:
                cell.draw_move(self._cells[i - 1][j], undo=True)
        if (
            i < self._num_cols - 1
            and not cell.has_right_wall
            and not self._cells[i + 1][j].visited
        ):
            cell.draw_move(self._cells[i + 1][j])
            result = self._solve_r(i + 1, j)
            if result:
                return result
            else:
                cell.draw_move(self._cells[i - 1][j], undo=True)

        if j > 0 and not cell.has_top_wall and not self._cells[i][j - 1].visited:
            cell.draw_move(self._cells[i][j - 1])
            result = self._solve_r(i, j - 1)
            if result:
                return result
            else:
                cell.draw_move(self._cells[i - 1][j], undo=True)

        if (
            j < self._num_rows - 1
            and not cell.has_bottom_wall
            and not self._cells[i][j + 1].visited
        ):
            cell.draw_move(self._cells[i][j + 1])
            result = self._solve_r(i, j + 1)
            if result:
                return result
            else:
                cell.draw_move(self._cells[i][j + 1], undo=True)

        return False
