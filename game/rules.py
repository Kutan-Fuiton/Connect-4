from game.board import ROWS, COLS, EMPTY


def check_winner(board):
    """
    Returns:
    1  -> Human wins
    -1 -> AI wins
    0  -> No winner
    """

    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            window = board[r, c:c + 4]
            if abs(sum(window)) == 4:
                return window[0]

    # Vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            window = board[r:r + 4, c]
            if abs(sum(window)) == 4:
                return window[0]

    # Diagonal (bottom-left to top-right)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r + i][c + i] for i in range(4)]
            if abs(sum(window)) == 4:
                return window[0]

    # Diagonal (top-left to bottom-right)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            window = [board[r - i][c + i] for i in range(4)]
            if abs(sum(window)) == 4:
                return window[0]

    return 0


def is_draw(board):
    """
    Returns True if board is full and no winner.
    """
    return EMPTY not in board[0]
