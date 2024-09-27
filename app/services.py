# poker/app/services.py

import uuid
from app.models import Deck, Card
from typing import List, Dict
from phevaluator.evaluator import evaluate_cards

class PokerGameService:
    def __init__(self) -> None:
        self.id: str = str(uuid.uuid4())  # Génère un ID unique pour chaque partie
        self.deck: Deck = Deck()
        self.deck.shuffle()
        self.player_1_hand: List[Card] = []
        self.player_2_hand: List[Card] = []
        self.community_cards: List[Card] = []

    def deal_hands(self) -> None:
        self.player_1_hand = self.deck.deal(2)
        self.player_2_hand = self.deck.deal(2)

    def burn_and_deal_flop(self) -> None:
        self.deck.burn_card()
        self.community_cards.extend(self.deck.deal(3))

    def burn_and_deal_turn(self) -> None:
        self.deck.burn_card()
        self.community_cards.extend(self.deck.deal(1))

    def burn_and_deal_river(self) -> None:
        self.deck.burn_card()
        self.community_cards.extend(self.deck.deal(1))

    def get_game_state(self) -> Dict[str, object]:
        return {
            'game_id': self.id,
            'player_1_hand': [str(card) for card in self.player_1_hand],
            'player_2_hand': [str(card) for card in self.player_2_hand],
            'community_cards': [str(card) for card in self.community_cards],
            'remaining_cards': self.deck.remaining_cards()
        }
    def evaluate(self) -> Dict[str, object]:

        player_1_hand_to_evaluate: List[str] = [str(card.to_phevaluate_format()) for card in self.community_cards] + [str(card.to_phevaluate_format()) for card in self.player_1_hand]
        player_2_hand_to_evaluate: List[str] = [str(card.to_phevaluate_format()) for card in self.community_cards] + [str(card.to_phevaluate_format()) for card in self.player_2_hand]

        score_player_1: int = evaluate_cards(*player_1_hand_to_evaluate)
        score_player_2: int = evaluate_cards(*player_2_hand_to_evaluate)

        if score_player_1 < score_player_2:
            winner: str = 'Player 1'
        elif score_player_1 > score_player_2:
            winner: str = 'Player 2'
        else:
            winner: str = "Egalité"

        return {
            'game_id': self.id,
            'player_1_hand': [str(card) for card in self.player_1_hand],
            'player_2_hand': [str(card) for card in self.player_2_hand],
            'community_cards': [str(card) for card in self.community_cards],
            "score_player_1": score_player_1,
            "score_player_2": score_player_2,
            "winner" : winner
        }