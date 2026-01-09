import numpy as np
import torch

from ai.dqn_model import DQN
from ai.minimax_ai import get_move as minimax_move

from game.board import apply_move, PLAYER_AI, PLAYER_HUMAN
from game.rules import check_winner
from game.utils import get_valid_moves


ROWS, COLS = 6, 7

# Load trained DQN model
model = DQN()
model.load_state_dict(torch.load("dqn_model.pt", map_location="cpu"))
model.eval()


def get_move(board):
    board = np.array(board)
    valid_moves = get_valid_moves(board)

    # ---------- 1️⃣ Immediate winning move ----------
    for col in valid_moves:
        temp = board.copy()
        apply_move(temp, col, PLAYER_AI)
        if check_winner(temp) == PLAYER_AI:
            return col

    # ---------- 2️⃣ Immediate block ----------
    for col in valid_moves:
        temp = board.copy()
        apply_move(temp, col, PLAYER_HUMAN)
        if check_winner(temp) == PLAYER_HUMAN:
            return col

    # ---------- 3️⃣ Neural Network decision ----------
    state = torch.tensor(board.flatten(), dtype=torch.float32)

    with torch.no_grad():
        q_values = model(state)

    # Mask invalid columns
    for c in range(COLS):
        if c not in valid_moves:
            q_values[c] = -1e9

    nn_col = int(torch.argmax(q_values).item())

    # ---------- 4️⃣ Safety check ----------
    temp = board.copy()
    apply_move(temp, nn_col, PLAYER_AI)

    for col in get_valid_moves(temp):
        temp2 = temp.copy()
        apply_move(temp2, col, PLAYER_HUMAN)
        if check_winner(temp2) == PLAYER_HUMAN:
            # Unsafe NN move → fallback
            return minimax_move(board)

    return nn_col
