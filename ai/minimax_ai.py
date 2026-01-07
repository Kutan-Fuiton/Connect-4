import math
import random
from game.board import apply_move, undo_move, PLAYER_AI, PLAYER_HUMAN, COLS
from game.rules import check_winner, is_draw
from game.utils import get_valid_moves, copy_board

MAX_DEPTH = 4


def evaluate_window(window):
    """
    Scores a group of 4 cells.
    """
    score = 0

    if window.count(PLAYER_AI) == 4:
        score += 100000
    elif window.count(PLAYER_AI) == 3 and window.count(0) == 1:
        score += 100
    elif window.count(PLAYER_AI) == 2 and window.count(0) == 2:
        score += 10

    if window.count(PLAYER_HUMAN) == 3 and window.count(0) == 1:
        score -= 120
    elif window.count(PLAYER_HUMAN) == 2 and window.count(0) == 2:
        score -= 10

    return score


def evaluate_board(board):
    """
    Heuristic evaluation of the board.
    """
    score = 0
    rows, cols = board.shape

    # Center column preference
    center_col = cols // 2
    center_count = list(board[:, center_col]).count(PLAYER_AI)
    score += center_count * 6

    # Horizontal
    for r in range(rows):
        for c in range(cols - 3):
            window = list(board[r, c:c + 4])
            score += evaluate_window(window)

    # Vertical
    for c in range(cols):
        for r in range(rows - 3):
            window = list(board[r:r + 4, c])
            score += evaluate_window(window)

    # Diagonal (bottom-left → top-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window)

    # Diagonal (top-left → bottom-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            window = [board[r - i][c + i] for i in range(4)]
            score += evaluate_window(window)

    return score


def minimax(board, depth, alpha, beta, maximizing):
    """
    Minimax algorithm with alpha-beta pruning.
    """
    winner = check_winner(board)
    valid_moves = get_valid_moves(board)

    if winner == PLAYER_AI:
        return None, 1000000
    elif winner == PLAYER_HUMAN:
        return None, -1000000
    elif is_draw(board) or depth == 0:
        return None, evaluate_board(board)

    if maximizing:
        value = -math.inf
        best_col = random.choice(valid_moves)

        for col in valid_moves:
            temp_board = copy_board(board)
            apply_move(temp_board, col, PLAYER_AI)
            _, new_score = minimax(temp_board, depth - 1, alpha, beta, False)

            if new_score > value:
                value = new_score
                best_col = col

            alpha = max(alpha, value)
            if alpha >= beta:
                break

        return best_col, value

    else:
        value = math.inf
        best_col = random.choice(valid_moves)

        for col in valid_moves:
            temp_board = copy_board(board)
            apply_move(temp_board, col, PLAYER_HUMAN)
            _, new_score = minimax(temp_board, depth - 1, alpha, beta, True)

            if new_score < value:
                value = new_score
                best_col = col

            beta = min(beta, value)
            if alpha >= beta:
                break

        return best_col, value


def get_move(board):
    """
    Public API: returns best column for AI move.
    """
    col, _ = minimax(board, MAX_DEPTH, -math.inf, math.inf, True)
    return col
