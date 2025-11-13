import numpy as np
from scipy.optimize import minimize

class PortfolioExecution:
    def __init__(self):
        self.correlation_matrix = None
        
    def optimize_portfolio_execution(self, orders, correlation_matrix=None):
        """
        Optimize execution across multiple stocks considering correlations
        """
        n_stocks = len(orders)
        
        if correlation_matrix is None:
            # Assume moderate correlation if not provided
            correlation_matrix = np.eye(n_stocks) * 0.3
            np.fill_diagonal(correlation_matrix, 1.0)
        
        def objective(execution_times):
            """Minimize total portfolio impact considering correlations"""
            total_risk = 0
            for i in range(n_stocks):
                for j in range(n_stocks):
                    risk_contribution = (orders[i]['risk'] * orders[j]['risk'] * 
                                       correlation_matrix[i,j] * 
                                       min(execution_times[i], execution_times[j]))
                    total_risk += risk_contribution
            return total_risk
        
        # Constraints: execution times between 1 and 390 minutes
        bounds = [(1, 390) for _ in range(n_stocks)]
        
        # Initial guess: proportional to order size
        x0 = [min(390, max(1, order['size'] / 10000)) for order in orders]
        
        result = minimize(objective, x0, bounds=bounds, method='L-BFGS-B')
        
        return {
            'optimal_times': result.x,
            'total_risk': result.fun,
            'success': result.success
        }