# region imports
from AlgorithmImports import *
# endregion


# This algorithm is a swing trading strategy for SPY.
# It uses daily data and combines trend filters, RSI pullbacks,
# moving averages, ATR-based stop losses, partial profit taking,
# and trailing stops.
class SPYSwingStrategy(QCAlgorithm):

    def initialize(self):
        # Set the start date for the backtest
        self.set_start_date(2023, 1, 1)

        # Set the starting account balance
        self.set_cash(100000)

        # Add SPY using daily resolution data
        self._spy = self.add_equity("SPY", Resolution.DAILY).symbol

        # Seed initial prices so indicators can initialize more smoothly
        self.settings.seed_initial_prices = True
        
        # -----------------------------
        # Indicators
        # -----------------------------

        # 50-day Simple Moving Average used for medium-term trend direction
        self._sma_50 = self.sma(self._spy, 50, Resolution.DAILY)

        # 200-day Simple Moving Average used for long-term trend direction
        self._sma_200 = self.sma(self._spy, 200, Resolution.DAILY)

        # 14-period RSI used to detect oversold pullback conditions
        self._rsi = self.rsi(self._spy, 14)

        # 20-day EMA used as the recovery trigger after RSI becomes oversold
        self._ema_20 = self.ema(self._spy, 20, Resolution.DAILY)

        # 14-period ATR used to calculate a volatility-based stop loss
        self._atr = self.atr(self._spy, 14)
        
        # -----------------------------
        # Strategy Parameters
        # -----------------------------

        # Use 95% of the portfolio when entering a position
        self._position_size = 0.95

        # RSI level that defines an oversold condition
        self._rsi_oversold = 30

        # Stop loss is placed 2 ATRs below the entry price
        self._atr_stop_multiplier = 2.0

        # Take partial profits once the position gains 5%
        self._partial_profit_pct = 0.05

        # Sell 50% of the position when partial profit target is reached
        self._partial_profit_size = 0.5

        # After partial profit is taken, use a 3% trailing stop
        self._trailing_stop_pct = 0.03

        # Exit the trade after holding for 20 days
        self._max_hold_days = 20

        # Wait 3 days after an exit before entering another trade
        self._cooldown_days = 3
        
        # -----------------------------
        # State Variables
        # -----------------------------

        # Stores the price where the trade was entered
        self._entry_price = None

        # Stores the ATR-based stop loss price
        self._stop_loss_price = None

        # Stores the trailing stop price after partial profit is taken
        self._trailing_stop_price = None

        # Stores the time when the trade was entered
        self._entry_time = None

        # Stores the time of the most recent exit
        self._last_exit_time = None

        # Tracks whether partial profit has already been taken
        self._partial_taken = False

        # Tracks whether RSI previously dropped into oversold territory
        self._rsi_was_oversold = False
        
    def on_data(self, data: Slice):
        # Make sure SPY data exists and the 200-day SMA is ready
        # The 200-day SMA is the slowest indicator, so it confirms enough historical data exists
        if not data.contains_key(self._spy) or not self._sma_200.is_ready:
            return
            
        # Get the current SPY price
        price = self.securities[self._spy].price
        
        # If currently invested, check whether the algorithm should exit
        if self.portfolio[self._spy].invested:
            self._check_exit_conditions(price)

        # If not invested, check whether the algorithm should enter
        else:
            self._check_entry_conditions(price)
    
    def _check_entry_conditions(self, price: float) -> None:
        # -----------------------------
        # Cooldown Check
        # -----------------------------

        # Prevent the strategy from entering another trade too soon after an exit
        if self._last_exit_time and (self.time - self._last_exit_time).days < self._cooldown_days:
            self._rsi_was_oversold = False
            return
            
        # -----------------------------
        # Trend Filter
        # -----------------------------

        # Only enter trades when the 50-day SMA is above the 200-day SMA.
        # This means the stock is in a longer-term uptrend.
        if self._sma_50.current.value <= self._sma_200.current.value:
            self._rsi_was_oversold = False
            return
            
        # -----------------------------
        # RSI Oversold Setup
        # -----------------------------

        # If RSI drops below the oversold threshold,
        # remember that a pullback has occurred.
        if self._rsi.current.value < self._rsi_oversold:
            self._rsi_was_oversold = True
            
        # Do not enter unless RSI was previously oversold
        if not self._rsi_was_oversold:
            return
            
        # -----------------------------
        # Recovery Entry Trigger
        # -----------------------------

        # Enter only after price recovers above the 20-day EMA.
        # This suggests that price may be bouncing after the pullback.
        if price <= self._ema_20.current.value:
            return
            
        # -----------------------------
        # Enter Trade
        # -----------------------------

        # Buy SPY using the defined portfolio allocation
        self.set_holdings(self._spy, self._position_size)

        # Save the entry price and entry time
        self._entry_price = price
        self._entry_time = self.time

        # Set an ATR-based stop loss below the entry price
        self._stop_loss_price = price - (self._atr.current.value * self._atr_stop_multiplier)

        # No trailing stop is active yet
        self._trailing_stop_price = None

        # Partial profit has not been taken yet
        self._partial_taken = False

        # Reset RSI setup flag after entering the trade
        self._rsi_was_oversold = False
        
        # Print entry information to the debug log
        self.debug(f"Entry at {price:.2f}, Stop: {self._stop_loss_price:.2f}, RSI: {self._rsi.current.value:.1f}")
    
    def _check_exit_conditions(self, price: float) -> None:
        # Calculate current profit or loss percentage
        profit_pct = (price - self._entry_price) / self._entry_price
        
        # -----------------------------
        # Max Hold Period Exit
        # -----------------------------

        # Exit the position if it has been held for too many days
        if (self.time - self._entry_time).days >= self._max_hold_days:
            self._exit_position("Max hold period")
            return
            
        # -----------------------------
        # ATR Stop Loss Exit
        # -----------------------------

        # Exit the position if price falls below the ATR-based stop loss
        if price <= self._stop_loss_price:
            self._exit_position("Stop loss")
            return
            
        # -----------------------------
        # Partial Profit Taking
        # -----------------------------

        # If the trade is up at least 5% and partial profit has not been taken,
        # sell half of the current position.
        if not self._partial_taken and profit_pct >= self._partial_profit_pct:
            # Get current SPY share quantity
            quantity = self.portfolio[self._spy].quantity

            # Sell 50% of the position
            self.market_order(self._spy, -int(quantity * self._partial_profit_size))

            # Mark that partial profit has been taken
            self._partial_taken = True

            # Activate trailing stop after partial profit
            self._trailing_stop_price = price * (1 - self._trailing_stop_pct)

            # Print partial profit information to the debug log
            self.debug(f"Partial profit at {price:.2f}, +{profit_pct:.2%}")
            return
            
        # -----------------------------
        # Trailing Stop Exit
        # -----------------------------

        # Only use the trailing stop after partial profit has been taken
        if self._trailing_stop_price:
            # Calculate a new trailing stop based on the current price
            new_trailing = price * (1 - self._trailing_stop_pct)

            # If price moves higher, raise the trailing stop
            if new_trailing > self._trailing_stop_price:
                self._trailing_stop_price = new_trailing
                
            # If price falls below the trailing stop, exit the remaining position
            if price <= self._trailing_stop_price:
                self._exit_position("Trailing stop")
                return
    
    def _exit_position(self, reason: str) -> None:
        # Get the current SPY price
        price = self.securities[self._spy].price

        # Calculate final profit or loss percentage
        profit_pct = (price - self._entry_price) / self._entry_price
        
        # Close the entire SPY position
        self.liquidate(self._spy)

        # Store the exit time for cooldown tracking
        self._last_exit_time = self.time
        
        # Print exit information to the debug log
        self.debug(f"Exit: {reason} at {price:.2f}, P/L: {profit_pct:.2%}")
        
        # -----------------------------
        # Reset Trade State
        # -----------------------------

        # Clear trade-specific values so the algorithm is ready for the next setup
        self._entry_price = None
        self._stop_loss_price = None
        self._trailing_stop_price = None
        self._entry_time = None
        self._partial_taken = False
        self._rsi_was_oversold = False