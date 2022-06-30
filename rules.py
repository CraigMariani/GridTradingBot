'''
Define 
    -number of grid lines
    -grid size (space between lines)
    -stop loss (5x position size)
    -take profits (5x position size)
    -position size 
'''

class Rules:

    def __init__(self, current_price) -> None:
        self.line_count = 5
        self.grid_space = 50
        self.current_price = current_price
    
    def calculate_grid_lines(self):
        line_count = self.line_count
        grid_space = self.grid_space
        price = self.current_price

        stop_loss = price - ((line_count + 1) * grid_space) 
        take_profit = price + ((line_count + 1) * grid_space) 
        buy_lines = []
        sell_lines = []
        for i in range(line_count):
            buy_lines.append(price - ((i * grid_space)))
            sell_lines.append(price + ((i * grid_space)))
        
        print('sl {}'.format(stop_loss))
        print('tp {}'.format(take_profit))
        print('bl {}'.format(buy_lines))
        print('sl {}'.format(sell_lines))
        
        return stop_loss, take_profit, buy_lines, sell_lines


    # we want to only risk no more than 10 percent of our account
    # when the stoploss is triggered we should only lose 10 percent
    # write the code so it does this
    def calculate_position_size(self, account_size):
        line_count = self.line_count
        grid_space = self.grid_space

        risk = account_size * .1
        tick_value = 1 
        ticks_at_risk = (line_count + 1) * grid_space
        position_size = risk / (ticks_at_risk * tick_value)
        position_size = round(position_size, 2) 
        return position_size