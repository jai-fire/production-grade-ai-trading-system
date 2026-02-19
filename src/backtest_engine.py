"""Backtesting Engine for strategy validation"""
import pandas as pd
from loguru import logger

class BacktestEngine:
    """Backtest trading strategies"""
    def __init__(self, initial_capital: float = 10000):
        self.initial_capital = initial_capital
        self.trades = []
        logger.info(f"Backtest engine initialized with {initial_capital}")
    
    def run_backtest(self, df: pd.DataFrame, strategy_func) -> dict:
        """Run backtest on OHLCV data"""
        balance = self.initial_capital
        position = None
        trades = []
        
        for idx, row in df.iterrows():
            signal = strategy_func(df.iloc[:idx+1])
            if signal == 'BUY' and not position:
                position = {'entry': row['close'], 'size': balance/row['close']}
            elif signal == 'SELL' and position:
                pnl = (row['close'] - position['entry']) * position['size']
                balance += pnl
                trades.append(pnl)
                position = None
        
        total_return = ((balance - self.initial_capital) / self.initial_capital) * 100
        logger.info(f"Backtest completed. Return: {total_return}%")
        
        return {
            'final_balance': balance,
            'total_return': total_return,
            'trades': len(trades),
            'win_rate': len([t for t in trades if t > 0]) / len(trades) if trades else 0
        }
