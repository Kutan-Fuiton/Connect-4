# 🎮 Connect‑4 AI 

A **full‑stack Connect‑4 game** featuring **multiple AI difficulty levels**, including a **Deep Reinforcement Learning (DQN) agent trained to challenge and beat Minimax**.

Built with:
- ⚡ **FastAPI** backend
- 🧠 **PyTorch (DQN)** for Hard AI
- ♟ **Minimax Algorithm** for Medium AI
- 🎨 **HTML, CSS, JavaScript** frontend

---

## 🚀 Live Features

### 🎯 Game Modes
| Difficulty | AI Type | Description |
|---------|--------|-------------|
| Easy | Random AI | Plays random valid moves |
| Medium | Minimax | Strategic search‑based AI |
| Hard | DQN (Neural Network) | Trained using Reinforcement Learning |

### 🧠 Hard AI Highlights
- Deep Q‑Network (DQN)
- Experience Replay
- Target Network
- Epsilon‑Greedy Exploration
- Trained over **100,000+ episodes**

---

## 🗂 Project Structure

```
root/
│
├── main.py                  # FastAPI server
├── requirements.txt         # Dependencies
├── dqn_model.pt             # Trained DQN weights
│
├── ai/
│   ├── dqn_model.py         # Neural network architecture
│   ├── hard_ai.py           # DQN inference logic
│   ├── minimax_ai.py        # Medium difficulty AI
│   ├── random_ai.py         # Easy difficulty AI
│   ├── replay_buffer.py     # Experience replay
│   └── train_dqn.py         # Training script
│
├── game/
│   ├── board.py             # Board representation & moves
│   ├── rules.py             # Win & draw logic
│   └── utils.py             # Valid move helpers
│
├── frontend/
│   ├── index.html           # UI
│   ├── style.css            # Styling
│   └── script.js            # Frontend logic
```

---

## 🧪 How the Hard AI Works (DQN)

1. Board is flattened into a **42‑dim state vector**
2. Neural network outputs **Q‑values for 7 columns**
3. Invalid moves are masked
4. Highest Q‑value valid move is chosen

### Training Strategy
- AI plays against random / curriculum opponents
- Rewards:
  - `+1` → Win
  - `-1` → Loss
  - `+0.2` → Draw
  - `-0.01` → Every move (to encourage faster wins)

---

## 🖥 Running Locally

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Start the server

```bash
uvicorn main:app --reload
```

### 3️⃣ Open browser

```
http://127.0.0.1:8000
```

---

## 🧠 Training the DQN (Optional)

```bash
python ai/train_dqn.py
```

You can safely stop training anytime — the model is saved incrementally.

---

## 📦 Model Details

- Framework: **PyTorch**
- File size: ~**436 KB**
- Architecture: Fully‑connected DQN

---

## 🏆 Why This Project is Special

✅ Combines **classic algorithms + deep learning**

✅ Production‑ready backend & frontend

✅ Deployable on cloud platforms

✅ Educational + competitive gameplay

---

## 🔮 Future Improvements

- Curriculum learning (Minimax opponent during training)
- Self‑play DQN vs DQN
- AlphaZero‑style MCTS
- Mobile UI
- Multiplayer mode

---

## 👤 Author

Built with ❤️ by **Itami**

If you like this project, ⭐ it on GitHub!

