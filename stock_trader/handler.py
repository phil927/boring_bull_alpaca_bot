# Alpaca Paper Trading Credentials
# API Key ID: PKP02C3QC742LGWNPCBO
# Secret Key: nwEK9FcjEyYvIKUvw7QTu5bT0PSXQYBtPesfUhXn
try:
  import unzip_requirements
except ImportError:
  pass

import pytz
import alpaca_trade_api as tradeapi
import urllib.request
import json
import re
from datetime import datetime, date, timedelta
import calendar
from time import sleep
from aws_sns import SnsWrapper
import boto3

stock_to_purchase = "SPXL"
boring_bull_json_url = "http://boringbull.com/assets/js/excel.js"
# 24-hour Format for Trading Time in EST
trading_hour = 15
trading_minute = 30
# Bot will execute trade on X mins either side of trading time
acceptable_trading_window = 5


api = tradeapi.REST(
    key_id="PKP02C3QC742LGWNPCBO",
    secret_key="nwEK9FcjEyYvIKUvw7QTu5bT0PSXQYBtPesfUhXn",
    base_url="https://paper-api.alpaca.markets")


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


# Returns a string, either 'buy', 'sell', or 'hold'
# This is based on dad's json data, if days_in = 1 and days_out = 0, or vice versa, a trade should be made
# Json located at "http://boringbull.com/assets/js/excel.js"
def decide_to_buy_sell_or_hold() -> str:
    data = ''
    with urllib.request.urlopen(boring_bull_json_url) as url:
        data = url.read().decode()
    days_in = re.search(r"(?<=\bfldDaysIn =\s)(\w+)", data).group()
    days_out = re.search(r"(?<=\bfldDaysOut =\s)(\w+)", data).group()
    print(f"Days In: {days_in} Days Out: {days_out}")

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


def error_alert(msg: str):
    # Sns = SnsWrapper(boto3.resource('sns', region_name='us-east-1'))
    # # print("Message ID: ", Sns.publish_text_message("+14047316031", "Hello from Phillip"))
    # topic = Sns.create_topic('')
    # Sns.publish_message(topic, msg, {})
    return {"status": 400, "msg": "Failure with msg " + msg }


def make_trade(trade_action: str):
    if trade_action != "buy" and trade_action != "sell":
        alert("Holding: No trade required today")
    elif trade_action == "buy":
        alert("Buying Stock Today!")
        all_in()
    else:
        alert("Selling Stock Today")
        all_out()


def is_market_open() -> bool:
    clock = api.get_clock()
    print('The market is {}'.format(
        'open.' if clock.is_open else 'closed. No trading today'))
    return clock.is_open

def is_trading_time() -> bool:
    UTC = pytz.utc
    eastern_timezone = pytz.timezone('US/Eastern')
    time_in_us_eastern = datetime.now(eastern_timezone)

    trading_time = datetime(
        time_in_us_eastern.year, time_in_us_eastern.month, time_in_us_eastern.day, trading_hour, trading_minute)
    trading_time = eastern_timezone.localize(trading_time)
    time_until_trading = trading_time - time_in_us_eastern

    if abs(time_until_trading) < timedelta(minutes=acceptable_trading_window):
        alert("It's trading time!")
        return True
    else:
        alert(
            f"Not trading time: \nCurrent Time: {time_in_us_eastern}\nTrading Time: {trading_time}\nTime until Trading: {time_until_trading}")
        return False


def lambda_handler(event, context):
    running_continuosly = False
    print("Lambda Handler Running")
    try:
        while True:
            if is_market_open() and is_trading_time():
                trade_decision = decide_to_buy_sell_or_hold()
                make_trade(trade_decision)
            if not running_continuosly:
                break
            # Sleeps for 5 minutes
            sleep(5*60)
    except Exception as e:
        print("A Critical Error Occured: " + str(e))

if __name__ == "__main__":
    lambda_handler(None, None)
