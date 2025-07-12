import random
import json

class RummyGame:
    def __init__(self, num_players):
        self.num_players = num_players
        self.deck = self.create_deck()
        self.hands = [[] for _ in range(num_players)]
        self.stock_pile = []
        self.discard_pile = []
        self.melds = []  # List of lists, where each inner list is a meld
        self.current_player = 0
        self.scores = [0] * num_players
        self.game_over = False

        self.deal_cards()
        self.setup_piles()

    def create_deck(self):
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        suits = ["C", "D", "H", "S"]
        deck = [rank + suit for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def deal_cards(self):
        cards_per_player = 10 if self.num_players == 2 else 7
        for player in range(self.num_players):
            self.hands[player] = self.deck[:cards_per_player]
            self.deck = self.deck[cards_per_player:]

    def setup_piles(self):
        self.stock_pile = self.deck[:-1]
        self.discard_pile.append(self.deck[-1])

    def next_player(self):
        self.current_player = (self.current_player + 1) % self.num_players

    def get_game_state(self):
        return {
            "num_players": self.num_players,
            "hands": self.hands,
            "stock_pile": self.stock_pile,
            "discard_pile": self.discard_pile,
            "melds": self.melds,
            "current_player": self.current_player,
            "scores": self.scores,
            "game_over": self.game_over,
        }

if __name__ == "__main__":
    game = RummyGame(2)
    game_state = game.get_game_state()
    json_state = json.dumps(game_state)
    print(json_state)
