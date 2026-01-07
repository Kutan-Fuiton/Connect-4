import random
from game.utils import get_valid_moves


def get_move(board):
    """
    Selects a random valid column.
    Used for Easy difficulty.
    """
    valid_moves = get_valid_moves(board)

    if not valid_moves:
        return None  # No possible moves (draw)

    return random.choice(valid_moves)
