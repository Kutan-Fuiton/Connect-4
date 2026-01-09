import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# ---------------- GAME IMPORTS ----------------
from game.board import create_board, apply_move, PLAYER_HUMAN, PLAYER_AI
from game.rules import check_winner, is_draw
from game.utils import get_valid_moves

# ---------------- AI IMPORTS ----------------
from ai.random_ai import get_move as random_ai
from ai.minimax_ai import get_move as minimax_ai

# OPTIONAL (enable when DQN is ready)
try:
    from ai.hard_ai import get_move as hard_ai
    DQN_AVAILABLE = True
except ImportError:
    DQN_AVAILABLE = False

# ---------------- APP SETUP ----------------
app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- GAME STATE ----------------
class GameState:
    def __init__(self):
        self.board = create_board()
        self.game_over = False
        self.winner = 0
        self.difficulty = "easy"

game_state = GameState()

# ---------------- ROUTES ----------------

@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")


@app.get("/state")
def get_state():
    return {
        "board": game_state.board.tolist(),
        "game_over": game_state.game_over,
        "winner": int(game_state.winner),
        "difficulty": game_state.difficulty
    }


@app.post("/reset")
def reset_game(difficulty: str = "easy"):
    game_state.board = create_board()
    game_state.game_over = False
    game_state.winner = 0
    game_state.difficulty = difficulty
    return {"status": "reset"}


@app.post("/move/{col}")
def player_move(col: int):

    print("Difficulty:", game_state.difficulty)

    # ---- 1. STOP IF GAME OVER ----
    if game_state.game_over:
        return {"error": "Game is over"}

    if col not in get_valid_moves(game_state.board):
        return {"error": "Invalid move"}

    # ---- 2. HUMAN MOVE ----
    apply_move(game_state.board, col, PLAYER_HUMAN)

    # ---- 3. CHECK HUMAN WIN ----
    winner = check_winner(game_state.board)
    if winner != 0 or is_draw(game_state.board):
        game_state.game_over = True
        game_state.winner = winner
        return get_state()

    # ---- 4. AI THINKING DELAY (REALISTIC) ----
    time.sleep(0.7)

    # ---- 5. AI MOVE ----
    if game_state.difficulty == "easy":
        ai_col = random_ai(game_state.board)

    elif game_state.difficulty == "medium":
        ai_col = minimax_ai(game_state.board)

    else:  # HARD
        if DQN_AVAILABLE:
            print("Using HARD AI (DQN)")
            ai_col = hard_ai(game_state.board)
        else:
            # fallback if DQN not loaded
            ai_col = minimax_ai(game_state.board)

    if ai_col is not None:
        apply_move(game_state.board, ai_col, PLAYER_AI)

    # ---- 6. CHECK AI WIN ----
    winner = check_winner(game_state.board)
    if winner != 0 or is_draw(game_state.board):
        game_state.game_over = True
        game_state.winner = winner

    return get_state()
