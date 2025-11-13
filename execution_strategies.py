import numpy as np
from market_impact import MarketImpactModel
from config import ExecutionConfig

class ExecutionStrategies:
    """
    Various optimal execution strategies
    """
    
    def __init__(self, config=None):
        self.config = config or ExecutionConfig()
        self.impact_model = MarketImpactModel(config)
        
    def volume_weighted_average_price(self, total_shares, time_buckets, historical_volume):
        """
        VWAP strategy: trade in proportion to historical volume patterns
        """
        # Ensure we have enough volume data
        if len(historical_volume) < time_buckets:
            historical_volume = np.pad(historical_volume, (0, time_buckets - len(historical_volume)), 'edge')
        
        volume_weights = historical_volume[:time_buckets] / np.sum(historical_volume[:time_buckets])
        schedule = total_shares * volume_weights
        
        return schedule
    
    def time_weighted_average_price(self, total_shares, time_buckets):
        """
        TWAP strategy: equal trading over time
        """
        return np.full(time_buckets, total_shares / time_buckets)
    
    def implementation_shortfall_simple(self, total_shares, time_horizon, volatility,
                                      average_volume, urgency):
        """
        Simplified implementation shortfall strategy
        """
        risk_aversion = self.config.RISK_AVERSION * urgency
        n_steps = max(1, time_horizon // self.config.MIN_TIME_SLICE)
        
        # Use exponential decay based on urgency
        if urgency > 0.8:
            # Aggressive execution
            decay_rate = 0.8
        elif urgency > 0.5:
            # Moderate execution
            decay_rate = 0.5
        else:
            # Patient execution
            decay_rate = 0.2
            
        schedule = []
        remaining = total_shares
        
        for i in range(n_steps):
            if i == n_steps - 1:
                shares = remaining
            else:
                shares = remaining * decay_rate / n_steps
                shares = min(shares, average_volume * self.config.MAX_POSITION_CHANGE)
            
            schedule.append(shares)
            remaining -= shares
            
        return np.array(schedule)
    
    def adaptive_execution(self, total_shares, market_conditions, urgency):
        """
        Adaptive strategy that responds to market conditions
        """
        volatility = market_conditions.get('volatility', 0.02)
        volume = market_conditions.get('average_volume', total_shares * 10)
        momentum = market_conditions.get('momentum', 0)
        
        # Adjust strategy based on market conditions
        if urgency > 0.8:  # High urgency
            return self.implementation_shortfall_simple(total_shares, 
                                                       self.config.TIME_HORIZON // 2,
                                                       volatility, volume, urgency)
        elif momentum > 0:  # Favorable conditions
            return self.implementation_shortfall_simple(total_shares,
                                                       self.config.TIME_HORIZON,
                                                       volatility, volume, urgency)
        else:  # Normal conditions
            time_buckets = self.config.TIME_HORIZON // self.config.MIN_TIME_SLICE
            historical_vol = np.ones(time_buckets)  # Default pattern
            return self.volume_weighted_average_price(total_shares, 
                                                     time_buckets,
                                                     historical_vol)