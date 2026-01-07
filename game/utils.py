import numpy as np
from game.board import COLS, EMPTY


def get_valid_moves(board):
    """
    Returns a list of columns where a move is possible.
    """
    return [col for col in range(COLS) if board[0][col] == EMPTY]


def copy_board(board):
    """
    Returns a deep copy of the board.
    """
    return np.copy(board)


def board_to_tensor(board):
    """
    Converts board to ML-friendly format.
    (Used later for Neural Networks)
    """
    return board.reshape(1, 6, 7)


def print_board(board):
    """
    Debug-friendly board print (optional).
    """
    print("\n".join(["\t".join(map(str, row)) for row in board]))
    print("-" * 20)
