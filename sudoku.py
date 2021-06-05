from copy import deepcopy


class Group(set):
    def __init__(self, values=None):
        super(Group, self).__init__()
        if values is not None:
            for i in values:
                self.add(i)
        else:
            for i in range(1, 9 + 1):
                self.add(i)


class Grid:
    def __init__(self, *, rows=None, columns=None, squares=None, values=None):
        self.rows = {i: Group() for i in range(1, 9 + 1)} \
            if rows is None else rows
        self.columns = {i: Group() for i in range(1, 9 + 1)} \
            if columns is None else columns
        self.squares = {i: Group() for i in range(1, 9 + 1)} \
            if squares is None else squares
        self.values = {(x, y): 0 for x in range(1, 9+1) for y in range(1, 9+1)} \
            if values is None else values

    def __deepcopy__(self, memo):
        return Grid(rows=deepcopy(self.rows),
                    columns=deepcopy(self.columns),
                    squares=deepcopy(self.squares),
                    values=deepcopy(self.values))

    def get_value(self, x, y):
        # return x, y, (x-1)//3*3 + (y-1)//3 + 1
        return self.values[x, y]

    def get_groups(self, x, y):
        # return x, y, (x-1)//3*3 + (y-1)//3 + 1
        return self.rows[x], self.columns[y], self.squares[(x-1)//3*3 + (y-1)//3 + 1]

    def remaining(self, x, y):
        return set.intersection(*self.get_groups(x, y))

    def specify(self, x, y, value):
        self.values[x, y] = value
        for group in self.get_groups(x, y):
            group.discard(value)

    def guess(self, x, y, value):
        self.values[x, y] = value
        for group in self.get_groups(x, y):
            group.remove(value)

    def undo_guess(self, x, y, value):
        self.values[x, y] = 0
        for group in self.get_groups(x, y):
            group.add(value)

    def __str__(self):
        out = []
        for y in range(1, 9+1):
            out.append(' ')
            for x in range(1, 9+1):
                out.append(str(i if (i := self.get_value(x, y)) != 0 else '.'))
                if x == 3 or x == 6:
                    out.append(' │ ')
                else:
                    out.append(' ')
            if y == 3 or y == 6:
                out.append('\n───────┼───────┼───────\n')
            elif y != 9:
                out.append('\n')
        return ''.join(out)

    def next_cell(self):
        min_found = None, None, None
        min_remaining = 9
        for y in range(1, 9+1):
            for x in range(1, 9+1):
                if self.get_value(x, y) == 0:
                    remaining = self.remaining(x, y)
                    if len(remaining) < min_remaining:
                        min_remaining = len(remaining)
                        min_found = x, y, remaining

        # for y in range(1, 9+1):
        #     for x in range(1, 9+1):
        #         # print(x, y, self.get_value(x, y))
        #         if self.get_value(x, y) == min_remaining:
        #             return x, y, self.remaining(x, y)
        # print(min_remaining, end='\t')
        return min_found


def read_grid(filename):
    grid = Grid()
    with open(filename, 'r') as f:
        data = f.read()
        i = 0
        for y in range(1, 9+1):
            for x in range(1, 9+1):
                grid.specify(x, y, int(data[i]) if data[i] in '123456789' else 0)
                i += 1
                while i < len(data) and data[i].isspace():
                    i += 1
    return grid


def solve_step(grid):
    x, y, remaining = grid.next_cell()
    if x is None and y is None:
        return [deepcopy(grid)]  # all cells assigned, found a solution
    if len(remaining) == 0:
        return []  # bad guess, not a solution, backtrack

    solutions = []
    for guess in remaining:
        # print("guess:", (x, y), '<-', guess, '<-', remaining)
        grid.guess(x, y, guess)
        # print(grid)
        solutions += solve_step(grid)
        # if solutions > 1:
        #     return solutions  # already know multiple solutions
        # print("undo_guess:", (x, y), '<-', guess, '<-', remaining)
        grid.undo_guess(x, y, guess)
    return solutions


def solve(grid):
    print(grid)
    print()
    solutions = solve_step(grid)
    if len(solutions) == 1:
        print("Solved!")
        print()
        print(solutions.pop())
    elif len(solutions) > 1:
        print(f"{len(solutions)} solutions found")
    elif len(solutions) == 0:
        print("Unsolvable")


if __name__ == "__main__":
    solve(read_grid('grid.txt'))
