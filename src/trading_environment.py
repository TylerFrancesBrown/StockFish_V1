import pandas as pd

class TradingEnvironment:
    def __init__(self, data, starting_balance=100000):
        self.data = data
        self.starting_balance = starting_balance
        self.balance = starting_balance
        self.position = 0  # Number of shares held
        self.current_step = 0
        self.trading_log = []

    def reset(self):
        self.balance = self.starting_balance
        self.position = 0
        self.current_step = 0
        self.trading_log = []

    def get_current_price(self):
        return self.data.iloc[self.current_step]['c']  # 'c' is close price

    def buy(self, quantity):
        price = self.get_current_price()
        total_cost = price * quantity
        if self.balance >= total_cost:
            self.balance -= total_cost
            self.position += quantity
            self.trading_log.append(('BUY', self.current_step, quantity, price))
        else:
            print("Insufficient balance to buy.")

    def sell(self, quantity):
        if self.position >= quantity:
            price = self.get_current_price()
            total_revenue = price * quantity
            self.balance += total_revenue
            self.position -= quantity
            self.trading_log.append(('SELL', self.current_step, quantity, price))
        else:
            print("Insufficient shares to sell.")

    def step(self):
        self.current_step += 1
        if self.current_step >= len(self.data):
            print("End of data reached.")

    def portfolio_value(self):
        price = self.get_current_price()
        return self.balance + (self.position * price)

    def print_status(self):
        print(f"Step: {self.current_step}, Balance: {self.balance:.2f}, Position: {self.position}, Portfolio Value: {self.portfolio_value():.2f}")

if __name__ == "__main__":
    from data_loader import get_historical_data

    # Load some data
    df = get_historical_data("AAPL", "2024-04-01T09:30:00-04:00", "2024-04-01T16:00:00-04:00")

    env = TradingEnvironment(df)

    # Simulate a tiny strategy
    for _ in range(10):
        env.print_status()
        if env.current_step % 2 == 0:
            env.buy(1)  # Buy 1 share every even step
        else:
            env.sell(1)  # Sell 1 share every odd step
        env.step()

    print("\nFinal Portfolio Value:", env.portfolio_value())
    print("\nTrading Log:", env.trading_log)