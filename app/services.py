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
        self.hands: List[List[Card]] = [[] for _ in range(num_players)]
        self.community_cards: List[Card] = []

    def deal_hands(self) -> None:
        for i in range(self.num_players):
            self.hands[i] = self.deck.deal(2)

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
            'hands': [[str(card) for card in hand] for hand in self.hands],
            'community_cards': [str(card) for card in self.community_cards],
            'remaining_cards': self.deck.remaining_cards()
        }
    def evaluate(self) -> Dict[str, object]:

        scores = []
        winners = []

        for i in range(self.num_players):
            player_hand_to_evaluate: List[str] = [str(card.to_phevaluate_format()) for card in self.community_cards] + [str(card.to_phevaluate_format()) for card in self.hands[i]]
            score = evaluate_cards(*player_hand_to_evaluate)
            scores.append(score)

        max_score = min(scores)

        winners = [f'Player {i + 1}' for i, score in enumerate(scores) if score == max_score]

        return {
            'game_id': self.id,
            'hands': [[str(card) for card in hand] for hand in self.hands],
            'community_cards': [str(card) for card in self.community_cards],
            "scores": scores,
            "winners" : winners
        }