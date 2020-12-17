initial_board = [
    [7, 8, 5, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]


def solve(board):
    """
    Recursive function that preforms backtracking in order to fill the board correctly.
    :param board: Our game's board we would like to solve.
    :return Returns true if the the function finished solving the board, false otherwise.
    """
    empty_cell = find_empty(board)
    if not empty_cell:
        return True
    else:
        row, col = empty_cell

    for i in range(1, 10):
        if is_valid(board, i, (row, col)):
            board[row][col] = i
            if solve(board):
                return True
            board[row][col] = 0
    return False


def is_valid(board, value, pos):
    """
    Checks if the cell that the function got is valid on the board.
    :param board: The board to check on.
    :param value: The value of the cell we wants to locate.
    :param pos: The position of the cell.
    :return: True if it is valid on the board, false otherwise.
    """
    # Check row
    for i in range(len(board[0])):
        if board[pos[0]][i] == value and pos[1] != i:
            return False
    # Check column
    for i in range(len(board)):
        if board[i][pos[1]] == value and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == value and (i, j) != pos:
                return False
    return True


def find_empty(board):
    """
    Looking for an empty cell in the board, if their isn't return None.
    :param board: Our game's board we would like to solve.
    :return: Empty index in order to generate number in this index.
    """
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return i, j  # row, col
    return None


def print_board(board):
    """
    Prints the board.
    :param board: The board to print.
    """
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")


def game_maneger():
    """
    Starts the game and controls the functions.
    """
    print("\nBefore solving: \n")
    print_board(initial_board)
    solve(initial_board)
    print("\nSolved: \n")
    print_board(initial_board)


if __name__ == '__main__':
    game_maneger()
