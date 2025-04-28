import pandas as pd

class SimpleMovingAverageStrategy:
    def __init__(self, env, short_window=5, long_window=20):
        self.env = env
        self.short_window = short_window
        self.long_window = long_window
        self.data = env.data.copy()
        self.signals = pd.Series('HOLD', index=self.data.index)

    def generate_signals(self):
        self.data['short_ma'] = self.data['c'].rolling(window=self.short_window, min_periods=1).mean()
        self.data['long_ma'] = self.data['c'].rolling(window=self.long_window, min_periods=1).mean()

        # Where short MA crosses above long MA -> BUY
        buy_signals = self.data['short_ma'] > self.data['long_ma']
        sell_signals = self.data['short_ma'] < self.data['long_ma']

        self.signals[buy_signals] = 'BUY'
        self.signals[sell_signals] = 'SELL'

    def run(self):
        self.generate_signals()

        for action in self.signals.iloc[self.long_window:].values:
            if action == 'BUY':
                self.env.buy(1)
            elif action == 'SELL':
                self.env.sell(1)
            self.env.step()

        print("\nFinal Portfolio Value:", self.env.portfolio_value())
        print("\nTrading Log:", self.env.trading_log)

if __name__ == "__main__":
    from trading_environment import TradingEnvironment
    from data_loader import get_historical_data

    df = get_historical_data("AAPL", "2024-04-01T09:30:00-04:00", "2024-04-01T16:00:00-04:00")
    env = TradingEnvironment(df)

    strategy = SimpleMovingAverageStrategy(env)
    strategy.run()

import matplotlib.pyplot as plt

def plot_strategy(data, signals):
    plt.figure(figsize=(15, 8))
    plt.plot(data['c'], label='Close Price', color='black', alpha=0.6)
    plt.plot(data['short_ma'], label=f'Short MA ({strategy.short_window})', color='blue', linestyle='--')
    plt.plot(data['long_ma'], label=f'Long MA ({strategy.long_window})', color='red', linestyle='--')

    # Mark buy signals
    buy_signals = data[signals == 'BUY']
    plt.scatter(buy_signals.index, buy_signals['c'], marker='^', color='green', label='Buy Signal', s=100)

    # Mark sell signals
    sell_signals = data[signals == 'SELL']
    plt.scatter(sell_signals.index, sell_signals['c'], marker='v', color='red', label='Sell Signal', s=100)

    plt.title("Simple Moving Average Strategy")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.show()

# After running the strategy
plot_strategy(strategy.data, strategy.signals)