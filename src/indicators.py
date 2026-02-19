"""Technical Indicators for trading analysis"""

import numpy as np
import pandas as pd
from typing import Tuple


class TechnicalIndicators:
    """Calculate technical indicators for trading signals"""
    
    @staticmethod
    def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index (RSI)"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    @staticmethod
    def calculate_macd(prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Calculate MACD (Moving Average Convergence Divergence)"""
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal).mean()
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram
    
    @staticmethod
    def calculate_bollinger_bands(prices: pd.Series, period: int = 20, std_dev: float = 2.0) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Calculate Bollinger Bands"""
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        return upper_band, sma, lower_band
    
    @staticmethod
    def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Average True Range (ATR)"""
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        return atr
    
    @staticmethod
    def calculate_moving_averages(prices: pd.Series, periods: list) -> dict:
        """Calculate multiple moving averages"""
        mas = {}
        for period in periods:
            mas[f'MA{period}'] = prices.rolling(window=period).mean()
        return mas
    
    @staticmethod
    def calculate_stochastic(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14, smooth: int = 3) -> Tuple[pd.Series, pd.Series]:
        """Calculate Stochastic Oscillator"""
        lowest_low = low.rolling(window=period).min()
        highest_high = high.rolling(window=period).max()
        
        k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        d_percent = k_percent.rolling(window=smooth).mean()
        
        return k_percent, d_percent
    
    @staticmethod
    def calculate_volume_profile(prices: pd.Series, volume: pd.Series, bins: int = 20) -> pd.DataFrame:
        """Calculate volume profile"""
        price_bins = pd.cut(prices, bins=bins)
        volume_profile = volume.groupby(price_bins).sum()
        return volume_profile
    
    @staticmethod
    def identify_support_resistance(prices: pd.Series, window: int = 5) -> Tuple[list, list]:
        """Identify support and resistance levels"""
        support = []
        resistance = []
        
        for i in range(window, len(prices) - window):
            if prices.iloc[i] == prices.iloc[i-window:i+window].min():
                support.append((i, prices.iloc[i]))
            if prices.iloc[i] == prices.iloc[i-window:i+window].max():
                resistance.append((i, prices.iloc[i]))
        
        return support, resistance
