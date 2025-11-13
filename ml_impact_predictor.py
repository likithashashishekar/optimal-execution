from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

class MLImpactPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.is_trained = False
        
    def generate_training_data(self, n_samples=10000):
        """Generate synthetic training data for market impact"""
        np.random.seed(42)
        
        data = {
            'order_size': np.random.exponential(100000, n_samples),
            'urgency': np.random.uniform(0, 1, n_samples),
            'volatility': np.random.uniform(0.01, 0.1, n_samples),
            'market_cap': np.random.lognormal(20, 1, n_samples),
            'volume_ratio': np.random.uniform(0.001, 0.5, n_samples),
            'spread': np.random.uniform(0.01, 0.1, n_samples)
        }
        
        # Simulate market impact (target variable)
        data['impact_cost'] = (
            data['order_size'] * 0.0001 +
            data['urgency'] * data['order_size'] * 0.0002 +
            data['volatility'] * data['order_size'] * 0.001 +
            np.random.normal(0, 100, n_samples)
        )
        
        return pd.DataFrame(data)
    
    def train_model(self):
        """Train the ML model"""
        print("Training ML impact prediction model...")
        data = self.generate_training_data()
        
        X = data.drop('impact_cost', axis=1)
        y = data['impact_cost']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        self.model.fit(X_train, y_train)
        
        score = self.model.score(X_test, y_test)
        print(f"Model trained with R² score: {score:.3f}")
        self.is_trained = True
        
    def predict_impact(self, order_features):
        """Predict market impact for new order"""
        if not self.is_trained:
            self.train_model()
            
        prediction = self.model.predict([order_features])[0]
        return max(0, prediction)  # Ensure non-negative