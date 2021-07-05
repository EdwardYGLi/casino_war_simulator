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
    def __init__(self, n_decks=1, stop_ind=0):
        self.n_decks = n_decks
        self.deck_size = 52
        self.cards = list(range(self.deck_size * self.n_decks))
        self.draw_ind = 0
        self.stop_ind = stop_ind
        self.reshuffle = False

    def seed(self, seed):
        np.random.seed(seed)
        random.seed(seed)

    def shuffle(self, times=7):
        for _ in range(times):
            random.shuffle(self.cards)

    def reinit(self, stop_ind=0):
        self.draw_ind = 0
        self.stop_ind = stop_ind
        self.shuffle()
        self.reshuffle = False

    def deal(self):
        # return value mod 52 % suit(13)
        card = self.cards[self.draw_ind] % 52 % 13
        suit = self.cards[self.draw_ind] % 52 // 13
        self.draw_ind += 1
        self.reshuffle = self.draw_ind >= len(self.cards) - self.stop_ind

        return card, suit

    def draw(self):
        return self.deal()

    def to_string(self, s, c):
        return _suits[s] + " " + _cards[c]


if __name__ == "__main__":
    deck = WarDeck(n_decks=1, stop_ind=0)

    for _ in range(1):
        deck.shuffle()
        counts = {}
        num_counts = {}
        while not deck.reshuffle:
            card, suit = deck.draw()
            counts[suit] = counts.get(suit, 0) + 1
            num_counts[card] = num_counts.get(card, 0) + 1
            print(deck.to_string(suit, card))

        deck.reinit(stop_ind=0)
        print("suits counts")
        for key in _suits.keys():
            print("{}:{}".format(_suits[key], counts[key]))

        print("card counts")
        for k in _cards.keys():
            print("{}:{}".format(_cards[k], num_counts[k]))
