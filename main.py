import os

import cv2
import imutils
import numpy as np
from imutils import contours
from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border

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


def board_extractor():
    cv2.namedWindow("Sudoku")
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 3)
        thresh = cv2.adaptiveThreshold(blurred, 255,
                                       cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        thresh = cv2.bitwise_not(thresh)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        puzzleCnt = None
        # loop over the contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                puzzleCnt = approx
                break
        output = frame.copy()
        cv2.drawContours(output, [puzzleCnt], -1, (0, 255, 0), 2)

        puzzle = four_point_transform(frame, puzzleCnt.reshape(4, 2))
        warped = four_point_transform(gray, puzzleCnt.reshape(4, 2))
        cv2.imshow("Puzzle Transform", puzzle)
        cv2.waitKey(1)
        return (puzzle, warped)


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


def input_checker(board):
    """
    Checks if the input board that provided is valid
    :param board: The board to check on
    :return: True if valid, false if not.
    """
    if not find_empty(board):
        return True
    return False


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


def game_manager():
    """
    Starts the game and controls the functions.
    """
    print("\nBefore solving: \n")
    print_board(initial_board)
    solve(initial_board)
    print("\nSolved: \n")
    if not input_checker(initial_board):
        print("Sorry, the board you provided is not valid! ")
    else:
        print_board(initial_board)


if __name__ == '__main__':
    # game_manager()
    board_extractor()
