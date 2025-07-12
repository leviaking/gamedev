from flask import Flask, jsonify, request, render_template, send_from_directory
import random
import os

app = Flask(__name__)

# --- Card Dealing and Game Setup ---

suits = ['H', 'D', 'C', 'S']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
deck = [f'{rank}{suit}' for suit in suits for rank in ranks]

# Card rank values for scoring
rank_values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 1
}

def deal_cards(num_players, cards_per_player=7):
    shuffled_deck = deck[:]
    random.shuffle(shuffled_deck)
    hands = [shuffled_deck[i:i + cards_per_player] for i in range(0, num_players * cards_per_player, cards_per_player)]
    global stock_pile
    stock_pile = shuffled_deck[num_players * cards_per_player:]
    return hands

def is_valid_set(cards):
    """Check if cards form a valid set (same rank, different suits)"""
    if len(cards) < 3:
        return False
    
    # Extract ranks
    ranks = [card[:-1] for card in cards]
    suits = [card[-1] for card in cards]
    
    # All cards must have the same rank
    if len(set(ranks)) != 1:
        return False
    
    # All cards must have different suits
    if len(set(suits)) != len(cards):
        return False
    
    return True

def is_valid_run(cards):
    """Check if cards form a valid run (consecutive ranks, same suit)"""
    if len(cards) < 3:
        return False
    
    # Extract ranks and suits
    ranks = [card[:-1] for card in cards]
    suits = [card[-1] for card in cards]
    
    # All cards must have the same suit
    if len(set(suits)) != 1:
        return False
    
    # Sort ranks by their numerical value
    sorted_ranks = sorted(ranks, key=lambda x: rank_values[x])
    
    # Check if ranks are consecutive
    for i in range(len(sorted_ranks) - 1):
        current_rank = sorted_ranks[i]
        next_rank = sorted_ranks[i + 1]
        
        # Find the next expected rank
        current_value = rank_values[current_rank]
        expected_next_value = current_value + 1
        
        # Handle Ace as both 1 and 14
        if current_rank == 'K' and next_rank == 'A':
            continue
        elif current_rank == 'A' and next_rank == '2':
            continue
        elif rank_values[next_rank] != expected_next_value:
            return False
    
    return True

def is_valid_meld(cards):
    """Check if cards form a valid meld (either set or run)"""
    return is_valid_set(cards) or is_valid_run(cards)

def calculate_hand_score(hand):
    """Calculate the score of a hand (sum of card values)"""
    return sum(rank_values[card[:-1]] for card in hand)

def check_win_condition(hand):
    """Check if a player has won (no cards left in hand)"""
    return len(hand) == 0

game_state = None
player_ids = {}  # Store player IDs and their corresponding player numbers
stock_pile = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game/<int:num_players>', methods=['POST'])
def start_game(num_players):
    global game_state, player_ids
    game_state = {
        'hands': deal_cards(num_players),
        'stock_pile': stock_pile,
        'discard_pile': [],
        'melds': [],
        'current_player': 0,
        'player_actions': {0: None, 1: None},
        'playerNumber': None,
        'game_over': False,
        'winner': None,
        'scores': [0, 0]
    }
    player_ids = {}  # Reset player IDs when a new game starts
    print(f'Server start_game, player_actions: {game_state["player_actions"]}')
    return jsonify({'message': 'Game started'})

def next_turn():
    global game_state
    game_state['current_player'] = (game_state['current_player'] + 1) % 2
    #print(f'Server next_turn, player_actions: {game_state["player_actions"]}')  # Removed this line


@app.route('/game_state', methods=['GET'])
def get_game_state():
    global game_state, player_ids
    if game_state:
        player_id = request.headers.get('Player-Id')
        if player_id:
            if player_id not in player_ids:
                if len(player_ids) < 2:
                    player_ids[player_id] = len(player_ids)  # Assign the next available player number
                else:
                    return jsonify({"error": "Game full"})

            game_state["playerNumber"] = player_ids[player_id]
            print("Server get_game_state, player_actions: ", game_state["player_actions"])
            return jsonify(game_state)
        else:
            return jsonify({"error": "No Player-Id"})
    else:
        return jsonify({'message': 'Game not started'})

@app.route('/draw_stock', methods=['POST'])
def draw_stock():
    global game_state, stock_pile
    player = request.json.get('player')
    if game_state['current_player'] == player:
        if stock_pile:
            card = stock_pile.pop(0)
            game_state['hands'][player].append(card)
            game_state['player_actions'][player] = 'draw'
            print(f'Server draw_stock, player_actions: {game_state["player_actions"]}')
            return jsonify({'message': 'Card drawn from stock'})
        else:
            return jsonify({'error': 'Stock pile is empty'})
    else:
        return jsonify({'error': 'Not your turn'})

