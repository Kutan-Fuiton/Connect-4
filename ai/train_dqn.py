import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from ai.dqn_model import DQN
from ai.replay_buffer import ReplayBuffer

from game.board import create_board, apply_move, PLAYER_AI, PLAYER_HUMAN
from game.rules import check_winner, is_draw
from game.utils import get_valid_moves


# ---------------- CONFIG ----------------
GAMMA = 0.99
LR = 1e-4
BATCH_SIZE = 128
BUFFER_SIZE = 100_000
TARGET_UPDATE = 1000

EPS_START = 1.0
EPS_END = 0.05
EPS_DECAY = 500_000

NUM_EPISODES = 500_000
DEVICE = "cpu"


# ---------------- MODELS ----------------
policy_net = DQN().to(DEVICE)
target_net = DQN().to(DEVICE)
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

optimizer = optim.Adam(policy_net.parameters(), lr=LR)
memory = ReplayBuffer(BUFFER_SIZE)

steps_done = 0


# ---------------- HELPERS ----------------
def select_action(state, board):
    global steps_done

    eps = EPS_END + (EPS_START - EPS_END) * np.exp(-steps_done / EPS_DECAY)
    steps_done += 1

    valid_moves = get_valid_moves(board)

    if random.random() < eps:
        return random.choice(valid_moves)

    with torch.no_grad():
        q = policy_net(torch.tensor(state, dtype=torch.float32))
        for c in range(7):
            if c not in valid_moves:
                q[c] = -1e9
        return int(torch.argmax(q).item())


def optimize():
    if len(memory) < BATCH_SIZE:
        return

    states, actions, rewards, next_states, dones = memory.sample(BATCH_SIZE)

    q_values = policy_net(states).gather(1, actions.unsqueeze(1)).squeeze(1)

    with torch.no_grad():
        next_q = target_net(next_states).max(1)[0]
        target = rewards + GAMMA * next_q * (1 - dones)

    loss = nn.SmoothL1Loss()(q_values, target)

    optimizer.zero_grad()
    loss.backward()
    nn.utils.clip_grad_norm_(policy_net.parameters(), 1.0)
    optimizer.step()


# ---------------- TRAIN LOOP ----------------
for episode in range(NUM_EPISODES):
    board = create_board()
    state = board.flatten()
    done = False

    current_player = PLAYER_AI

    while not done:
        if current_player == PLAYER_AI:
            action = select_action(state, board)
            apply_move(board, action, PLAYER_AI)

            winner = check_winner(board)
            draw = is_draw(board)

            if winner == PLAYER_AI:
                reward = 1.0
                done = True
            elif draw:
                reward = 0.2
                done = True
            else:
                reward = -0.01

            next_state = board.flatten()
            memory.push(state, action, reward, next_state, done)
            state = next_state

            optimize()
            current_player = PLAYER_HUMAN

        else:
            # Opponent plays random (curriculum later)
            opp_move = random.choice(get_valid_moves(board))
            apply_move(board, opp_move, PLAYER_HUMAN)

            if check_winner(board) == PLAYER_HUMAN:
                memory.push(state, action, -1.0, board.flatten(), True)
                done = True
            elif is_draw(board):
                done = True
            else:
                current_player = PLAYER_AI

    if episode % TARGET_UPDATE == 0:
        target_net.load_state_dict(policy_net.state_dict())

    if episode % 10_000 == 0:
        print(f"Episode {episode}")

# ---------------- SAVE ----------------
torch.save(policy_net.state_dict(), "dqn_model.pt")
print("Training complete. Model saved.")
