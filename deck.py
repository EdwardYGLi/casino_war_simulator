"""
Created by edwardli on 7/5/21
"""
import random

import numpy as np

_suits = {
    0: "Clubs",
    1: "Diamonds",
    2: "Hearts",
    3: "Spades"
}

_cards = {
    0: "2",
    1: "3",
    2: "4",
    3: "5",
    4: "6",
    5: "7",
    6: "8",
    7: "9",
    8: "10",
    9: "J",
    10: "Q",
    11: "K",
    12: "A",

}


class WarDeck:
    def __init__(self, n_decks=1):
        self.n_decks = n_decks
        self.deck_size = 52
        self.cards = list(range(self.deck_size * self.n_decks))
        self.draw_ind = 0

    def seed(self, seed):
        np.random.seed(seed)
        random.seed(seed)

    def shuffle(self, times=7):
        for _ in range(times):
            random.shuffle(self.cards)

    def reinit(self):
        self.draw_ind = 0
        self.shuffle()

    def draw(self):
        if self.draw_ind >= len(self.cards):
            return None, None

        # return value mod 52 % suit(13)
        card = self.cards[self.draw_ind] % 52 % 13
        suit = self.cards[self.draw_ind] % 52 // 13
        self.draw_ind += 1

        return card, suit

    def to_string(self, s, c):
        return _suits[s] + " " + _cards[c]


if __name__ == "__main__":
    deck = WarDeck(1)

    for _ in range(2):
        deck.shuffle()
        counts = {}
        num_counts = {}
        while 1:
            card, suit = deck.draw()
            counts[suit] = counts.get(suit, 0) + 1
            num_counts[card] = num_counts.get(card, 0) + 1
            if card is None or suit is None:
                deck.reinit()
                break
            print(deck.to_string(suit, card))

        print("suits counts")
        for key in _suits.keys():
            print("{}:{}".format(_suits[key], counts[key]))

        print("card counts")
        for k in _cards.keys():
            print("{}:{}".format(_cards[k], num_counts[k]))
