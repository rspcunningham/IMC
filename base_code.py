import pandas as pd
import numpy as np
import statistics
import math
from typing import List, Dict

from datamodel import OrderDepth, TradingState, Order, Trade, Symbol

# ----------------------------------------------------------------------------------------------------------------

charts = pd.DataFrame()
first_run = True
iter = 0

# ----------------------------------------------------------------------------------------------------------------

# get the most updated price of product


def get_new_price(own_trades: Dict[Symbol, List[Trade]], market_trades: Dict[Symbol, List[Trade]], symbol: Symbol):
    total = 0
    quantity = 0

    if symbol in market_trades:
        for trade in market_trades[symbol]:
            total += trade.price * trade.quantity
            quantity += trade.quantity

    if symbol in own_trades:
        for trade in own_trades[symbol]:
            total += trade.price * trade.quantity
            quantity += trade.quantity

    if quantity == 0:
        return None

    return total / quantity

# time_stamp from TradingState called from run function


def build_price_chart(state: TradingState):

    global charts

    # new_prices = get_new_prices(state.own_trades, state.market_trades)
    new_row = []

    for symbol in state.listings:
        new_price = get_new_price(
            state.own_trades, state.market_trades, symbol)

        if new_price == None:
            new_price = charts[symbol].iloc[-1]

        new_row.append(new_price)

    charts.loc[state.timestamp] = new_row


class Trader:
    def run(self, state: TradingState) -> Dict[str, List[Order]]:

        global charts, first_run, iter
        iter += 1

        if first_run:
            for symbol in state.listings:
                charts[symbol] = []
            first_run = False

        build_price_chart(state)

        if iter == 50:
            print(charts)

        result = {}
        return result
