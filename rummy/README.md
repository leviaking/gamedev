# 🃏 Rummy Card Game

A web-based implementation of the classic Rummy card game built with Python Flask and modern web technologies.

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- Flask web framework

### Installation & Running
```bash
# Install Flask (if not already installed)
pip3 install flask

# Run the game
python3 app.py

# Open your browser and go to:
# http://localhost:5050
```

## 🎮 How to Play

1. **Start the game** - The server will automatically deal cards
2. **Draw a card** - Click "Draw from Stock" or "Draw from Discard"
3. **Select cards** - Click cards to select them (multiple selection supported)
4. **Meld cards** - Select 3+ cards that form a valid set or run, then click "Meld"
5. **Lay off** - Add cards to existing melds by selecting a card and a meld
6. **Discard** - End your turn by discarding one card
7. **Win** - Get rid of all your cards to win!

## 📖 Documentation

For complete game rules and detailed instructions, see:
- **[GAME_MANUAL.md](GAME_MANUAL.md)** - Comprehensive game manual with rules, strategy, and technical details

## 🏗️ Project Structure

```
rummy/
├── app.py                 # Main Flask application
├── rummy_game.py          # Game logic classes
├── templates/
│   └── index.html         # Game interface
├── assets/
│   └── cards/             # Card images (52 cards + 2 jokers)
├── GAME_MANUAL.md         # Complete game documentation
└── README.md              # This file
```

## ✨ Features

- **Real-time gameplay** with automatic updates
- **Valid meld validation** (sets and runs)
- **Multi-card selection** for melding
- **Game statistics** and scoring
- **Error handling** with helpful messages
- **Responsive web interface**
- **New game functionality**

## 🐛 Troubleshooting

- **"python command not found"** → Use `python3` instead
- **Port 5050 busy** → Check if another process is using the port
- **Cards not loading** → Ensure all card images are in `assets/cards/`

## 🎯 Game Rules Summary

- **Objective**: Be the first to get rid of all your cards
- **Valid Melds**: Sets (same rank, different suits) or Runs (consecutive ranks, same suit)
- **Turn Structure**: Draw → Act (optional) → Discard
- **Scoring**: Winner gets 100 points, loser gets penalty points equal to their hand value

## 📝 Development

This is a work-in-progress implementation. See `GAME_MANUAL.md` for planned enhancements and current feature status.

---

**Enjoy playing Rummy!** 🎉 