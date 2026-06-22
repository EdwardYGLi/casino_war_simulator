"""
Created by edwardli on 7/4/21
"""

import argparse
import os

from matplotlib import pyplot as plt
from tqdm import tqdm

from deck import WarDeck

_outdir = "./output"


def run_simulation(deck, args, war_n, progress=True):
    """Run num_sims games using a "1 in war_n" deterministic war strategy.

    On every tie the player goes to war on 1 of every ``war_n`` ties (counting
    ties within a session) and surrenders the rest. ``war_n == 1`` means always
    go to war; larger ``war_n`` means war less often. This is something a person
    can actually execute at a table by counting ties.

    Returns (win, lose, ties, total_money, results).
    """
    results = []
    win = 0
    lose = 0
    total_money = 0
    iterator = range(args.num_sims)
    if progress:
        iterator = tqdm(iterator)
    for _ in iterator:
        deck.reinit(stop_ind=10)
        # burn at start
        deck.deal()
        money = args.money
        tie_count = 0
        while not deck.reshuffle:
            if money <= 0:
                money = 0
                break

            # draw cards
            player = deck.draw()
            dealer = deck.draw()

            # win
            if player[0] > dealer[0]:
                money += args.bet
            # lose
            elif player[0] < dealer[0]:
                money -= args.bet
            # tie
            else:
                tie_count += 1
                # surrender on ties that are not the war_n-th one
                if tie_count % war_n != 0:
                    money -= args.bet / 2
                # war on every war_n-th tie
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
                    if player[0] > dealer[0]:
                        money += args.bet
                    # lose
                    elif player[0] < dealer[0]:
                        money -= 2 * args.bet
                    # tie
                    else:
                        money += 2 * args.bet
        results.append(money)
        if money > args.money:
            win += 1
        elif money < args.money:
            lose += 1
        total_money += money
    ties = args.num_sims - win - lose
    return win, lose, ties, total_money, results


def main(args):
    exp_name = "d_{}_wn_{}_m_{}_b_{}_n_{}".format(args.decks,
                                                                    args.war_n, args.money,
                                                                    args.bet, args.num_sims)

    deck = WarDeck(args.decks, stop_ind=10)
    win, lose, ties, total_money, results = run_simulation(deck, args, args.war_n)
    print(len(results))
    plt.figure()
    plt.hist(results)
    plt.xlabel("money ($)")
    plt.ylabel("occurence (out of {})".format(args.num_sims))
    plt.savefig(os.path.join(_outdir, "{}_distribution.png".format(exp_name)))

    with open(os.path.join(_outdir, "{}_stats.txt".format(exp_name)), "w") as f:
        f.write("wins: {}, win %: {}\n".format(win, win / args.num_sims))
        f.write("losses: {}, lose %: {}\n".format(lose, lose / args.num_sims))
        f.write("ties: {}, tie %: {}\n".format(ties, ties / args.num_sims))
        f.write("expected_value: {}".format(total_money/args.num_sims))


def sweep(args):
    """Sweep the "1 in n" war strategy and chart its effect on expected value."""
    exp_name = "d_{}_m_{}_b_{}_n_{}_sweep_{}".format(args.decks, args.money,
                                                     args.bet, args.num_sims,
                                                     args.sweep_max)

    deck = WarDeck(args.decks, stop_ind=10)
    war_ns = list(range(1, args.sweep_max + 1))
    expected_values = []
    for war_n in tqdm(war_ns):
        _, _, _, total_money, _ = run_simulation(deck, args, war_n, progress=False)
        expected_values.append(total_money / args.num_sims)

    plt.figure()
    plt.plot(war_ns, expected_values, marker="o")
    plt.axhline(args.money, color="gray", linestyle="--", label="starting money")
    plt.xlabel("war strategy (go to war on 1 of every n ties)")
    plt.ylabel("expected value ($)")
    plt.title("war frequency (1 in n ties) vs expected value")
    plt.xticks(war_ns)
    plt.legend()
    plt.savefig(os.path.join(_outdir, "{}_chart.png".format(exp_name)))

    with open(os.path.join(_outdir, "{}_stats.txt".format(exp_name)), "w") as f:
        f.write("war_n,expected_value\n")
        for war_n, ev in zip(war_ns, expected_values):
            f.write("{},{}\n".format(war_n, ev))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("arg parser for casino war simulator")
    parser.add_argument("-d", "--decks", help="number of decks", type=int, default=12)
    parser.add_argument("--war_n", help="go to war on 1 of every n ties (1 = always war)",
                        type=int, default=1)
    parser.add_argument("-m", "--money", help="player money at start", type=float, default=1000)
    parser.add_argument("-b", "--bet", help="default bet amount", type=float, default=25)
    parser.add_argument("-n", "--num_sims", help="number of simulations", type=int, default=1000)
    parser.add_argument("--sweep", help="sweep the 1-in-n war strategy and chart expected value",
                        action="store_true")
    parser.add_argument("--sweep_max", help="largest n to sample in a 1-in-n sweep",
                        type=int, default=10)
    args = parser.parse_args()
    os.makedirs(_outdir, exist_ok=True)
    if args.sweep:
        sweep(args)
    else:
        main(args)
