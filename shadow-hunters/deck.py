import random
import copy

from card import Card
# deck.py
# Implements the Deck object.


class Deck:
    def __init__(self, cards):
        # Make sure a list is passed to cards
        if not isinstance(cards, list):
            raise ValueError("cards must be a list.")

        self.cards = cards  # note that cards are ordered [bottom, ... top]

        # Make sure every card in self.cards is a Card object
        for c in self.cards:
            if not isinstance(c, Card):
                raise ValueError("One or more cards is not a Card object.")

        self.discard = []
        self.shuffle()
        # for i in range(5):
        #    self.addToDiscard(self.drawCard())

    def shuffle(self):
        random.shuffle(self.cards)

    def drawCard(self):
        if len(self.cards) > 0:
            drawn = self.cards.pop()

            # Discard the card IFF it is not an equipment card
            if not drawn.is_equipment:
                self.discard.append(copy.deepcopy(drawn))

            return drawn
        else:
            self.cards, self.discard = self.discard, []
            self.shuffle()
            return self.drawCard()

    def listEquipmentInDiscard(self):
        equipment = []
        for c in self.discard:
            if c.is_equipment:
                equipment.append(c.title)
        return equipment

    def addToDiscard(self, card):
        self.discard.append(card)

    def takeFromDiscard(self, title):
        card = None
        for c in self.discard:
            if c.title == title:
                card = c
                break
        if card is not None:
            self.discard.remove(card)
        return card
