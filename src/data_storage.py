"""Data Storage and Database Management"""
import pandas as pd
from datetime import datetime
from loguru import logger

class DataStorage:
    """Store and retrieve trading data"""
    def __init__(self, db_path: str = 'data/trading.db'):
        self.db_path = db_path
        logger.info(f"Data storage initialized at {db_path}")
    
    def save_ohlcv(self, symbol: str, df: pd.DataFrame):
        """Save OHLCV data"""
        df.to_csv(f'data/{symbol}_ohlcv.csv', index=False)
        logger.info(f"Saved {len(df)} candles for {symbol}")
    
    def load_ohlcv(self, symbol: str) -> pd.DataFrame:
        """Load OHLCV data"""
        try:
            df = pd.read_csv(f'data/{symbol}_ohlcv.csv')
            logger.info(f"Loaded {len(df)} candles for {symbol}")
            return df
        except Exception as e:
            logger.error(f"Failed to load data for {symbol}: {e}")
            return pd.DataFrame()
    
    def save_trades(self, trades: list):
        """Save trade history"""
        df = pd.DataFrame(trades)
        df.to_csv('data/trades.csv', index=False)
        logger.info(f"Saved {len(trades)} trades")
    
    def load_trades(self) -> list:
        """Load trade history"""
        try:
            df = pd.read_csv('data/trades.csv')
            return df.to_dict('records')
        except:
            return []
