# poker/app/models.py
import random
from typing import List, Dict

CARD_VALUES: Dict[int, str] = {
    2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
    11: 'J', 12: 'Q', 13: 'K', 14: 'A'
}

CARD_SUITS: set = {'♠', '♥', '♦', '♣'}

SUIT_MAPPING: Dict[str, str] = {
    '♠': 's',
    '♥': 'h',
    '♦': 'd',
    '♣': 'c'
}

VALUE_MAPPING: Dict[str, str] = {
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
    '10': 'T',
    'J': 'J',
    'Q': 'Q',
    'K': 'K',
    'A': 'A'
}

class Card:
    def __init__(self, value: int, suit: str) -> None:
        if value not in CARD_VALUES:
            raise ValueError(f"Invalid card value: {value} during card creation.")
        if suit not in CARD_SUITS:
            raise ValueError(f"Invalid card suit: {suit} during card creation.")
        self.value: int = value
        self.suit: str = suit
    
    def __str__(self) -> str:
        return f'{CARD_VALUES[self.value]}{self.suit}'

    def to_phevaluate_format(self) -> str:
        return f'{VALUE_MAPPING[CARD_VALUES[self.value]]}{SUIT_MAPPING[self.suit]}'


class Deck:
    def __init__(self) -> None:
        self.cards: List[Card] = self._generate_deck()
        self.burned_cards: List[Card] = []

    def _generate_deck(self) -> List[Card]:
        return [Card(value, suit) for value in CARD_VALUES for suit in CARD_SUITS]

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def burn_card(self) -> None:
        burned_card = self.cards.pop(0)
        self.burned_cards.append(burned_card)

    def deal(self, number_of_cards: int) -> List[Card]:
        if number_of_cards > len(self.cards):
            raise ValueError("Il ne reste pas assez de cartes dans le paquet.")
        return [self.cards.pop(0) for _ in range(number_of_cards)]

    def remaining_cards(self) -> int:
        return len(self.cards)