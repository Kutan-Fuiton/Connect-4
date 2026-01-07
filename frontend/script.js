// Config
const ROWS = 6;
const COLS = 7;

// DOM Elements
const boardElement = document.getElementById("board");
const clickRow = document.getElementById("click-row");
const statusDiv = document.getElementById("status");
const difficultySelect = document.getElementById("difficulty-select");
const resetBtn = document.getElementById("reset-btn");

const modal = document.getElementById("result-modal");
const modalTitle = document.getElementById("modal-title");
const modalMessage = document.getElementById("modal-message");
const modalEmoji = document.getElementById("modal-emoji");

let isProcessing = false;

// Init
document.addEventListener("DOMContentLoaded", () => {
    buildGridHTML();
    initClickAreas();
    resetGame();
});

// Build grid
function buildGridHTML() {
    boardElement.innerHTML = "";
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            const cell = document.createElement("div");
            cell.classList.add("cell");
            cell.id = `cell-${r}-${c}`;
            boardElement.appendChild(cell);
        }
    }
}

function initClickAreas() {
    clickRow.innerHTML = "";
    for (let c = 0; c < COLS; c++) {
        const arrow = document.createElement("div");
        arrow.classList.add("arrow-col");
        arrow.onclick = () => handleMove(c);
        clickRow.appendChild(arrow);
    }
}

resetBtn.addEventListener("click", resetGame);

// -------- API --------
async function resetGame() {
    const difficulty = difficultySelect.value;
    statusDiv.textContent = "Starting...";
    isProcessing = true;

    modal.classList.add("hidden");

    try {
        await fetch(`/reset?difficulty=${difficulty}`, { method: "POST" });
        await fetchState();
        isProcessing = false;
        statusDiv.textContent = "Your Turn";
    } catch {
        isProcessing = false;
    }
}

async function handleMove(col) {
    if (isProcessing) return;
    isProcessing = true;
    statusDiv.textContent = "AI Thinking...";

    try {
        const res = await fetch(`/move/${col}`, { method: "POST" });
        const data = await res.json();

        if (data.error) {
            isProcessing = false;
            statusDiv.textContent = "Your Turn";
            return;
        }

        updateBoard(data.board);

        if (data.game_over) {
            // ⏳ Let winning disc settle first
            setTimeout(() => showModal(data.winner), 700);
            return;
        }

        // ⏳ AI delay before giving control back
        setTimeout(() => {
            isProcessing = false;
            statusDiv.textContent = "Your Turn";
        }, 600);

    } catch {
        isProcessing = false;
    }
}

async function fetchState() {
    const res = await fetch("/state");
    const data = await res.json();
    updateBoard(data.board);
}

// -------- RENDER --------
function updateBoard(serverBoard) {
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            const val = serverBoard[r][c];
            const cell = document.getElementById(`cell-${r}-${c}`);
            const token = cell.querySelector(".token");

            if (val === 0 && token) cell.innerHTML = "";
            else if (val !== 0 && !token) {
                const t = document.createElement("div");
                t.classList.add("token", "drop-anim", val === 1 ? "red" : "yellow");
                cell.appendChild(t);
            }
        }
    }
}

// -------- MODAL --------
function showModal(winner) {
    if (winner === 1) {
        modalEmoji.textContent = "🎉";
        modalTitle.textContent = "You Win!";
        modalMessage.textContent = "Congratulations! Well played 🎊";
    } else if (winner === -1) {
        modalEmoji.textContent = "😢";
        modalTitle.textContent = "You Lost";
        modalMessage.textContent = "The AI outplayed you this time 🤖";
    } else {
        modalEmoji.textContent = "🤝";
        modalTitle.textContent = "Draw";
        modalMessage.textContent = "That was a close one!";
    }

    modal.classList.remove("hidden");
}

function closeModal() {
    modal.classList.add("hidden");
    resetGame();
}
