# poker/app/services.py

import uuid
from app.models import Deck
from phevaluator.evaluator import evaluate_cards

class PokerGameService:
    def __init__(self):
        self.id = str(uuid.uuid4())  # Génère un ID unique pour chaque partie
        self.deck = Deck()
        self.deck.shuffle()
        self.player_1_hand = []
        self.player_2_hand = []
        self.community_cards = []

    def deal_hands(self):
        self.player_1_hand = self.deck.deal(2)
        self.player_2_hand = self.deck.deal(2)

    def burn_and_deal_flop(self):
        self.deck.burn_card()
        self.community_cards.extend(self.deck.deal(3))

    def burn_and_deal_turn(self):
        self.deck.burn_card()
        self.community_cards.extend(self.deck.deal(1))

    def burn_and_deal_river(self):
        self.deck.burn_card()
        self.community_cards.extend(self.deck.deal(1))

    def get_game_state(self):
        return {
            'game_id': self.id,
            'player_1_hand': [str(card) for card in self.player_1_hand],
            'player_2_hand': [str(card) for card in self.player_2_hand],
            'community_cards': [str(card) for card in self.community_cards],
            'remaining_cards': self.deck.remaining_cards()
        }
    def evaluate(self):

        player_1_hand_to_evaluate = [str(card.to_phevaluate_format()) for card in self.community_cards] + [str(card.to_phevaluate_format()) for card in self.player_1_hand]
        player_2_hand_to_evaluate = [str(card.to_phevaluate_format()) for card in self.community_cards] + [str(card.to_phevaluate_format()) for card in self.player_2_hand]

        score_player_1 = evaluate_cards(*player_1_hand_to_evaluate)
        score_player_2 = evaluate_cards(*player_2_hand_to_evaluate)

        if score_player_1 < score_player_2:
            winner = 'Player 1'
        elif score_player_1 > score_player_2:
            winner = 'Player 2'
        else:
            winner = "Egalité"

        return {
            'game_id': self.id,
            'player_1_hand': [str(card) for card in self.player_1_hand],
            'player_2_hand': [str(card) for card in self.player_2_hand],
            'community_cards': [str(card) for card in self.community_cards],
            "score_player_1": score_player_1,
            "score_player_2": score_player_2,
            "winner" : winner
        }