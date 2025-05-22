# Minimax vs Alpha-Beta Pruning in Tic-Tac-Toe AI

## How They Work Differently (Conceptually)

### Minimax (Exhaustive Search)

- Explores **all possible game states** to calculate the optimal move.
- In a complete game tree, it evaluates **every leaf node**.
- The time complexity is **O(b^d)** where:
  - `b` is the branching factor (number of possible moves),
  - `d` is the depth of the tree (remaining moves in the game).

### Alpha-Beta Pruning (Selective Search)

- An optimization over Minimax that **skips unnecessary branches**.
- It **prunes** game paths that cannot influence the final decision, based on alpha (best already explored option for maximizer) and beta (best for minimizer).
- In the best-case scenario with **perfect move ordering**, it reduces time complexity to **O(b^(d/2))**.
- Produces the **same output** as Minimax, just more efficiently.

---

## 🎮 My Tic-Tac-Toe Implementation

I implemented both **Minimax** and **Alpha-Beta Pruning** in my Tic-Tac-Toe game. While there was **no drastic performance change** after introducing pruning, here’s why:

- **Tic-Tac-Toe has a small search space** — at most 9! (362,880) possible board states, and even fewer due to early game conclusions and symmetry.
- **Minimax can evaluate the entire game tree in milliseconds**, making pruning seem unnecessary.
- However, **Alpha-Beta Pruning still reduces redundant evaluations**, making the logic cleaner and more efficient under the hood.

This kind of optimization becomes significantly more impactful in **larger games** (e.g., Chess or Go), where pruning can skip evaluating millions of nodes and make real-time AI computation feasible.

---

## ✅ Why It Still Matters

Even if Alpha-Beta Pruning doesn’t feel impactful in a small game like Tic-Tac-Toe:

- It's a **foundational AI optimization** technique.
- It prepares the codebase for **more complex games or deeper trees**.
- It encourages **better algorithmic practices** in game AI development.

# Tic-Tac-Toe with AI Game Features 

A Python implementation of Tic-Tac-Toe featuring:
- Player vs Player mode
- Unbeatable AI using Minimax with Alpha-Beta pruning
- Smooth animations and clean UI

## Features
- ✨ Play against a friend or AI
- 🤖 Smart bot using advanced algorithms
- 🎮 Interactive game board with animations
- 🏆 Win detection with visual effects

## Requirements
- python installation
- pygame installation 

