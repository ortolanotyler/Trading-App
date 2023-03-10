#!/usr/bin/python3
from trader import trader
import randy_random
import time
import math
from config import config_dict

"""
Cassandra Classic
"""


def find_profit():
    lst = []
    owned_stocks = trader.owned_stocks()
    for stock in owned_stocks:
        if made_profit(stock):
            lst.append(stock)
    return lst


def made_profit(sym):
    plpc = trader.stock_plpc(sym)
    profit_margen = 0.02
    return plpc > profit_margen


def find_loss():
    lst = []
    ownd_stocks = trader.owned_stocks()
    for stock in ownd_stocks:
        if made_loss(stock):
            lst.append(stock)
    return lst


def made_loss(sym):
    plpc = trader.stock_plpc(sym)
    loss_margen = -0.065
    return plpc < loss_margen


def find_market_loss():
    market_assets = trader.nasdaq_assets()
    market_assets = market_assets[:20]
    loss_lst = []
    for asset in market_assets:
        sym = asset.symbol
        if market_made_loss(sym):
            loss_lst.append(sym)
    return loss_lst


def find_market_growth():
    market_assets = trader.nasdaq_assets()
    market_assets = market_assets[:20]
    loss_lst = []
    for asset in market_assets:
        sym = asset.symbol
        if market_made_loss(sym):
            loss_lst.append(sym)
    return loss_lst


def market_made_loss(sym):
    plpc = trader.value_of_stock(sym)
    loss_margen = 5
    return plpc < loss_margen


def market_made_profit(sym):
    plpc = trader.value_of_stock(sym)
    loss_margen = 5
    return plpc > loss_margen


def find_losing_stock():
    losing_stocks = find_market_loss()
    lost_lst = []
    for sym in losing_stocks:
        pl_change = trader.get_week_pl_change(sym)
        lost_lst += [(sym, pl_change)]
    lost_lst = sorted(lost_lst, key=lambda l:l[1])
    if config_dict["DEBUG"]:
        print(" [-] losing stock : ")
        print(lost_lst)
    lost_lst = lost_lst[len(lost_lst)%2]
    return lost_lst[0]


def find_growing_stock():
    losing_stocks = find_market_loss()
    lost_lst = []
    for sym in losing_stocks:
        pl_change = trader.get_week_pl_change(sym)
        lost_lst += [(sym, pl_change)]
    lost_lst = sorted(lost_lst, key=lambda l:l[1])
    if config_dict["DEBUG"]:
        print(" [-] losing stock : ")
        print(lost_lst)
    lost_lst = lost_lst[len(lost_lst)%2]
    return lost_lst[0]


def investment_qty_lossing_stock(sym):
    pl_change = trader.get_week_pl_change(sym)
    qty = int(math.sqrt(int(pl_change)))
    if qty < 0: # should never happend sqrt should never be negative
        qty = -1 * qty
    if qty == 0 or qty == float(0): # cast for 0, can be 0.0 
        qty = 2
    if config_dict["DEBUG"]:
        print(" [+] investment " + str(sym) + " : " + str(qty))
    return qty


def one_instance_cassandra():
    #find to sell
    stock_profits = find_profit()
    
    if config_dict["DEBUG"]:
        print(" [-] stock profit lst : ")
        print(stock_profits)
    
    if stock_profits:
        trader.sell_list(stock_profits)
    
    randy_random.random_buy()
    #losing_stock = find_losing_stock()
    #losing_stock_invst = investment_qty_lossing_stock(losing_stock)
    
    # find stock to buy
    #trader.buy(losing_stock_invst, losing_stock)


def run_cassandra():
    """ runs Cassandra forever """
    hour = 60 * 60
    wait = hour//4
    print(" [*] Cassandra Classic is running ")
    while True:
        if config_dict["DEBUG"]:
            print(" [*] is NASDAQ open " + str(trader.exchange_open()))
        if trader.exchange_open():
            one_instance_cassandra()
            time.sleep(wait)
