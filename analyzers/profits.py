# -*- coding: utf-8 -*-
import typing as ty  # noqa

import pandas as pd
from .base import BaseAnalyzer
from .costs import CostAnalyzer


class ProfitAnalyzer(BaseAnalyzer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cost_analyzer = CostAnalyzer(*args, **kwargs)

    def get_return_rate(self,  purchase: pd.DataFrame, current_price: float,
                        include_matching_shares: bool = False) -> float:
        diluted_cost = self.cost_analyzer.get_diluted_cost(purchase,
                                                           include_matching_shares=include_matching_shares)
        return_rate = (current_price - diluted_cost) / diluted_cost
        return return_rate

    # def get_annualized_return_rate(self, purchase: pd.DataFrame, current_price: float) -> float:
    #     return_rate = self.get_return_rate(purchase, current_price)
    #     duration = len(purchase)
    #
    #     annualized_return_rate = (1 + return_rate) ** (1 / 3) - 1
    #     return annualized_return_rate