@app.route('/draw_discard', methods=['POST'])
def draw_discard():
    global game_state
    player = request.json.get('player')
    if game_state['current_player'] == player:
        if game_state['discard_pile']:
            card = game_state['discard_pile'].pop()
            game_state['hands'][player].append(card)
            game_state['player_actions'][player] = 'draw'
            print(f'Server draw_discard, player_actions: {game_state["player_actions"]}')
            return jsonify({'message': 'Card drawn from discard'})
        else:
            return jsonify({'error': 'Discard pile is empty'})
    else:
        return jsonify({'error': 'Not your turn'})

@app.route('/discard', methods=['POST'])
def discard():
    global game_state
    player = request.json.get('player')
    card = request.json.get('card')
    if game_state['current_player'] == player:
        if game_state['player_actions'][player] == 'draw':
            # Check if card is in player's hand
            if card not in game_state['hands'][player]:
                return jsonify({'error': f'Card {card} not in your hand'})
            
            game_state['hands'][player].remove(card)
            game_state['discard_pile'].append(card)
            game_state['player_actions'][player] = None
            print(f'Server discard, player_actions: {game_state["player_actions"]}')
            
            # Check for win condition after discard
            if check_win_condition(game_state['hands'][player]):
                game_state['game_over'] = True
                game_state['winner'] = player
                game_state['scores'][player] += 100  # Bonus for winning
                return jsonify({'message': 'Card discarded - Game Over! You won!'})
            
            next_turn()
            return jsonify({'message': 'Card discarded'})
        else:
            return jsonify({'error': 'You must draw a card before discarding'})
    else:
        return jsonify({'error': 'Not your turn'})

@app.route('/meld', methods=['POST'])
def meld():
    global game_state
    player = request.json.get('player')
    cards = request.json.get('cards')

    if game_state['current_player'] == player:
        if len(cards) < 3:
            return jsonify({'error': 'Must meld at least 3 cards'})

        # Check if all cards are in player's hand
        player_hand = game_state['hands'][player]
        for card in cards:
            if card not in player_hand:
                return jsonify({'error': f'Card {card} not in your hand'})

        if is_valid_meld(cards):
            for card in cards:
                game_state['hands'][player].remove(card)
            game_state['melds'].append(cards)
            
            # Check for win condition
            if check_win_condition(game_state['hands'][player]):
                game_state['game_over'] = True
                game_state['winner'] = player
                game_state['scores'][player] += 100  # Bonus for winning
            
            return jsonify({'message': 'Cards melded successfully'})
        else:
            # Provide more specific error message
            if is_valid_set(cards):
                return jsonify({'error': 'Invalid run - cards must be consecutive ranks of the same suit'})
            elif is_valid_run(cards):
                return jsonify({'error': 'Invalid set - cards must be the same rank with different suits'})
            else:
                return jsonify({'error': 'Invalid meld - must be either a set (same rank, different suits) or run (consecutive ranks, same suit)'})
    else:
        return jsonify({'error': 'Not your turn'})

@app.route('/lay_off', methods=['POST'])
def lay_off():
    global game_state
    player = request.json.get('player')
    card = request.json.get('card')
    meld_index = request.json.get('meld_index')

    if game_state['current_player'] == player:
        if 0 <= meld_index < len(game_state['melds']):
            # Check if card is in player's hand
            if card not in game_state['hands'][player]:
                return jsonify({'error': f'Card {card} not in your hand'})
            
            # Create temporary meld to validate
            temp_meld = game_state['melds'][meld_index] + [card]
            
            if is_valid_meld(temp_meld):
                game_state['hands'][player].remove(card)
                game_state['melds'][meld_index].append(card)
                
                # Check for win condition
                if check_win_condition(game_state['hands'][player]):
                    game_state['game_over'] = True
                    game_state['winner'] = player
                    game_state['scores'][player] += 100  # Bonus for winning
                
                return jsonify({'message': 'Card laid off successfully'})
            else:
                return jsonify({'error': 'Cannot lay off this card - it would make the meld invalid'})
        else:
            return jsonify({'error': 'Invalid meld index'})
    else:
        return jsonify({'error': 'Not your turn'})

@app.route('/game_stats', methods=['GET'])
def get_game_stats():
    global game_state
    if game_state:
        stats = {
            'game_over': game_state.get('game_over', False),
            'winner': game_state.get('winner'),
            'scores': game_state.get('scores', [0, 0]),
            'hand_scores': [calculate_hand_score(hand) for hand in game_state['hands']],
            'total_melds': len(game_state['melds']),
            'cards_in_stock': len(game_state['stock_pile']),
            'cards_in_discard': len(game_state['discard_pile'])
        }
        return jsonify(stats)
    else:
        return jsonify({'error': 'Game not started'})

@app.route('/assets/cards/<path:filename>')
def serve_static(filename):
    cards_dir = os.path.join(os.getcwd(), 'assets', 'cards')
    return send_from_directory(cards_dir, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
