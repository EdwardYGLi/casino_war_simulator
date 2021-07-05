"""
Created by edwardli on 7/4/21
"""

import argparse
import os
from deck import WarDeck
_outdir = "./output"


def main(args):
    exp_name = "d_{}_tr_{}_tp_{}_wr_{}_m_{}_b_{}_n_{}".format(args.decks, args.tie_wager_ration,
                                                              args.tie_wager_payout, args.war_ratio, args.money,
                                                              args.bet, args.num_sims)
    results = []

    deck = WarDeck(args.num_decks,stop_ind=8)
    for n in range(args.num_sims):
        deck.shuffle()
        money = args.money
        while not deck.reshuffle:




if __name__ == "__main__":
    parser = argparse.ArgumentParser("arg parser for casino war simulator")
    parser.add_argument("-d", "--decks", help="number of decks"., default=12)
    parser.add_argument("--tie_wager_ratio", help="percentage of tie wagers to bet", default=0.5)
    parser.add_argument("--tie_wager_payout", help="tie wager payout", default=10)
    parser.add_argument("--war_ratio", help="ratio of war on ties", default=0.5)
    parser.add_argument("-m,--money", help="player money at start", default=1000)
    parser.add_argument("-b", "--bet", help="default bet amount", default=25)
    parser.add_argument("-n", "--num_sims", help="number of simulations", default=100)
    args = parser.parse_args()
    os.makedirs(_outdir, exist_ok=True)
    main(args)
