# -*- coding: utf-8 -*-
import sys
import typing as ty  # noqa

import argparse
from cleaners.lenovo_shares import LenovoSharesMixin, LenovoSharesCleaner
from analyzers.costs import CostAnalyzer
from analyzers.profits import ProfitAnalyzer

parser = argparse.ArgumentParser()
parser.add_argument('--current-price', type=float, help="Current stock price")
parser.add_argument('file_path', type=str, help='Path to the file to be analyzed')


def main(*argv):
    args, __ = parser.parse_known_args(args=argv)
    cleaner = LenovoSharesCleaner()
    costs = CostAnalyzer(LenovoSharesMixin)
    profits = ProfitAnalyzer(LenovoSharesMixin)

    purchase_ = cleaner.load(args.file_path)
    diluted_cost = costs.get_diluted_cost(purchase_, False)
    diluted_cost_with_matching = costs.get_diluted_cost(purchase_, True)

    print("Diluted Cost: ", diluted_cost)
    print("Diluted Cost with Matching: ", diluted_cost_with_matching)

    current_price = args.current_price
    if not current_price:
        return

    return_rate = profits.get_return_rate(purchase_, current_price, False)
    return_rate_with_matching = profits.get_return_rate(purchase_, current_price, True)

    print("Return Rate: ", return_rate)
    print("Return Rate with Matching: ", return_rate_with_matching)


if __name__ == '__main__':
    main(*sys.argv[1:])
