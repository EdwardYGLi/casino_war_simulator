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
    deck = WarDeck(args.decks, stop_ind=10)

    # run the "1 in n" sweep once, keeping full results so we can also draw the
    # money distribution for the chosen strategy without re-simulating it
    war_ns = list(range(1, args.sweep_max + 1))
    runs = {}
    for war_n in tqdm(war_ns):
        runs[war_n] = run_simulation(deck, args, war_n, progress=False)
    if args.war_n not in runs:
        runs[args.war_n] = run_simulation(deck, args, args.war_n, progress=False)

    base = "d_{}_m_{}_b_{}_n_{}".format(args.decks, args.money, args.bet, args.num_sims)

    # chart 1: distribution of final money for the chosen war_n
    win, lose, ties, total_money, results = runs[args.war_n]
    dist_name = "{}_wn_{}".format(base, args.war_n)
    plt.figure()
    plt.hist(results)
    plt.xlabel("money ($)")
    plt.ylabel("occurence (out of {})".format(args.num_sims))
    plt.title("final money distribution (war on 1 of every {} ties)".format(args.war_n))
    plt.savefig(os.path.join(_outdir, "{}_distribution.png".format(dist_name)))

    with open(os.path.join(_outdir, "{}_stats.txt".format(dist_name)), "w") as f:
        f.write("wins: {}, win %: {}\n".format(win, win / args.num_sims))
        f.write("losses: {}, lose %: {}\n".format(lose, lose / args.num_sims))
        f.write("ties: {}, tie %: {}\n".format(ties, ties / args.num_sims))
        f.write("expected_value: {}".format(total_money / args.num_sims))

    # chart 2: war frequency (1 in n ties) vs expected value across the sweep
    expected_values = [runs[n][3] / args.num_sims for n in war_ns]
    sweep_name = "{}_sweep_{}".format(base, args.sweep_max)
    plt.figure()
    plt.plot(war_ns, expected_values, marker="o")
    plt.axhline(args.money, color="gray", linestyle="--", label="starting money")
    plt.xlabel("war strategy (go to war on 1 of every n ties)")
    plt.ylabel("expected value ($)")
    plt.title("war frequency (1 in n ties) vs expected value")
    plt.xticks(war_ns)
    plt.legend()
    plt.savefig(os.path.join(_outdir, "{}_chart.png".format(sweep_name)))

    with open(os.path.join(_outdir, "{}_stats.txt".format(sweep_name)), "w") as f:
        f.write("war_n,expected_value\n")
        for n, ev in zip(war_ns, expected_values):
            f.write("{},{}\n".format(n, ev))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("arg parser for casino war simulator")
    parser.add_argument("-d", "--decks", help="number of decks", type=int, default=12)
    parser.add_argument("--war_n", help="go to war on 1 of every n ties (1 = always war)",
                        type=int, default=1)
    parser.add_argument("-m", "--money", help="player money at start", type=float, default=1000)
    parser.add_argument("-b", "--bet", help="default bet amount", type=float, default=25)
    parser.add_argument("-n", "--num_sims", help="number of simulations", type=int, default=1000)
    parser.add_argument("--sweep_max", help="largest n to sample in the 1-in-n sweep chart",
                        type=int, default=10)
    args = parser.parse_args()
    os.makedirs(_outdir, exist_ok=True)
    main(args)
