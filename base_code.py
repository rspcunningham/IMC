import pandas as pd
import numpy as np
import statistics
import math
from typing import List, Dict

from datamodel import OrderDepth, TradingState, Order, Trade, Symbol

# ----------------------------------------------------------------------------------------------------------------

charts = {} # {'BAN': df}
has_run = False

# ----------------------------------------------------------------------------------------------------------------

# get the most updated price of product
def get_new_prices(own_trades: Dict[Symbol, List[Trade]], market_trades: Dict[Symbol, List[Trade]]):
    new_prices = {}

    for symbol in market_trades:
        total = 0
        quantity = 0
        for trade in market_trades[symbol]:
            total += trade.price * trade.quantity
            quantity += trade.quantity
        
        if symbol in own_trades:
            for trade in own_trades[symbol]:
                total += trade.price * trade.quantity
                quantity += trade.quantity
        
        new_price = total / quantity
        new_prices[symbol] = new_price

    return new_prices # {'BAN': $241.12}

# time_stamp from TradingState called from run function
def build_price_chart(state: TradingState):
    new_prices = get_new_prices(state.own_trades, state.market_trades)

    for symbol in charts:
        df = charts[symbol]
        if symbol in new_prices:
            new_row = pd.DataFrame({'price': new_prices[symbol]}, index=[state.timestamp])
            df = df.append(new_row)
        else:
            new_row = pd.DataFrame({'price': df['price'].iloc[-1]}, index=[state.timestamp])
            df = df.append(new_row)

# init
def initalize_price_chart(symbol):
    df = pd.DataFrame(columns=['price'])
    charts[symbol] = df




class Trader:
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        if not has_run:
            for symbol in state.listings:
                if symbol not in charts:
                    initalize_price_chart(symbol)
            has_run = True


        result = {}
        return result
    

