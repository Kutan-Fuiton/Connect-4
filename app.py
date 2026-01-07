from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time

from game.board import (
    create_board,
    apply_move,
    PLAYER_HUMAN,
    PLAYER_AI
)
from game.rules import check_winner, is_draw
from game.utils import get_valid_moves
from ai.random_ai import get_move as random_ai
from ai.minimax_ai import get_move as minimax_ai


app = FastAPI(title="Connect-4 AI Backend")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- In-memory Game State ----------
game_state = {
    "board": create_board(),
    "game_over": False,
    "winner": 0,
    "difficulty": "easy"
}


# ---------- API Endpoints ----------

@app.get("/state")
def get_state():
    return {
        "board": game_state["board"].tolist(),
        "game_over": game_state["game_over"],
        "winner": game_state["winner"]
    }


@app.post("/reset")
def reset_game(difficulty: str = "easy"):
    game_state["board"] = create_board()
    game_state["game_over"] = False
    game_state["winner"] = 0
    game_state["difficulty"] = difficulty
    return {"status": "reset"}


@app.post("/move/{col}")
def player_move(col: int):
    if game_state["game_over"]:
        return {"error": "Game is over"}

    if col not in get_valid_moves(game_state["board"]):
        return {"error": "Invalid move"}

    # Human move
    apply_move(game_state["board"], col, PLAYER_HUMAN)

    winner = check_winner(game_state["board"])
    if winner or is_draw(game_state["board"]):
        game_state["game_over"] = True
        game_state["winner"] = winner
        return get_state()

    # Pause (human-like)
    time.sleep(0.6)

    # AI move
    ai_col = (
        random_ai(game_state["board"])
        if game_state["difficulty"] == "easy"
        else minimax_ai(game_state["board"])
    )

    if ai_col is not None:
        apply_move(game_state["board"], ai_col, PLAYER_AI)

    winner = check_winner(game_state["board"])
    if winner or is_draw(game_state["board"]):
        game_state["game_over"] = True
        game_state["winner"] = winner

    return get_state()
