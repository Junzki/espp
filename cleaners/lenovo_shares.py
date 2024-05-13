# -*- coding: utf-8 -*-
import typing as ty

import re
import pandas as pd


class LenovoSharesMixin(object):
    OUTPUT_COLUMNS = ['plan', 'date', 'local_currency', 'plan_currency', 'exchange_rate',
                      'contribution_local', 'contribution_plan', 'purchase_price',
                      'contribution_shares', 'matching_shares', 'total_shares']

    FIELD_TOTAL_SHARES = 'total_shares'
    FIELD_MATCHING_SHARES = 'matching_shares'
    FIELD_CONTRIBUTION_SHARES = 'contribution_shares'
    FIELD_CONTRIBUTION = 'contribution_plan'
    FIELD_PURCHASE_PRICE = 'purchase_price'


class LenovoSharesCleaner(LenovoSharesMixin):
    SKIP_ROW = 5
    CURRENCY_PATTERN = re.compile(r'.\s?(?P<value>(\d,?)+\.\d+)\s(?P<currency>\w{3})')

    def load(self, file_path: str) -> pd.DataFrame:
        df = pd.read_csv(file_path, skiprows=self.SKIP_ROW)
        df['Date'] = pd.to_datetime(df['Date'])
        df['Date'] = df['Date'].apply(lambda x: x.replace(day=1))
        contribution = df[df['Description'] == 'Contribution']
        purchase = df[df['Description'] == 'Purchase']

        purchase['Contribution Amount (Local Currency)'] = purchase.apply(
            lambda x: self.find_contribution_by_month(contribution, x['Plan Year'], x['Date']),
            axis=1
        )

        output_ = purchase.apply(self.clean_row, axis=1)
        return output_

    @staticmethod
    def find_contribution_by_month(contribution: pd.DataFrame,
                                   plan_year, date_) -> ty.Optional[str]:
        contribute_date = date_ - pd.DateOffset(months=1)
        found = contribution[(contribution['Plan Year'] == plan_year) &
                             (contribution['Date'] == contribute_date)]
        try:
            return found['Contribution Amount (Local Currency)'].values[0]
        except IndexError:
            return None

    @classmethod
    def cast_currency(cls, in_: str) -> (int, str):
        m = cls.CURRENCY_PATTERN.match(in_)
        if not m:
            return 0, None
        groups = m.groupdict()
        num = groups['value'].replace(',', '').replace('.', '')
        currency = groups['currency']
        num = int(num)
        return num, currency

    @classmethod
    def clean_row(cls, row):
        plan = row['Plan Year']
        date_ = row['Date']
        contribution_local, local_currency = cls.cast_currency(row['Contribution Amount (Local Currency)'])
        contribution_plan, plan_currency = cls.cast_currency(row['Contribution Amount (Plan Currency)'])
        exchange_rate = row['Exchange Rate']
        purchase_price, __ = cls.cast_currency(row['Purchase Price (Plan Currency)'])
        contribution_shares = row['Contribution Shares Purchased']
        matching_shares = row['Matching Shares']
        total_shares = row['Total Shares Purchased']

        result = (plan, date_, local_currency, plan_currency, exchange_rate, contribution_local, contribution_plan,
                  purchase_price, contribution_shares, matching_shares, total_shares)
        result = dict(zip(cls.OUTPUT_COLUMNS, result))
        result = pd.Series(result)
        return result
