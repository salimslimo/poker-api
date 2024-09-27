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
        if num_players < 2:
            raise ValueError("A poker game must have at least 2 players.")
        self.num_players: int = num_players
        self.hands: Dict[str, List[Card]] = {}
        self.community_cards: List[Card] = []
        self.player_hands_dealt: bool = False

    def deal_hands(self) -> None:
        if self.player_hands_dealt:
            raise RuntimeError("The hands have already been dealt.")
        for i in range(1, self.num_players + 1):
            self.hands[f'player_{i}'] = self.deck.deal(2)
        self.player_hands_dealt = True

    def burn_and_deal_flop(self) -> None:
        if not self.player_hands_dealt:
            raise RuntimeError("Hands have not been dealt yet. Deal hands first.")
        if len(self.community_cards) >= 3:
            raise RuntimeError("The flop has already been distributed.")
        self.deck.burn_card()
        self.community_cards.extend(self.deck.deal(3))

    def burn_and_deal_turn(self) -> None:
        if len(self.community_cards) < 3:
            raise RuntimeError("The flop has not been dealt yet. Proceed to the flop first.")
        if len(self.community_cards) >= 4:
            raise RuntimeError("The turn has already been dealt.")
        self.deck.burn_card()
        self.community_cards.extend(self.deck.deal(1))

    def burn_and_deal_river(self) -> None:
        if len(self.community_cards) < 3:
            raise RuntimeError("The flop has not been dealt yet. Proceed to the flop first.")
        if len(self.community_cards) < 4:
            raise RuntimeError("The turn has not yet been dealt. Pass to the turn first.")
        if len(self.community_cards) >= 5:
            raise RuntimeError("The river has already been dealt.")
        self.deck.burn_card()
        self.community_cards.extend(self.deck.deal(1))

    def get_game_state(self) -> Dict[str, object]:
        return {
            'game_id': self.id,
            'hands': {player: [str(card) for card in hand] for player, hand in self.hands.items()},
            'community_cards': [str(card) for card in self.community_cards],
            'remaining_cards': self.deck.remaining_cards(),
            'player_hands_dealt': self.player_hands_dealt
        }
    def evaluate(self) -> Dict[str, object]:

        scores = {}

        for player, hand in self.hands.items():
            hand_to_evaluate: List[str] = [str(card.to_phevaluate_format()) for card in self.community_cards + hand]

            score_value = evaluate_cards(*hand_to_evaluate)
            if score_value > 6185:
                hand_value = "High card"
            elif score_value > 3325:
                hand_value = "One pair"
            elif score_value > 2467:
                hand_value = "Two pair"
            elif score_value > 1609:
                hand_value = "Three of a kind"
            elif score_value > 1599:
                hand_value = "Straight"
            elif score_value > 322:
                hand_value = "Flush"
            elif score_value > 166:
                hand_value = "Full house"
            elif score_value > 10:
                hand_value = "Four of a kind"
            else:
                hand_value = "Straight flush"
            scores[player] = {
                'score': score_value,
                'hand_value': hand_value
            }

        max_score = min([score['score'] for score in scores.values()])
        winners = [player for player, score in scores.items() if score['score'] == max_score]
        return {
            'game_id': self.id,
            'hands': {player: [str(card) for card in hand] for player, hand in self.hands.items()},
            'community_cards': [str(card) for card in self.community_cards],
            "scores": scores,
            "winner(s)" : winners
        }