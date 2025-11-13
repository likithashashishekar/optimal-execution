import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from database import ExecutionDatabase

class PerformanceAnalytics:
    """
    Advanced analytics and reporting for execution performance
    """
    
    def __init__(self):
        self.db = ExecutionDatabase()
    
    def generate_performance_report(self, days=30):
        """Generate comprehensive performance report"""
        analytics_df = self.db.get_performance_analytics(days)
        
        print("📊 EXECUTION PERFORMANCE REPORT")
        print("=" * 50)
        
        if analytics_df.empty:
            print("No execution data found. Run some executions first.")
            return analytics_df
        
        for _, row in analytics_df.iterrows():
            print(f"\n{row['strategy'].upper()} Strategy:")
            print(f"  Trades: {row['trade_count']}")
            print(f"  Avg Cost: ${row['avg_cost']:,.2f}")
            print(f"  Avg Cost/Share: ${row['avg_cost_per_share']:.4f}")
            print(f"  Avg Completion: {row['avg_completion_time']:.0f} min")
        
        # Best performing strategy
        best_strategy = analytics_df.loc[analytics_df['avg_cost_per_share'].idxmin()]
        print(f"\n🎯 BEST PERFORMING STRATEGY: {best_strategy['strategy'].upper()}")
        print(f"   Cost/Share: ${best_strategy['avg_cost_per_share']:.4f}")
        
        return analytics_df
    
    def plot_performance_trends(self, days=30):
        """Plot performance trends over time"""
        conn = self.db.db_path
        query = '''
            SELECT 
                date(timestamp) as trade_date,
                strategy,
                AVG(cost_per_share) as daily_avg_cost
            FROM executions
            WHERE timestamp >= datetime('now', '-? days')
            GROUP BY date(timestamp), strategy
            ORDER BY trade_date
        '''
        
        try:
            df = pd.read_sql_query(query, conn, params=(days,))
        except:
            print("No data available for plotting. Run some executions first.")
            return
        
        if df.empty:
            print("No data available for plotting.")
            return
        
        plt.figure(figsize=(12, 8))
        
        for strategy in df['strategy'].unique():
            strategy_data = df[df['strategy'] == strategy]
            plt.plot(strategy_data['trade_date'], strategy_data['daily_avg_cost'], 
                    label=strategy, marker='o', linewidth=2)
        
        plt.title('Execution Cost Trends', fontsize=14, fontweight='bold')
        plt.xlabel('Date')
        plt.ylabel('Cost per Share ($)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('performance_trends.png', dpi=300, bbox_inches='tight')
        plt.show()

def main():
    """Standalone analytics main function"""
    print("📊 EXECUTION ANALYTICS DASHBOARD")
    print("=" * 40)
    
    analytics = PerformanceAnalytics()
    
    # Generate report
    print("\n1. Generating performance report...")
    analytics.generate_performance_report(7)
    
    # Plot trends
    print("\n2. Plotting performance trends...")
    analytics.plot_performance_trends(7)
    
    print("\n✅ Analytics complete!")

if __name__ == "__main__":
    main()