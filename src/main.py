import websocket, json
from strategies import *
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


bot = AfkTrader(
    base_url="https://paper-api.alpaca.markets",  # paper API
    socket="wss://stream.data.alpaca.markets/v1beta1/crypto",  # crypto endpoint
    api_key=get_secret_api_token(token_name="API_KEY_ID"),
    api_secret=get_secret_api_token(token_name="API_SECRET"),
    symbol="BTCUSD",
)


if __name__ == "__main__":

    ws = websocket.WebSocketApp(
        bot.socket,
        on_open=bot.on_open,
        on_close=bot.on_close,
        on_message=bot.on_message,
    )
    ws.run_forever()
