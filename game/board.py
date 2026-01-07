import numpy as np

ROWS = 6
COLS = 7

EMPTY = 0
PLAYER_HUMAN = 1
PLAYER_AI = -1


def create_board():
    """
    Creates and returns an empty Connect-4 board.
    """
    return np.zeros((ROWS, COLS), dtype=int)


def apply_move(board, col, player):
    """
    Drops a piece into the selected column.
    Returns True if move is successful, False otherwise.
    """
    if col < 0 or col >= COLS:
        return False

    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            board[row][col] = player
            return True

    return False  # Column is full


def undo_move(board, col):
    """
    Removes the top-most piece from a column (used in Minimax).
    """
    for row in range(ROWS):
        if board[row][col] != EMPTY:
            board[row][col] = EMPTY
            return True
    return False


def is_column_full(board, col):
    """
    Checks if a column is full.
    """
    return board[0][col] != EMPTY
