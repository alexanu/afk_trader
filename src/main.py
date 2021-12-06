import alpaca_trade_api as tradeapi
import websocket, json
from strategies import Strategy
import boto3


def get_secret_api_token(token_name):
    """
    Accesses AWS Secrets Manager and retrieves the secret token names for the API
    :return: secret token values
    """
    client = boto3.client("secretsmanager", region_name="us-east-1")
    response = client.get_secret_value(SecretId=token_name)
    return response["SecretString"]


class AfkTrader:
    def __init__(self, base_url, socket, api_key, api_secret, symbol):
        self.base_url = base_url
        self.socket = socket
        self.api_key = api_key
        self.api_secret = api_secret
        self.symbol = symbol
        self.api = tradeapi.REST(
            key_id=self.api_key,
            secret_key=self.api_secret,
            base_url=self.base_url,
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
                symbol=self.symbol,
                type=type,
                time_in_force=time_in_force,
                limit_price=limit_price,
            )
            print(order_val)
            return True
        except Exception as e:
            print("An exception occured - {}".format(e))
            return False

    def on_open(self, ws):
        """
        The on_open method to implement when websocket is opened. Subscribes to the stream feed of a particular stock
        :param ws: websocket
        :return: None
        """
        print("Connection Opened")
        auth_data = {"action": "auth", "key": self.api_key, "secret": self.api_secret}
        ws.send(json.dumps(auth_data))
        channel_data = {
            "action": "subscribe",
            # 'trades': [self.symbol],
            # 'quotes': [self.symbol],
            "bars": [self.symbol],
        }
        ws.send(json.dumps(channel_data))

    def on_close(self, ws):
        """
        The on_close method to implement when the websocket connection is closed
        :param ws: websocket
        :return: 'Connection Closed'
        """
        return "Connection Closed"

    def on_message(self, ws, message):
        """
        The on_message method to implement the trading strategy to be executed
        :param ws: websocket
        :param message: websocket message response
        :return: None
        """
        print("Received Message")
        self.mess = json.loads(message)

        Strategy().rsi_indicator(
            RSI_PERIOD=14, RSI_OVERBOUGHT=70, RSI_OVERSOLD=30, message=self.mess
        )


if __name__ == "__main__":

    bot = AfkTrader(
        base_url="https://paper-api.alpaca.markets",  # paper API
        socket="wss://stream.data.alpaca.markets/v1beta1/crypto",  # crypto endpoint
        api_key=get_secret_api_token(token_name="API_KEY_ID"),
        api_secret=get_secret_api_token(token_name="API_SECRET"),
        symbol="BTCUSD",
    )

    ws = websocket.WebSocketApp(
        bot.socket,
        on_open=bot.on_open,
        on_close=bot.on_close,
        on_message=bot.on_message,
    )
    ws.run_forever()
