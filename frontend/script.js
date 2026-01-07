const API_URL = "http://127.0.0.1:8000";

const ROWS = 6;
const COLS = 7;

const boardDiv = document.getElementById("board");
const statusDiv = document.getElementById("status");

let isLocked = false;

document.addEventListener("DOMContentLoaded", () => {
    loadGame();
});

async function loadGame() {
    const res = await fetch(`${API_URL}/state`);
    const data = await res.json();
    renderBoard(data.board);
    updateStatus(data);
}

async function resetGame(difficulty = "easy") {
    await fetch(`${API_URL}/reset?difficulty=${difficulty}`, {
        method: "POST"
    });
    isLocked = false;
    loadGame();
}

async function playMove(col) {
    if (isLocked) return;

    isLocked = true;

    const res = await fetch(`${API_URL}/move/${col}`, {
        method: "POST"
    });

    const data = await res.json();
    renderBoard(data.board);
    updateStatus(data);

    isLocked = false;
}

function renderBoard(board) {
    boardDiv.innerHTML = "";

    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            const cell = document.createElement("div");
            cell.classList.add("cell");

            if (board[r][c] === 1) {
                const token = document.createElement("div");
                token.classList.add("token", "red");
                cell.appendChild(token);
            }

            if (board[r][c] === 2) {
                const token = document.createElement("div");
                token.classList.add("token", "yellow");
                cell.appendChild(token);
            }

            boardDiv.appendChild(cell);
        }
    }
}

function updateStatus(data) {
    statusDiv.className = "status";

    if (data.game_over) {
        if (data.winner === 1) {
            statusDiv.textContent = "🎉 You win!";
            statusDiv.classList.add("win");
        } else if (data.winner === 2) {
            statusDiv.textContent = "🤖 AI wins!";
            statusDiv.classList.add("lose");
        } else {
            statusDiv.textContent = "🤝 Draw!";
            statusDiv.classList.add("draw");
        }
    } else {
        statusDiv.textContent = "🔴 Your turn";
    }
}

function onColumnClick(col) {
    if (isLocked) return;
    playMove(col);
}

const clickRow = document.getElementById("click-row");
for (let c = 0; c < COLS; c++) {
    const colDiv = document.createElement("div");
    colDiv.classList.add("click-col");
    colDiv.onclick = () => onColumnClick(c);
    clickRow.appendChild(colDiv);
}