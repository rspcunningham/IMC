import pandas as pd
import numpy as np
import statistics
import math
from typing import List, Dict

from datamodel import OrderDepth, TradingState, Order, Trade, Symbol

LIMITS = {Symbol('PEARLS'): 20, Symbol('BANANAS'): 20}
STRATEGY = {}

# ----------------------------------------------------------------------------------------------------------------


def get_histogram(depths: OrderDepth, own_trades: List[Trade], market_trades: List[Trade]) -> list[list[int]]:

    bids = []
    asks = []

    for trade in market_trades:
        bids.extend([trade.price] * trade.quantity)
        asks.extend([trade.price] * trade.quantity)

    for trade in own_trades:
        bids.extend([trade.price] * trade.quantity)
        asks.extend([trade.price] * trade.quantity)

    for price in depths.buy_orders:
        bids.extend([price] * depths.buy_orders[price])

    for price in depths.sell_orders:
        asks.extend([price] * -depths.sell_orders[price])

    return [bids, asks]


def position_controller(current_position: int, target_position: int, k: float) -> float:

    position_error = current_position - target_position

    return 2/(1 + np.exp(position_error * k))


def balancer(position, symbol):

    if symbol in position:
        ask_quantity = LIMITS[symbol] + position[symbol]
        bid_quantity = LIMITS[symbol] - position[symbol]
    else:
        ask_quantity = LIMITS[symbol]
        bid_quantity = LIMITS[symbol]

    return ask_quantity, bid_quantity


def marketmaking(k, bids, asks, total, position, symbol):
    # get statistics
    mean_total = statistics.mean(total)

    # calculate what spread we want to take
    spread_min = 2
    spread_calc = (max(bids) - min(asks)) / 1.5
    spread = max(spread_min, spread_calc)

    print(f'{symbol}: {spread_calc}')

    if symbol in position:
        price_factor = position_controller(position[symbol], 0, k)
    else:
        price_factor = 1

    print(mean_total)

    # calculate our bid and ask prices
    bid_price = mean_total * price_factor - spread/2
    ask_price = mean_total * price_factor + spread/2

    ask_quantity, bid_quantity = balancer(position, symbol)

    # assemble outgoing orders
    return [Order(symbol, bid_price, bid_quantity), Order(
        symbol, ask_price, -ask_quantity)]


def stablecoin(ask_price, bid_price, total, position, symbol) -> List[Order]:

    ask_quantity, bid_quantity = balancer(position, symbol)

    return [Order(symbol, bid_price, bid_quantity), Order(symbol, ask_price, -ask_quantity)]


# ----------------------------------------------------------------------------------------------------------------


class Trader:
    def run(self, state: TradingState) -> Dict[str, List[Order]]:

        orders = {}

        print(state.position)

        for symbol in state.listings:

            # Get current order book
            bids, asks = get_histogram(
                state.order_depths.get(symbol, OrderDepth()), state.own_trades.get(symbol, []), state.market_trades.get(symbol, []))

            total = [*bids, *asks]

            if not bids or not asks or not total:
                continue  # if the order book is empty, make no offers

            if symbol == 'PEARLS':
                orders[symbol] = stablecoin(
                    10002, 9998, total, state.position, symbol)
            else:
                orders[symbol] = marketmaking(
                    0, bids, asks, total, state.position, symbol)

        return orders
