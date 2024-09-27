# poker/app/services.py

import uuid
from app.models import Deck, Card
from typing import List, Dict
from phevaluator.evaluator import evaluate_cards

class PokerGameService:
    def __init__(self, num_players: int = 2) -> None:
        self.id: str = str(uuid.uuid4())  # Génère un ID unique pour chaque partie
        self.deck: Deck = Deck()
        self.deck.shuffle()
        self.num_players: int = num_players
        self.hands: Dict[str, List[Card]] = {}
        self.community_cards: List[Card] = []
        self.player_hands_dealt: bool = False

    def deal_hands(self) -> None:
        for i in range(1, self.num_players + 1):
            player_key = f'player_{i}_hand'
            self.hands[player_key] = self.deck.deal(2)
        self.player_hands_dealt = True

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
            'hands': {player: [str(card) for card in hand] for player, hand in self.hands.items()},
            'community_cards': [str(card) for card in self.community_cards],
            'remaining_cards': self.deck.remaining_cards()
        }
    def evaluate(self) -> Dict[str, object]:

        scores = {}
        winners = []

        for player, hand in self.hands.items():
            player_hand_to_evaluate: List[str] = [str(card.to_phevaluate_format()) for card in self.community_cards] + [str(card.to_phevaluate_format()) for card in hand]
            scores[player] = evaluate_cards(*player_hand_to_evaluate)

        max_score = min(scores.values())

        winners = [player for player, score in scores.items() if score == max_score]

        return {
            'game_id': self.id,
            'hands': {player: [str(card) for card in hand] for player, hand in self.hands.items()},
            'community_cards': [str(card) for card in self.community_cards],
            "scores": scores,
            "winner(s)" : winners
        }