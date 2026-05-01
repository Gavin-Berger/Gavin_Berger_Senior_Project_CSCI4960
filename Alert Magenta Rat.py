# region imports
from AlgorithmImports import *
# endregion

class AlertMagentaRat(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2022, 1, 1)
        self.set_cash(100000)
        
        # Add SPY with minute resolution for fast execution
        self._symbol = self.add_equity("SPY", Resolution.MINUTE).symbol
        
        # Optimization parameters
        fast_period = selfAget_parameter("fast_period", 20)
        slow_period = self.get_parameter("slow_period", 50)
        trend_period = self.get_parameter("trend_period", 200)
        stop_loss_pct = self.get_parameter("stop_loss_pct", 0.05)
        
        # Use EMA instead of SMA for faster response to price changes
        self._fast_ma = self.ema(self._symbol, fast_period, Resolution.DAILY)
        self._slow_ma = self.ema(self._symbol, slow_period, Resolution.DAILY)
        # Add long-term trend filter to avoid choppy markets
        self._trend_ma = self.ema(self._symbol, trend_period, Resolution.DAILY)
        
        # ATR for volatility-based position sizing
        self._atr = self.atr(self._symbol, 14, resolution=Resolution.DAILY)
        
        # Risk management
        self._stop_loss_pct = stop_loss_pct
        self._entry_price = 0
        self._last_fast_value = 0
        self._last_slow_value = 0
        
        # Schedule daily check for crossover signals near market close
        # This ensures daily bars are updated
        self.schedule.on(self.date_rules.every_day(self._symbol),
                        self.time_rules.before_market_close(self._symbol, 10),
                        self._check_signals)
        
        # Warm up the indicators
        self.set_warm_up(trend_period, Resolution.DAILY)

    def on_data(self, data: Slice):
        """Monitor stop loss intraday for fast exits"""
        if not data.bars.contains_key(self._symbol):
            return
        
        holdings = self.portfolio[self._symbol]
        if holdings.invested and self._entry_price > 0:
            price = data.bars[self._symbol].close
            # Intraday stop loss check for fast exits
            if price < self._entry_price * (1 - self._stop_loss_pct):
                self.liquidate(self._symbol)
                self.debug(f"Intraday Stop Loss: Entry {self._entry_price:.2f}, Current {price:.2f}")
                self._entry_price = 0

    def _check_signals(self):
        """Check for moving average crossover signals daily with trend filter"""
        if not self._fast_ma.is_ready or not self._slow_ma.is_ready or not self._trend_ma.is_ready:
            return
        
        holdings = self.portfolio[self._symbol]
        price = self.securities[self._symbol].price
        
        fast_value = self._fast_ma.current.value
        slow_value = self._slow_ma.current.value
        trend_value = self._trend_ma.current.value
        
        # Detect actual crossovers (not just relative positions)
        bullish_crossover = (fast_value > slow_value and 
                            self._last_fast_value <= self._last_slow_value and 
                            self._last_fast_value > 0)
        
        bearish_crossover = (fast_value < slow_value and 
                            self._last_fast_value >= self._last_slow_value and 
                            self._last_fast_value > 0)
        
        # Only trade when price is above long-term trend (bullish environment)
        in_uptrend = price > trend_value
        
        # Golden cross: Fast MA crosses above Slow MA AND in uptrend
        if bullish_crossover and not holdings.is_long and in_uptrend:
            # Volatility-based position sizing
            atr_value = self._atr.current.value
            volatility_ratio = atr_value / price
            position_size = max(0.5, min(1.0, 1.0 - (volatility_ratio * 20)))
            
            self.set_holdings(self._symbol, position_size)
            self._entry_price = price
            self.debug(f"Golden Cross: Fast {fast_value:.2f} > Slow {slow_value:.2f}, Size: {position_size:.1%}")
        
        # Death cross: Fast MA crosses below Slow MA
        elif bearish_crossover and holdings.invested:
            self.liquidate(self._symbol)
            self.debug(f"Death Cross: Fast {fast_value:.2f} < Slow {slow_value:.2f}")
            self._entry_price = 0
        
        # Store current values for next crossover detection
        self._last_fast_value = fast_value
        self._last_slow_value = slow_value
