# -*- coding: utf-8 -*-
import typing as ty


class BaseAnalyzer(object):
    field_total_shares = 'total_shares'
    field_contribution_shares = 'contribution_shares'
    field_contribution = 'contribution'
    field_purchase_price = 'purchase_price'

    def __init__(self, mixin: ty.Any = None):
        if mixin:
            self.setup_fields(mixin)

    def setup_fields(self, mixin: ty.Any):
        self.field_contribution = getattr(mixin, 'FIELD_CONTRIBUTION', None)
        self.field_purchase_price = getattr(mixin, 'FIELD_PURCHASE_PRICE', None)
        self.field_contribution_shares = getattr(mixin, 'FIELD_CONTRIBUTION_SHARES', None)
        self.field_total_shares = getattr(mixin, 'FIELD_TOTAL_SHARES', None)
