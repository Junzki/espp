# -*- coding: utf-8 -*-
import typing as ty  # noqa

import pandas as pd
from .base import BaseAnalyzer


class CostAnalyzer(BaseAnalyzer):

    def get_diluted_cost(self, purchase: pd.DataFrame,
                         include_matching_shares: bool = False) -> float:
        if include_matching_shares:
            shares = purchase[self.field_total_shares].sum()
        else:
            shares = purchase[self.field_contribution_shares].sum()

        total_cost = purchase[self.field_contribution].sum() / 100.0  # To float
        diluted_cost = total_cost / shares
        return diluted_cost

    def get_average_cost(self, purchase: pd.DataFrame) -> float:
        average_cost = 0
        total_shares = 0

        def _collate(contribution: int, shares: float):
            nonlocal average_cost, total_shares
            next_shares_ = total_shares + shares
            next_average_cost = (average_cost * total_shares + contribution / 100.0) / next_shares_
            average_cost = next_average_cost
            total_shares = next_shares_

        purchase[[self.field_contribution, self.field_contribution_shares]].apply(lambda x: _collate(*x), axis=1)
        return average_cost


if __name__ == '__main__':
    from cleaners.lenovo_shares import LenovoSharesCleaner, LenovoSharesMixin

    cleaner = LenovoSharesCleaner()
    purchase_ = cleaner.load('data/ContributionHistory.csv')
    az_ = CostAnalyzer()
    az_.setup_fields(LenovoSharesMixin)
    print("Diluted Cost: ", az_.get_diluted_cost(purchase_, False))
    print("AVG Cost: ", az_.get_average_cost(purchase_))
