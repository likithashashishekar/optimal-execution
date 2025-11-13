import numpy as np
import pandas as pd
from typing import Dict, List

class MarketDataFeed:
    """
    Simulated market data feed for testing execution strategies
    """
    
    def __init__(self):
        self.volume_patterns = self._generate_volume_patterns()
        
    def _generate_volume_patterns(self):
        """Generate typical U-shaped volume patterns"""
        times = np.arange(390)  # Trading minutes
        # U-shaped curve: high volume at open and close
        volume = 1000 + 500 * (np.exp(-times/100) + np.exp(-(390-times)/100))
        return volume
    
    def get_historical_volume(self, days=30):
        """Get historical volume data"""
        patterns = []
        for _ in range(days):
            noise = np.random.normal(1, 0.1, 390)
            patterns.append(self.volume_patterns * noise)
        return np.array(patterns)
    
    def estimate_hidden_liquidity(self, recent_trades=None, order_book=None):
        """
        Detect hidden liquidity using order flow analysis
        """
        if recent_trades is None:
            recent_trades = np.random.exponential(1000, 100)
            
        if order_book is None:
            order_book = {
                'bid_volume': np.random.uniform(50000, 200000),
                'ask_volume': np.random.uniform(50000, 200000)
            }
            
        hidden_probabilities = {}
        
        # Analyze order book imbalances
        bid_volume = order_book.get('bid_volume', 0)
        ask_volume = order_book.get('ask_volume', 0)
        
        if bid_volume > 2 * ask_volume:
            hidden_probabilities['hidden_buy_pressure'] = min(0.8, bid_volume / (bid_volume + ask_volume))
        elif ask_volume > 2 * bid_volume:
            hidden_probabilities['hidden_sell_pressure'] = min(0.8, ask_volume / (bid_volume + ask_volume))
        
        # Analyze trade size distribution
        large_trades = [t for t in recent_trades if t > np.percentile(recent_trades, 90)]
        if large_trades:
            hidden_probabilities['iceberg_indication'] = len(large_trades) / len(recent_trades)
        
        return hidden_probabilities
    
    def get_market_conditions(self):
        """Get current market conditions"""
        return {
            'volatility': np.random.uniform(0.01, 0.05),
            'average_volume': 1000000,
            'momentum': np.random.uniform(-0.02, 0.02),
            'spread': np.random.uniform(0.01, 0.05)
        }