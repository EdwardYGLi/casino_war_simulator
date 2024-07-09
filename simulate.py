"""
Created by edwardli on 7/4/21
"""

import argparse
import os
import random

from matplotlib import pyplot as plt
from tqdm import tqdm

from deck import WarDeck

_outdir = "./output"


def main(args):
    exp_name = "d_{}_wr_{}_m_{}_b_{}_n_{}".format(args.decks,
                                                                    args.war_ratio, args.money,
                                                                    args.bet, args.num_sims)
    results = []

    deck = WarDeck(args.decks, stop_ind=10)
    win = 0
    lose = 0
    for _ in tqdm(range(args.num_sims)):
        deck.reinit(stop_ind=10)
        # burn at start
        deck.deal()
        money = args.money
        while not deck.reshuffle:
            if money <= 0:
                results.append(0)
                break

            # draw cards
            player = deck.draw()
            dealer = deck.draw()

            # win
            if player[1] > dealer[1]:
                money += args.bet
            # lose
            elif player[1] < dealer[1]:
                money -= args.bet
            # tie
            else:
                # surrender
                if random.random() > args.war_ratio:
                    money -= args.bet / 2
                # war
                else:
                    # burn
                    for _ in range(3):
                        deck.deal()

                    player = deck.deal()

                    # burn
                    for _ in range(3):
                        deck.deal()

                    dealer = deck.deal()

                    # win
                    if player[1] > dealer[1]:
                        money += args.bet
                    # lose
                    elif player[1] < dealer[1]:
                        money -= 2 * args.bet
                    # tie
                    else:
                        money += 2 * args.bet
        if money > 0 :
            results.append(money)
        if money > args.money:
            win += 1
        elif money < args.money:
            lose += 1
    print(len(results))
    plt.figure()
    plt.hist(results)
    plt.xlabel("money ($)")
    plt.ylabel("occurence (out of {})".format(args.num_sims))
    plt.savefig(os.path.join(_outdir, "{}_distribution.png".format(exp_name)))

    with open(os.path.join(_outdir, "{}_stats.txt".format(exp_name)), "w") as f:
        f.write("wins: {}, win %: {}\n".format(win, win / args.num_sims))
        f.write("losses: {}, lose %: {}\n".format(lose, lose / args.num_sims))
        ties = args.num_sims - win - lose
        f.write("ties: {}, tie %: {}\n".format(ties, ties / args.num_sims))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("arg parser for casino war simulator")
    parser.add_argument("-d", "--decks", help="number of decks", default=12)
    parser.add_argument("--war_ratio", help="ratio of war on ties", default=1)
    parser.add_argument("-m", "--money", help="player money at start", default=1000)
    parser.add_argument("-b", "--bet", help="default bet amount", default=25)
    parser.add_argument("-n", "--num_sims", help="number of simulations", default=1000)
    args = parser.parse_args()
    os.makedirs(_outdir, exist_ok=True)
    main(args)
