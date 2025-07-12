from flask import Flask, jsonify, request, render_template, send_from_directory
import random
import os

app = Flask(__name__)

# --- Card Dealing and Game Setup ---

suits = ['H', 'D', 'C', 'S']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
deck = [f'{rank}{suit}' for suit in suits for rank in ranks]

def deal_cards(num_players, cards_per_player=7):
    shuffled_deck = deck[:]
    random.shuffle(shuffled_deck)
    hands = [shuffled_deck[i:i + cards_per_player] for i in range(0, num_players * cards_per_player, cards_per_player)]
    global stock_pile
    stock_pile = shuffled_deck[num_players * cards_per_player:]
    return hands

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
        'playerNumber': None
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
            game_state['hands'][player].remove(card)
            game_state['discard_pile'].append(card)
            game_state['player_actions'][player] = None
            print(f'Server discard, player_actions: {game_state["player_actions"]}')
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

        if len(set([card.split('_of_')[0] for card in cards])) == 1:
            for card in cards:
                game_state['hands'][player].remove(card)
            game_state['melds'].append(cards)
            return jsonify({'message': 'Cards melded'})
        else:
            return jsonify({'error': 'Invalid meld'})
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
            game_state['hands'][player].remove(card)
            game_state['melds'][meld_index].append(card)
            return jsonify({'message': 'Card laid off'})
        else:
            return jsonify({'error': 'Invalid meld index'})
    else:
        return jsonify({'error': 'Not your turn'})

@app.route('/assets/cards/<path:filename>')
def serve_static(filename):
    cards_dir = os.path.join(os.getcwd(), 'assets', 'cards')
    return send_from_directory(cards_dir, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
