# region imports
from AlgorithmImports import *
# endregion


# This algorithm trades SPY using a medium-speed trend-following strategy.
# It uses 15-minute bars and compares a fast SMA against a slow SMA.
class MediumSpeedSpyTrend(QCAlgorithm):

    def initialize(self):
        # Set the backtest start and end dates
        self.set_start_date(2023, 1, 1)
        self.set_end_date(2026, 1, 1)

        # Set the starting account balance
        self.set_cash(100000)

        # Add SPY equity data at minute resolution
        self.spy = self.add_equity("SPY", Resolution.MINUTE).symbol

        # Create a 15-minute consolidator.
        # This converts minute data into 15-minute trade bars.
        consolidator = TradeBarConsolidator(timedelta(minutes=15))

        # Every time a 15-minute bar is completed,
        # call the on_fifteen_minute_bar function.
        consolidator.data_consolidated += self.on_fifteen_minute_bar

        # Attach the consolidator to SPY's data subscription
        self.subscription_manager.add_consolidator(self.spy, consolidator)

        # Create two Simple Moving Average indicators:
        # fast SMA reacts quicker to price changes
        # slow SMA reacts slower and represents the broader trend
        self.fast = SimpleMovingAverage(9)
        self.slow = SimpleMovingAverage(21)

        # Register both indicators to update using the 15-minute bars
        self.register_indicator(self.spy, self.fast, consolidator)
        self.register_indicator(self.spy, self.slow, consolidator)

        # Warm up the algorithm so the moving averages have enough data
        self.set_warm_up(timedelta(days=10))

        # Store the previous SMA values so we can detect crossovers
        self.prev_fast = None
        self.prev_slow = None

        # Risk and trade management settings
        self.max_allocation = 0.95       # Use up to 95% of portfolio value
        self.stop_loss_pct = 0.01        # Exit if trade loses 1%
        self.take_profit_pct = 0.02      # Exit if trade gains 2%

        # Track the trade entry price for stop-loss and take-profit checks
        self.entry_price = None

        # Track the most recent trade time to prevent overtrading
        self.last_trade_time = None

        # Wait 60 minutes after a trade before entering another one
        self.cooldown_minutes = 60

        # Count how many trades the strategy has entered
        self.trade_count = 0

    def on_data(self, data: Slice):
        # This function runs every time new minute data arrives.
        # It is left empty because this strategy only trades on 15-minute bars.
        pass

    def on_fifteen_minute_bar(self, sender, bar):
        # Do not trade while the algorithm is warming up
        if self.is_warming_up:
            return

        # Do not trade until both moving averages have enough data
        if not self.fast.is_ready or not self.slow.is_ready:
            return

        # Only trade when the SPY market is open
        if not self.securities[self.spy].exchange.hours.is_open(self.time, False):
            return

        # Get the current moving average values and current closing price
        fast = self.fast.current.value
        slow = self.slow.current.value
        price = bar.close

        # If currently invested, check risk management exits first
        if self.portfolio[self.spy].invested and self.entry_price is not None:
            # Calculate current profit or loss percentage
            pnl_pct = (price - self.entry_price) / self.entry_price

            # Stop-loss rule:
            # If the trade loses 1% or more, exit the position
            if pnl_pct <= -self.stop_loss_pct:
                self.liquidate(self.spy)
                self.entry_price = None
                self.last_trade_time = self.time

                # Update previous SMA values before exiting the function
                self.prev_fast = fast
                self.prev_slow = slow
                return

            # Take-profit rule:
            # If the trade gains 2% or more, exit the position
            if pnl_pct >= self.take_profit_pct:
                self.liquidate(self.spy)
                self.entry_price = None
                self.last_trade_time = self.time

                # Update previous SMA values before exiting the function
                self.prev_fast = fast
                self.prev_slow = slow
                return

        # Cooldown rule:
        # Prevent the strategy from entering another trade too soon
        if self.last_trade_time is not None:
            mins_since = (self.time - self.last_trade_time).total_seconds() / 60

            # If less than 60 minutes have passed since the last trade,
            # do not allow a new trade
            if mins_since < self.cooldown_minutes:
                self.prev_fast = fast
                self.prev_slow = slow
                return

        # Only check for crossovers if previous SMA values exist
        if self.prev_fast is not None and self.prev_slow is not None:

            # Bullish crossover:
            # Fast SMA was below or equal to slow SMA, then crosses above it.
            # This signals upward momentum, so the algorithm buys SPY.
            if self.prev_fast <= self.prev_slow and fast > slow:
                if not self.portfolio[self.spy].invested:
                    self.trade_count += 1
                    self.set_holdings(self.spy, self.max_allocation)
                    self.entry_price = price
                    self.last_trade_time = self.time

            # Bearish crossover:
            # Fast SMA was above or equal to slow SMA, then crosses below it.
            # This signals weakening momentum, so the algorithm exits SPY.
            elif self.prev_fast >= self.prev_slow and fast < slow:
                if self.portfolio[self.spy].invested:
                    self.liquidate(self.spy)
                    self.entry_price = None
                    self.last_trade_time = self.time

        # Save the current SMA values so they can be compared
        # against the next 15-minute bar
        self.prev_fast = fast
        self.prev_slow = slow