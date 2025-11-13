#!/usr/bin/env python3
"""
Demo Script for Optimal Execution System
Shows the full capabilities of the institutional trading system
"""

from main import AdvancedOptimalExecution
import time

def run_demo():
    print("🎯 OPTIMAL EXECUTION SYSTEM DEMO")
    print("=" * 50)
    
    # Initialize system
    system = AdvancedOptimalExecution()
    
    print("1. 🤖 Testing ML-Enhanced Execution...")
    results = system.ml_enhanced_execution(1000000, 0.7)
    print(f"   ✅ Cost: ${results['total_cost']:,.2f}")
    
    print("2. 📊 Testing Portfolio Optimization...")
    portfolio = [
        {'symbol': 'AAPL', 'size': 500000, 'risk': 0.02},
        {'symbol': 'GOOGL', 'size': 300000, 'risk': 0.025}
    ]
    portfolio_results = system.portfolio_level_execution(portfolio)
    print(f"   ✅ Portfolio optimized")
    
    print("3. 🔍 Testing Hidden Liquidity Detection...")
    liquidity = system.data_feed.estimate_hidden_liquidity()
    print(f"   ✅ Liquidity signals found: {len(liquidity)}")
    
    print("4. 📈 Launching Web Dashboard...")
    print("   🚀 Run: python dashboard_network.py")
    print("   🌐 Access: http://localhost:5001")
    
    print("\n🎉 DEMO COMPLETE!")
    print("Your institutional trading system is ready! 🏆")

if __name__ == "__main__":
    run_demo()