import numpy as np
from scipy import stats

class RiskModels:
    """
    Risk management for optimal execution
    """
    
    def __init__(self, config=None):
        self.config = config or ExecutionConfig()
        
    def value_at_risk(self, position, volatility, confidence=0.95):
        """
        Calculate Value at Risk for a position
        """
        return position * volatility * stats.norm.ppf(confidence)
    
    def execution_risk(self, remaining_shares, volatility, time_remaining):
        """
        Calculate execution risk (variance of implementation shortfall)
        """
        if time_remaining <= 0:
            return 0
        return remaining_shares**2 * volatility**2 * time_remaining
    
    def liquidity_adjusted_var(self, position, volatility, average_volume, 
                              liquidation_time):
        """
        Liquidity-adjusted VaR considering market impact
        """
        base_var = self.value_at_risk(position, volatility)
        
        # Estimate market impact cost
        impact_cost = position * 0.01 * (position / average_volume)
        
        return base_var + impact_cost
    
    def stress_test_scenarios(self, execution_plan, market_scenarios):
        """
        Test execution plan under various market scenarios
        """
        results = {}
        
        for scenario_name, conditions in market_scenarios.items():
            volatility = conditions.get('volatility', 0.02)
            volume_change = conditions.get('volume_change', 1.0)
            
            # Calculate costs under stressed conditions
            stressed_volume = conditions.get('average_volume', 1000000) * volume_change
            stressed_volatility = volatility * conditions.get('volatility_scale', 1.0)
            
            # Simplified stress test calculation
            market_impact = np.sum(execution_plan) * stressed_volatility * 0.02
            timing_risk = self.execution_risk(np.sum(execution_plan), 
                                            stressed_volatility, 1.0)
            
            results[scenario_name] = {
                'market_impact_cost': market_impact,
                'timing_risk': timing_risk,
                'total_cost': market_impact + 0.1 * timing_risk
            }
        
        return results