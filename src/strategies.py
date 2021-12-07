import numpy as np
import talib
import alpaca_trade_api as tradeapi
from src.main import *


closing_prices = []
in_position = False


class Strategy:
    def __init__(self):
        self.api = tradeapi.REST(
            key_id=bot.api_key,
            secret_key=bot.api_secret,
            base_url=bot.base_url,
            api_version="v2",
        )

    def order(self, side, qty, type, time_in_force, limit_price=None):
        """
        The order method to implment the buy/sell functionality of Afk Trader
        :param side: buy or sell
        :param qty: amount of the stock you would like to buy
        :param type: type of trade to be made usually 'market'
        :param time_in_force: how long an order will remain active before it is executed or expired
        :param limit_price: limit price of the side if available
        :return: True or False
        """
        try:
            print("Sending order")
            order_val = self.api.submit_order(
                side=side,
                qty=qty,
                symbol=bot.symbol,
                type=type,
                time_in_force=time_in_force,
                limit_price=limit_price,
            )
            print(order_val)
            return True
        except Exception as e:
            print("An exception occured - {}".format(e))
            return False

    def rsi_indicator(self, RSI_PERIOD, RSI_OVERBOUGHT, RSI_OVERSOLD, message):
        """
        Basic trading stretegy implemented using a RSI value to determine if the stock is overbought or oversold. And
        sends buy/sell orders accordingly to the Alpaca API
        :param RSI_PERIOD: The period used to calculate the RSI value
        :param RSI_OVERBOUGHT: The RSI value indicating when a stock should be considered overbought
        :param RSI_OVERSOLD: The RSI value indicating when a stock should be considered oversold
        :param message: websocket message
        :return: None
        """

        global in_position

        self.message = message
        self.RSI_PERIOD = RSI_PERIOD
        self.RSI_OVERBOUGHT = RSI_OVERBOUGHT
        self.RSI_OVERSOLD = RSI_OVERSOLD

        print(self.message)
        open_price = self.message[0]["o"]
        close_price = self.message[0]["c"]
        closing_prices.append(float(close_price))

        print(
            "The close price is {}".format(close_price),
            "The open price is {}".format(open_price),
        )
        print("Closing prices list: {} ".format(closing_prices))

        if len(closing_prices) > self.RSI_PERIOD:
            np_closing_prices = np.array(closing_prices)
            rsi_values = talib.RSI(np_closing_prices, self.RSI_PERIOD)

            print("All rsi's calculated so far: {}".format(rsi_values))

            last_rsi_value = rsi_values[-1]

            print("The current rsi value is {}".format(last_rsi_value))

            if last_rsi_value > self.RSI_OVERBOUGHT:
                if in_position:
                    print("The Stock Is Overbought: SELL NOW!!!")
                    # put alpaca sell logic here
                    order_succeeded = self.order(
                        side="sell", qty=1, type="market", time_in_force="day"
                    )

                    if order_succeeded:
                        in_position = False
                else:
                    print(
                        "The stock is overbought but, you do not own any. So, you are unable to sell."
                    )

            if last_rsi_value < self.RSI_OVERSOLD:
                if in_position:
                    print(
                        "The Stock Is oversold but, you already own it. So, you are unable to buy."
                    )
                else:
                    print("The Stock Is Oversold: BUY NOW!!!")
                    # put alpaca buy order logic here
                    order_succeeded = self.order(
                        side="buy", qty=1, type="market", time_in_force="day"
                    )
                    if order_succeeded:
                        in_position = True
