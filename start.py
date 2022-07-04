'''
For initial position of trading bot, run this at the start 
'''


from secret import Secret
import alpaca_trade_api as tradeapi
from stream_data import Stream_Data as stream
from rules import Rules

class Start:
    def __init__(self):
        api_key = Secret.paper_api_key
        secret_key = Secret.paper_secret_key
        alp_base_url = 'https://paper-api.alpaca.markets'
        api = tradeapi.REST(api_key, secret_key, alp_base_url, api_version='v2')
        
        self.data_url = 'https://data.alpaca.markets/v1beta1/crypto'
        self.header = { 
                        'APCA-API-KEY-ID' : Secret.paper_api_key,
                        'APCA-API-SECRET-KEY' : Secret.paper_secret_key}

        self.api_key = api_key
        self.secret_key = secret_key
        self.api = api

    def current_profit_loss(self):
        api = self.api
        account = api.get_account()

        # Check our current balance vs. our balance at the last market close
        balance_change = float(account.equity) - float(account.last_equity)
        print(f'Today\'s portfolio balance change: ${balance_change}')

    def start_bot(self):
        api = self.api
        s = stream()
        bars = s.bar_data()

        

        for _ in range(3):
            print(next(bars))

        first_close = next(bars)['c']
        r = Rules(first_close)

        account = api.get_account()
        available_funds = int(round(float(account.buying_power), 2))
        print(available_funds)
        # position size is the total amount of our account that we are risking
        position_size = r.calculate_position_size(account_size=available_funds)
        print('position_size {}'.format(position_size))

        # inital buy order
        print('First Purchase of {} at {}'.format(position_size, first_close))

        api.submit_order(
            symbol='ETHUSD',
            side='buy',
            type='market',
            qty=position_size,
        )


if __name__ == '__main__':
    s = Start()
    s.start_bot()