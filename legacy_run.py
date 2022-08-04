'''
For cron job this will be used every time we are entering trades


crontab -e
select 1 (nano) 
0 */1 * * * (run every hour)

'''
import alpaca_trade_api as tradeapi
from stream_data import Stream_Data as stream
from secret import Secret
from rules import Rules
from subprocess import call
import pytz
from datetime import datetime
from datetime import timezone
from datetime import timedelta

class Run:
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

    def main(self):
        s = stream()

        api = self.api
        bars = s.bar_data()
        for _ in range(3):
            print(next(bars))
        
        first_close = next(bars)['c']
        r = Rules(first_close)
        stop_loss, take_profit, buy_lines, sell_lines = r.calculate_grid_lines()
        account = api.get_account()
        available_funds = int(round(float(account.buying_power), 2))
        print(available_funds)
        # position size is the total amount of our account that we are risking
        position_size = r.calculate_position_size(account_size=available_funds)
        print('position_size {}'.format(position_size))

        # the amount of the position we buy or sell off at each line
        partial_position = position_size / 5

        # get the current time in PST
        PST_tz = timezone(timedelta(hours=-8))

        for bar in bars:
            close = bar['c']
            print('close: {}'.format(close))
            print('bar: {}'.format(bar))
            print('buy_lines {}'.format(buy_lines))
            print('sell_lines {}'.format(sell_lines))


            # problem: I suspect price is moving and the grid lines are not detecting the price change
            # solution: confirm theory by checking trade log after running script 
            # we might need to see where the buy and sell lines are in relation to closing price
            # right now the lines are more focused if the price hits it, price may never be the exact same 
            # as those lines, use a greater/less than or equal to in order to catch these movements  
            if close in buy_lines:
                print('Long ETHUSD {} : {}'.format(partial_position, datetime.now(PST_tz)))
                api.submit_order(
                    symbol='ETHUSD',
                    side='buy',
                    type='market',
                    qty=partial_position,
                )

            if close in sell_lines:
                print('Short ETHUSD {} : {}'.format(partial_position, datetime.now(PST_tz)))
                api.submit_order(
                    symbol='ETHUSD',
                    side='sell',
                    type='market',
                    qty=partial_position,
                )

            if take_profit == close:
                print('exit all positions at profit')
                api.close_all_positions()
                ru.current_profit_loss()
                call(["python3", "start.py"])

            if stop_loss == close:
                print('exit all positions at a loss')
                api.close_all_positions()
                ru.current_profit_loss()
                call(["python3", "start.py"])
            print('No Purchase {}'.format(datetime.now(PST_tz)))
                


if __name__ == '__main__':
    ru = Run()
    ru.main()
