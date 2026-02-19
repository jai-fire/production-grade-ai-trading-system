"""LSTM Neural Network Model for price prediction"""

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from loguru import logger
from typing import Tuple


class LSTMModel:
    """LSTM model for price prediction"""
    
    def __init__(self, lookback_window: int = 100, units: list = None, dropout: float = 0.2):
        """Initialize LSTM model parameters"""
        self.lookback_window = lookback_window
        self.units = units or [128, 64, 32]
        self.dropout = dropout
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.model = None
        logger.info(f"LSTM model initialized with lookback={lookback_window}")
    
    def build_model(self, input_shape: Tuple[int, int]) -> keras.Model:
        """Build LSTM model architecture"""
        model = Sequential()
        
        for i, unit in enumerate(self.units):
            if i == 0:
                model.add(LSTM(unit, activation='relu', input_shape=input_shape, return_sequences=True))
            else:
                model.add(LSTM(unit, activation='relu', return_sequences=(i < len(self.units) - 1)))
            model.add(Dropout(self.dropout))
        
        model.add(Dense(25, activation='relu'))
        model.add(Dense(1))
        
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        logger.info("LSTM model built successfully")
        
        self.model = model
        return model
    
    def prepare_data(self, prices: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare data for LSTM training"""
        # Normalize data
        scaled_data = self.scaler.fit_transform(prices.reshape(-1, 1))
        
        X, y = [], []
        for i in range(len(scaled_data) - self.lookback_window):
            X.append(scaled_data[i:i+self.lookback_window])
            y.append(scaled_data[i+self.lookback_window])
        
        X = np.array(X)
        y = np.array(y)
        
        logger.info(f"Data prepared: X shape={X.shape}, y shape={y.shape}")
        return X, y
    
    def train(self, prices: np.ndarray, epochs: int = 50, batch_size: int = 32, validation_split: float = 0.2):
        """Train the LSTM model"""
        X, y = self.prepare_data(prices)
        
        if self.model is None:
            self.build_model((X.shape[1], X.shape[2]))
        
        history = self.model.fit(
            X, y,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            verbose=1
        )
        
        logger.info(f"Model training completed. Final loss: {history.history['loss'][-1]:.6f}")
        return history
    
    def predict(self, prices: np.ndarray, steps: int = 1) -> np.ndarray:
        """Predict future prices"""
        if self.model is None:
            raise ValueError("Model not built. Train the model first.")
        
        scaled_data = self.scaler.transform(prices.reshape(-1, 1))
        predictions = []
        
        for _ in range(steps):
            last_lookback = scaled_data[-self.lookback_window:].reshape(1, self.lookback_window, 1)
            pred = self.model.predict(last_lookback, verbose=0)
            predictions.append(pred[0][0])
            scaled_data = np.vstack([scaled_data, pred])
        
        # Inverse transform predictions
        predictions = np.array(predictions).reshape(-1, 1)
        predictions = self.scaler.inverse_transform(predictions)
        
        return predictions.flatten()
    
    def evaluate(self, prices: np.ndarray, test_size: float = 0.2) -> dict:
        """Evaluate model performance"""
        X, y = self.prepare_data(prices)
        split_idx = int(len(X) * (1 - test_size))
        X_test, y_test = X[split_idx:], y[split_idx:]
        
        predictions = self.model.predict(X_test, verbose=0)
        
        mse = mean_squared_error(y_test, predictions)
        mae = mean_absolute_error(y_test, predictions)
        rmse = np.sqrt(mse)
        
        metrics = {
            'mse': mse,
            'mae': mae,
            'rmse': rmse
        }
        
        logger.info(f"Model evaluation - RMSE: {rmse:.6f}, MAE: {mae:.6f}")
        return metrics
    
    def save_model(self, filepath: str):
        """Save model to file"""
        if self.model is None:
            raise ValueError("No model to save")
        self.model.save(filepath)
        logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load model from file"""
        self.model = keras.models.load_model(filepath)
        logger.info(f"Model loaded from {filepath}")
