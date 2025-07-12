# 🃏 **Rummy - Classic Card Game**

## **Game Overview**
Rummy is a classic card game of skill and strategy where players compete to be the first to get rid of all their cards by forming valid combinations called "melds." The game combines elements of luck, strategy, and quick thinking as players draw, discard, and organize their cards to create winning hands.

## **What's Included**
- **52 Standard Playing Cards** (2-10, J, Q, K, A in all four suits)
- **2 Players** (expandable to more)
- **Digital Game Board** with real-time scoring and statistics

## **Objective**
Be the first player to get rid of all your cards by forming valid melds and discarding your remaining cards. The player with no cards left wins the game!

## **Setup**
1. **Deal 7 cards** to each player
2. **Place remaining cards** face-down as the "Stock Pile"
3. **Start with Player 0** - the game begins!

## **How to Play**

### **Your Turn Structure:**
1. **DRAW** - Take one card from either:
   - **Stock Pile** (face-down deck)
   - **Discard Pile** (top card only)

2. **ACT** (Optional) - You may:
   - **Meld** cards (form valid combinations)
   - **Lay Off** cards (add to existing melds)

3. **DISCARD** - End your turn by discarding one card to the discard pile

### **Valid Melds**

#### **Sets** (Same Rank, Different Suits)
- **Example**: 7♥, 7♦, 7♣
- **Minimum**: 3 cards
- **Maximum**: 4 cards (one of each suit)

#### **Runs** (Consecutive Ranks, Same Suit)
- **Example**: 5♥, 6♥, 7♥, 8♥
- **Minimum**: 3 cards
- **Maximum**: 13 cards (A-2-3...-K)
- **Aces count as 1** (lowest value)

### **Card Values**
- **Number Cards (2-10)**: Face value (2=2 points, 10=10 points)
- **Face Cards (J, Q, K)**: 10 points each
- **Aces**: 1 point each

## **Game Actions**

### **Drawing Cards**
- **From Stock**: Click "Draw from Stock" to take the top card
- **From Discard**: Click "Draw from Discard" to take the top card from discard pile
- **Note**: You must draw before taking any other actions

### **Melding Cards**
1. **Select 3 or more cards** that form a valid set or run
2. **Click "Meld"** to play them on the table
3. **Cards are removed** from your hand and placed in the meld area

### **Laying Off Cards**
1. **Select one card** from your hand
2. **Click on an existing meld** to select it
3. **Click "Lay Off"** to add your card to that meld
4. **Card must maintain** the meld's validity

### **Discarding**
- **Select one card** from your hand
- **Click "Discard"** to end your turn
- **Card goes to** the discard pile

## **Scoring System**

### **During the Game**
- **Hand Score**: Total value of cards in your hand
- **Strategy**: Lower hand score = better position
- **Display**: Shows "Your Hand Score: X" during play

### **Game End Scoring**
- **Winner**: Gets 100 bonus points
- **Loser**: Gets penalty points equal to their hand score
- **Example**: Loser with 7♥, 8♦, K♣ = 7+8+10 = 25 penalty points

## **Winning the Game**
- **Primary Win**: Get rid of all your cards (hand score = 0)
- **Winning Move**: Can be achieved by:
  - Melding all remaining cards
  - Laying off all remaining cards
  - Discarding your last card

## **Strategy Tips**

### **Early Game**
- **Draw from stock** to build your hand
- **Look for potential melds** in your starting hand
- **Keep low-value cards** for easier discarding

### **Mid Game**
- **Form melds early** to reduce your hand score
- **Watch the discard pile** for useful cards
- **Plan your discards** carefully

### **End Game**
- **Focus on getting rid** of high-value cards
- **Use lay-offs** to reduce your hand quickly
- **Time your final discard** perfectly

## **Game Interface**

### **Display Elements**
- **Player Hands**: Shows all cards for both players
- **Stock Pile**: Number of remaining cards
- **Discard Pile**: Top card visible
- **Melds Area**: All played combinations
- **Game Statistics**: Scores, hand values, and game state

### **Controls**
- **Card Selection**: Click cards to select/deselect
- **Action Buttons**: Draw, Meld, Lay Off, Discard, New Game
- **Visual Feedback**: Selected cards highlighted in red
- **Turn Indicators**: Clear display of whose turn it is

## **Game Rules Summary**

### **Must Follow**
- ✅ Draw exactly one card per turn
- ✅ Discard exactly one card per turn
- ✅ Form valid melds (sets or runs of 3+ cards)
- ✅ Maintain meld validity when laying off

### **Cannot Do**
- ❌ Draw without discarding
- ❌ Discard without drawing first
- ❌ Form invalid melds
- ❌ Lay off cards that break meld rules
- ❌ Play out of turn

## **Technical Features**
- **Real-time Updates**: Game state refreshes automatically
- **Error Handling**: Clear messages for invalid actions
- **Multi-card Selection**: Select multiple cards for melding
- **Game Statistics**: Live scoring and hand analysis
- **New Game**: Restart anytime with fresh cards

## **How to Run the Game**

### **Prerequisites**
- Python 3.6 or higher
- Flask web framework

### **Installation**
```bash
# Install Flask if not already installed
pip3 install flask

# Navigate to the game directory
cd /path/to/rummy

# Run the game
python3 app.py
```

### **Access the Game**
1. Open your web browser
2. Go to: `http://localhost:5050`
3. The game will load automatically

### **Troubleshooting**
- If `python` command not found, use `python3`
- If port 5050 is busy, the server will show an error
- Make sure all card images are in the `assets/cards/` directory

## **File Structure**
```
rummy/
├── app.py                 # Main Flask application
├── rummy_game.py          # Game logic classes
├── templates/
│   └── index.html         # Game interface
├── assets/
│   └── cards/             # Card images (52 cards + 2 jokers)
└── GAME_MANUAL.md         # This file
```

## **Development Notes**

### **Current Features**
- ✅ 2-player gameplay
- ✅ Real-time game state updates
- ✅ Valid meld validation (sets and runs)
- ✅ Multi-card selection
- ✅ Game statistics and scoring
- ✅ Error handling and validation
- ✅ Responsive web interface

### **Potential Enhancements**
- 🔄 3-4 player support
- 🔄 AI opponents
- 🔄 Tournament mode
- 🔄 Card sorting functionality
- 🔄 Sound effects and animations
- 🔄 Game history and replays
- 🔄 Custom card themes
- 🔄 Mobile app version


---

*This manual is part of the Rummy game project. For technical support or feature requests, please refer to the project documentation.* 