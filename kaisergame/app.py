from flask import Flask, render_template, jsonify, request
from kaisergame import kaiser_game_v0

app = Flask(__name__, static_url_path='/assets', static_folder='assets')

env = kaiser_game_v0()
env.reset()

def card_value_to_code(card_value):
    suits = ["C", "D", "H", "S"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    suit_index = card_value // 13
    rank_index = card_value % 13
    return ranks[rank_index] + suits[suit_index]

def get_game_actions():
    actions = []
    if env.can_make_match():
        actions.append("Make Match")
    elif env.can_discard():
        actions.append("Discard")
    return actions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game_state')
def game_state():
    hands = [[card_value_to_code(card) for card in hand] for hand in env.hands]
    table = [card_value_to_code(card) for card in env.table]
    player_turn = env.player_turn
    actions = get_game_actions()

    return jsonify({'hands': hands, 'table': table, 'player_turn': player_turn, "actions": actions})

@app.route('/make_match', methods=['POST'])
def make_match():
    data = request.get_json()
    print(f"Make Match: hand_index={data.get('hand_index')}, table_index={data.get('table_index')}")
    hand_index = data.get('hand_index')
    table_index = data.get('table_index')
    action = hand_index * 4 + table_index
    env.step(action)
    return jsonify({'success': True})

@app.route('/discard', methods=['POST'])
def discard():
    data = request.get_json()
    print(f"Discard: hand_index={data.get('hand_index')}, table_index={data.get('table_index')}")
    hand_index = data.get('hand_index')
    table_index = data.get('table_index')
    action = hand_index * 4 + table_index
    env.step(action)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)