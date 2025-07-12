import gymnasium.spaces as spaces
import numpy as np
from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector, wrappers

# Helper function to convert card IDs to human-readable format
def card_id_to_str(card_id):
    suits = ["C", "D", "H", "S"]  # Clubs, Diamonds, Hearts, Spades
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    suit = suits[card_id // 13]
    rank = ranks[card_id % 13]
    return f"{rank}{suit}"

def kaiser_game_v0():
    """The Kaiser Game environment"""
    env = _env()
    env = wrappers.TerminateIllegalWrapper(env, illegal_reward=-1)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    return env

class _env(AECEnv):
    metadata = {"render_modes": None, "name": "kaiser_game_v0"}
    
    def can_make_match(self):
        """Checks if the current player can make a match."""
        agent_id = int(self.agent_selection.split("_")[1])
        hand = self.hands[agent_id]
        for hand_card in hand:
            for table_card in self.table:
                if hand_card % 13 == table_card % 13:
                    return True
        return False
    def can_discard(self):
        """Checks if the current player can discard a card."""
        agent_id = int(self.agent_selection.split("_")[1])
        return len(self.hands[agent_id]) > 0 # if the player has any cards, they can discard.

    def __init__(self):
        self.possible_agents = ["player_" + str(r) for r in range(2)]

        self.observation_spaces = {
            agent: spaces.Dict(
                {
                    "observation": spaces.Box(low=0, high=52, shape=(16,), dtype=np.int8),
                    "action_mask": spaces.Box(low=0, high=1, shape=(52 * 4,), dtype=np.int8),
                }
            )
            for agent in self.possible_agents
        }
        self.player_turn = 0  # add player turn

    def reset(self, seed=None, options=None):
        # Initialize game state
        self.agents = self.possible_agents[:]
        self.rewards = {agent: 0 for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.terminations = {agent: False for agent in self.agents}
        self.truncations = {agent: False for agent in self.agents}
        self.infos = {agent: {} for agent in self.agents}
        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.reset()
        self.last_action = None  # Initialize the last action as None
        self.player_turn = 0  # reset player_turn

        # Initialize deck, hands, table, etc.
        self.deck = np.arange(52)
        np.random.shuffle(self.deck)
        self.hands = [sorted(self.deck[:6].tolist()), sorted(self.deck[6:12].tolist())]
        self.table = sorted(self.deck[12:15].tolist())
        self.deck = self.deck[15:].tolist()
        self.scores = [[], []]
        self.discard = []

    def step(self, action):
        # Game logic here
        current_agent = self.agent_selection
        if self.terminations[current_agent] or self.truncations[current_agent]:
            return self._was_dead_step(action)
        agent_id = int(current_agent.split("_")[1])

        # Convert action to cards
        hand_card_index = action // 4
        table_card_index = action % 4
        hand_card = self.hands[agent_id][hand_card_index]

        if table_card_index < 3:
            table_card = self.table[table_card_index]

            if hand_card % 13 == table_card % 13:
                # Player matches and claims the face-up card
                self.scores[agent_id].append(hand_card)
                self.scores[agent_id].append(table_card)
                self.table.pop(table_card_index)
                self.last_action = f"Player {agent_id} claimed card {card_id_to_str(table_card)} using card {card_id_to_str(hand_card)}"
            else:
                # Player discards both the selected hand and face-up cards
                self.discard.append(hand_card)
                self.discard.append(table_card)
                self.table.pop(table_card_index)
                self.last_action = f"Player {agent_id} discarded card {card_id_to_str(hand_card)} and table card {card_id_to_str(table_card)}"
        else:
            # Player discards a card with no matching table card
            self.discard.append(hand_card)
            # Also discard and replace a face-up card
            if len(self.table) > 0:
                discarded_table_card = self.table.pop(0)
                self.discard.append(discarded_table_card)
                self.last_action = (
                    f"Player {agent_id} discarded card {card_id_to_str(hand_card)} "
                    f"and replaced face-up card {card_id_to_str(discarded_table_card)}"
                )
            else:
                self.last_action = f"Player {agent_id} discarded card {card_id_to_str(hand_card)}"

        self.hands[agent_id].pop(hand_card_index)

        # Ensure the player's hand is replenished
        if len(self.deck) > 0:
            self.hands[agent_id].append(self.deck.pop(0))
            self.hands[agent_id].sort()  # Sort the hand after drawing a card

        # Ensure the table never has more than 3 cards
        while len(self.table) < 3 and len(self.deck) > 0:
            self.table.append(self.deck.pop(0))
            self.table.sort()  # Sort the table after adding a card

        # Check for game-ending conditions
        if len(self.deck) == 0 or len(self.table) == 0:
            self.terminations = {agent: True for agent in self.agents}
            score_0 = len(self.scores[0])
            score_1 = len(self.scores[1])

            if score_0 > score_1:
                self.rewards["player_0"] = 1
                self.rewards["player_1"] = -1
            elif score_1 > score_0:
                self.rewards["player_1"] = 1
                self.rewards["player_0"] = -1
            else:
                self.rewards["player_0"] = 0
                self.rewards["player_1"] = 0

        # Select the next agent's turn
        self.agent_selection = self._agent_selector.next()
        self._accumulate_rewards()
        self.player_turn = 1 - self.player_turn  # switches players.

    def observe(self, agent):
        # Observation logic here
        agent_id = int(agent.split("_")[1])
        observation = np.zeros(16, dtype=np.int8)
        observation[:len(self.hands[agent_id])] = self.hands[agent_id]
        observation[6:6 + len(self.table)] = self.table
        observation[9] = len(self.scores[agent_id])
        observation[10] = len(self.scores[1 - agent_id])
        observation[11] = len(self.deck)

        if len(self.hands[agent_id]) > 0:
            action_mask_size = len(self.hands[agent_id]) * 4
            action_mask = np.zeros(action_mask_size, dtype=np.int8)
            for hand_index, hand_card in enumerate(self.hands[agent_id]):
                if len(self.table) > 0:
                    for table_index in range(len(self.table)):
                        table_card = self.table[table_index]
                        if hand_card % 13 == table_card % 13:
                            action_mask[hand_index * 4 + table_index] = 1
                if (hand_index * 4 + 3) < action_mask_size:
                    action_mask[hand_index * 4 + 3] = 1
            return {"observation": observation, "action_mask": action_mask}
        else:
            return {"observation": observation, "action_mask": np.zeros(0, dtype=np.int8)}
