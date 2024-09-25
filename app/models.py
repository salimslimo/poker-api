# poker/app/models.py

CARD_VALUES = {
    2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
    11: 'J', 12: 'Q', 13: 'K', 14: 'A'
}

CARD_SUITS = ['♠', '♥', '♦', '♣']

class Card:
    def __init__(self, value, suit):
        if value not in CARD_VALUES:
            raise ValueError(f"Invalid card value: {value}")
        if suit not in CARD_SUITS:
            raise ValueError(f"Invalid card suit: {suit}")
        self.value = value
        self.suit = suit
    
    def __str__(self):
        return f'{CARD_VALUES[self.value]}{self.suit}'


class Deck:
    def __init__(self):
        self.cards = [Card(value, suit) for value in CARD_VALUES for suit in CARD_SUITS]
        self.burned_cards = []

    def shuffle(self):
        import random
        random.shuffle(self.cards)

    def burn_card(self):
        burned_card = self.cards.pop(0)
        self.burned_cards.append(burned_card)

    def deal(self, number_of_cards):
        return [self.cards.pop(0) for _ in range(number_of_cards)]

    def remaining_cards(self):
        return len(self.cards)