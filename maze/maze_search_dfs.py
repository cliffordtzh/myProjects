maze = []
maze.append([" ", "#", "#", "#", "#", "#", "#"])
maze.append([" ", " ", " ", " ", " ", " ", " "])
maze.append([" ", "#", "#", " ", "#", "#", " "])
maze.append([" ", "#", " ", " ", " ", "#", " "])
maze.append([" ", "#", " ", "#", " ", "#", " "])
maze.append([" ", "#", " ", "#", " ", "#", " "])
maze.append([" ", "#", " ", "#", " ", "#", "#"])
maze.append([" ", " ", " ", " ", " ", " ", " "])
maze.append(["#", "#", "#", "#", "#", "#", " "])

BLOCKER = '#'

moves = dict(U = (-1, 0), D = (1, 0), L = (0, -1), R = (0, 1))
nrow = len(maze)
ncol = len(maze[0])

START = (0,0)
END = (nrow-1, ncol-1)


def valid_moves(loc, maze, visited):
    res = []
    row, col = loc

    if maze[row][col] == BLOCKER:
        return []

    for move in moves:
        x, y = moves[move]
        newx = row + x
        newy = col + y
        if 0 <= newx < nrow and 0 <= newy < ncol and maze[newx][newy] != BLOCKER \
            and (newx, newy) not in visited:
            res.append(move)

    return res


def mover(path, loc):
    row, col = loc
    for move in path:
        x, y = moves[move]
        row += x
        col += y

    return row, col


def solve(maze):
    visited = [START]
    paths = valid_moves(START, maze, visited)
    while True:
        path = paths.pop(len(paths)-1)
        current_loc = mover(path, START)
        visited.append(current_loc)
        if current_loc == END:
            return path

        possible_moves = valid_moves(current_loc, maze, visited)
        updated_moves = [path + move for move in possible_moves]
        paths.extend(updated_moves)

print(solve(maze))