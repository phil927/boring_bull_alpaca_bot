# Alpaca Paper Trading Credentials
# API Key ID: PKP02C3QC742LGWNPCBO
# Secret Key: nwEK9FcjEyYvIKUvw7QTu5bT0PSXQYBtPesfUhXn
import pytz
import alpaca_trade_api as tradeapi
import urllib.request
import json
import re
from datetime import datetime, date
import calendar

stock_to_purchase = "SPXL"
boring_bull_json_url = "http://boringbull.com/assets/js/excel.js"

api = tradeapi.REST(
    key_id="PKP02C3QC742LGWNPCBO",
    secret_key="nwEK9FcjEyYvIKUvw7QTu5bT0PSXQYBtPesfUhXn",
    base_url="https://paper-api.alpaca.markets")


# api.submit_order("SPXL", qty=1, side="buy", type="market", time_in_force="day")


def all_in():
    # Get available money to trade
    response = api.get_account()
    avail_amount_trade = float(response.non_marginable_buying_power)
    print(f'Amount to trade is: ${avail_amount_trade:,.2f}')

    if(avail_amount_trade <= 0):
        print("You're all out of funds!")
        return

    print("Going all in!")
    response = api.submit_order(stock_to_purchase, notional=avail_amount_trade,
                                side="buy", type="market", time_in_force="day")
    print(
        f"Buy Order Created for ${float(response.notional):,.2f} of {stock_to_purchase:s}")


def all_out():
    # Get existing position on stock_to_trade
    # stock_to_purchase = "PLTR"
    response = api.list_positions()

    quantity_of_stock = 0
    for position in response:
        if position.symbol == stock_to_purchase:
            quantity_of_stock += float(position.qty)

    if quantity_of_stock <= 0:
        alert(
            f"Attempted to Sell all Positions of {stock_to_purchase} but None Found")
        return
    else:
        print(
            f"Selling quantity of {stock_to_purchase}: {quantity_of_stock:.10f}")

        response = api.submit_order(stock_to_purchase, qty=quantity_of_stock,
                                    side="sell", type="market", time_in_force="day")
        print(
            f"Sell Order Created for {float(response.qty):.2f} shares of {stock_to_purchase:s}")


# Returns an int list of form [days_in, days_out]


def get_days_in_and_out():
    hardcode_data = "var fldDaysIn = 5; var fldDaysOut = 0;"
    data = ''
    with urllib.request.urlopen(boring_bull_json_url) as url:
        data = url.read().decode()
    # data = hardcode_data
    days_in = re.search(r"(?<=\bfldDaysIn =\s)(\w+)", data).group()
    days_out = re.search(r"(?<=\bfldDaysOut =\s)(\w+)", data).group()
    print(f"Days In: {days_in} Days Out: {days_out}")
    return [int(days_in), int(days_out)]


# Returns a string, either 'buy', 'sell', or 'hold'
def decide_to_buy_sell_or_hold(days_in: int, days_out: int) -> str:
    if days_in == 1 and days_out == 0:
        print("Buying!")
        return "buy"
    elif days_in == 0 and days_out == 1:
        print("Selling!")
        return "sell"
    else:
        print("Holding!")
        return "hold"


def alert(msg: str):
    print(msg)


def make_trade(trade_action: str):
    if trade_action != "buy" and trade_action != "sell":
        alert("Holding: No trade required today")
    elif trade_action == "buy":
        alert("Buying Stock Today!")
    else:
        alert("Selling Stock Today")


def is_time_to_trade() -> bool:
    trading_hour = 15
    trading_minute = 30

    UTC = pytz.utc
    timeZ_Ea = pytz.timezone('US/Eastern')
    print(timeZ_Ea)
    time_in_us_eastern = timeZ_Ea.localize(datetime.now())
    print(time_in_us_eastern)

    trading_time = datetime(
        time_in_us_eastern.year, time_in_us_eastern.month, time_in_us_eastern.day, trading_hour, trading_minute, tzinfo=timeZ_Ea)
    print(trading_time)

    time_until_trading = abs(trading_time - time_in_us_eastern)
    print(f"Time until Trading: {time_until_trading}")


# BUG IN CALCULATING the time until trading

    print(date.today(tzinfo=timeZ_Ea).year())

    trading_time = datetime(time_in_us_eastern.year(), time_in_us_eastern.month(
    ), time_in_us_eastern.day(), hour=15, minute=30, second=0, microsecond=0, tzinfo=timeZ_Ea)

    print(time_in_us_eastern)
    print(time_in_us_eastern.strftime('%Y-%m-%d %H:%M:%S %Z %z'))
    print(time_in_us_eastern.strftime('-%d %H:%M:%S %Z %z'))
    day_of_the_week_index = time_in_us_eastern.weekday()
    day_of_the_week_index = 4
    day_of_the_week = calendar.day_name[day_of_the_week_index]
    print(f"{day_of_the_week} with index: {day_of_the_week_index:d}")

    if day_of_the_week_index >= 5:
        alert("It's the weekend, no trades possible")
        return False

    # get_days_in_and_out()
# decide_to_buy_sell_or_hold(5, 0)
# days_list = get_days_in_and_out()
# trade_action = decide_to_buy_sell_or_hold(
#     days_in=days_list[0], days_out=days_list[1])
# make_trade(trade_action)
# is_time_to_trade()
all_out()
# all_in()
