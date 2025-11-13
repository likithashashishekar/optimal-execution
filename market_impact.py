import numpy as np
from scipy.optimize import minimize
from config import ExecutionConfig

class MarketImpactModel:
    """
    Models permanent and temporary market impact of large orders
    """
    
    def __init__(self, config=None):
        self.config = config or ExecutionConfig()
        
    def permanent_impact(self, volume_fraction, volatility):
        """
        Permanent impact: long-term price movement due to information leakage
        """
        return (self.config.PERMANENT_IMPACT_FACTOR * 
                volume_fraction * volatility)
    
    def temporary_impact(self, trade_size, average_volume, volatility):
        """
        Temporary impact: immediate price movement due to liquidity demand
        """
        volume_ratio = trade_size / average_volume
        return (self.config.TEMPORARY_IMPACT_FACTOR * 
                np.sqrt(volume_ratio) * volatility)
    
    def total_impact_cost(self, execution_schedule, average_volume, volatility):
        """
        Calculate total market impact cost for an execution schedule
        """
        total_cost = 0
        remaining_shares = sum(execution_schedule)
        
        for i, shares in enumerate(execution_schedule):
            volume_frac = shares / average_volume
            time_frac = i / len(execution_schedule)
            
            # Permanent impact accumulates
            perm_impact = self.permanent_impact(volume_frac, volatility)
            
            # Temporary impact for this trade
            temp_impact = self.temporary_impact(shares, average_volume, volatility)
            
            # Impact on remaining shares
            cost = shares * (perm_impact + temp_impact)
            total_cost += cost
            
            remaining_shares -= shares
            
        return total_cost
    
    def almgren_chriss_optimal(self, total_shares, time_horizon, volatility, 
                              average_volume, risk_aversion):
        """
        Implement Almgren-Chriss optimal execution model
        """
        n_steps = max(1, time_horizon // self.config.MIN_TIME_SLICE)
        time_points = np.linspace(0, 1, n_steps)
        
        # Exponential decay schedule
        optimal_schedule = []
        remaining = total_shares
        
        for t in time_points[:-1]:
            shares = total_shares * np.exp(-risk_aversion * t) / n_steps
            shares = min(shares, remaining)
            optimal_schedule.append(shares)
            remaining -= shares
        
        optimal_schedule.append(remaining)
        return np.array(optimal_schedule)