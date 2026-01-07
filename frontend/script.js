// Config
const ROWS = 6;
const COLS = 7;

// DOM Elements
const boardElement = document.getElementById("board");
const clickRow = document.getElementById("click-row");
const statusDiv = document.getElementById("status");
const difficultySelect = document.getElementById("difficulty-select");
const resetBtn = document.getElementById("reset-btn");

let isProcessing = false;

// Init
document.addEventListener("DOMContentLoaded", () => {
    buildGridHTML();  // Create the empty grid structure once
    initClickAreas(); // Create the arrows on top
    resetGame();      // Start game
});

// 1. Build the static grid structure (Empty Holes)
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

// 2. Button Listeners
resetBtn.addEventListener("click", resetGame);

// --- API Logic ---

async function resetGame() {
    const difficulty = difficultySelect.value;
    statusDiv.textContent = "Starting...";
    
    // Lock while resetting to prevent glitches
    isProcessing = true; 
    
    try {
        await fetch(`/reset?difficulty=${difficulty}`, { method: "POST" });
        await fetchState();
        
        // --- FIX IS HERE: Unlock the board explicitly ---
        isProcessing = false;
        statusDiv.textContent = "Your Turn"; 
        
    } catch (e) {
        console.error(e);
        isProcessing = false; // Unlock even if error
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
            // If move was invalid (e.g. column full), ignore and unlock
            if (data.error !== "Game is over") {
                isProcessing = false;
                statusDiv.textContent = "Your Turn";
            }
        } else {
            updateBoard(data.board); // Update visuals
            
            if (data.game_over) {
                // Keep locked if game over
                if (data.winner === 1) statusDiv.textContent = "🎉 You Win!";
                else if (data.winner === -1) statusDiv.textContent = "🤖 AI Wins!";
                else statusDiv.textContent = "🤝 Draw!";
            } else {
                // Unlock if game continues
                isProcessing = false;
                statusDiv.textContent = "Your Turn";
            }
        }
    } catch (e) {
        console.error(e);
        isProcessing = false;
    }
}

async function fetchState() {
    try {
        const res = await fetch("/state");
        const data = await res.json();
        updateBoard(data.board);
        // We don't unlock here because resetGame handles it
    } catch (e) {
        console.error(e);
    }
}

// --- Rendering ---

function updateBoard(serverBoard) {
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            const val = serverBoard[r][c];
            const cellDiv = document.getElementById(`cell-${r}-${c}`);
            const hasToken = cellDiv.querySelector(".token");

            // 1. Clear if server says empty but we have token (Reset scenario)
            if (val === 0 && hasToken) {
                cellDiv.innerHTML = ""; 
            } 
            // 2. Add if server says occupied but we have NO token (Move scenario)
            else if (val !== 0 && !hasToken) {
                const token = document.createElement("div");
                token.classList.add("token");
                token.classList.add("drop-anim"); 
                
                if (val === 1) token.classList.add("red");
                else token.classList.add("yellow");
                
                cellDiv.appendChild(token);
            }
        }
    }
}