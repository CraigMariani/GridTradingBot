import alpaca_trade_api as tradeapi
from stream_data import Stream_Data as stream
from secret import Secret
from rules import Rules


'''
Algorithm
Inital Set Up
    -Buy at the current price
    -Set the grid lines (5 above, 5 below)
    -Set stop loss (exit all positions at a loss, this will be below the 5th lowest level)
    -Set take profit (exit all position at a profit, this will be above the 5th highest level) 

Running 
    -price hits the grid lines above it will sell one fifth of the current position
    -price hits the grid lines below it will buy one fifth of the current position
    -hit stop loss we exit all positions at a loss
    -hit take profit we exit all positions at a profit
    -After tp/sl is hit we go back to initial set up


Example Output:
{'S': 'BTCUSD',
 'T': 'b',
 'c': 29466.03,
 'h': 29474.04,
 'l': 29464.84,
 'n': 149,
 'o': 29472.95,
 't': '2022-05-22T01:59:00Z',
 'v': 2.15212065,
 'vw': 29468.8181816825,
 'x': 'CBSE'}
'''



class Bot:

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
        available_funds = int(account.buying_power)
        print(available_funds)
        # position size is the total amount of our account that we are risking
        position_size = r.calculate_position_size(account_size=available_funds)
        print('position_size {}'.format(position_size))

        # the amount of the position we buy or sell off at each line
        partial_position = position_size / 5

        # inital buy order
        print('First Purchase of {} at {}'.format(position_size, first_close))
        api.submit_order(
            symbol='ETHUSD',
            side='buy',
            type='market',
            qty=position_size,
        )

        # set up grid lines
        stop_loss, take_profit, buy_lines, sell_lines = r.calculate_grid_lines()

        for bar in bars:
            close = bar['c']

            if close in buy_lines:
                api.submit_order(
                    symbol='ETHUSD',
                    side='buy',
                    type='market',
                    qty=partial_position,
                )

            if close in sell_lines:
                api.submit_order(
                    symbol='ETHUSD',
                    side='sell',
                    type='market',
                    qty=partial_position,
                )

            if take_profit == close:
                print('exit all positions at profit')
                api.close_all_positions()
                b.current_profit_loss()
                b.start_bot()

            if stop_loss == close:
                print('exit all positions at a loss')
                api.close_all_positions()
                b.current_profit_loss()
                b.start_bot()


if __name__ == '__main__':
    b= Bot()
    b.start_bot()