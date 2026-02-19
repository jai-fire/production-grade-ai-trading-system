"""Risk Management Module"""

from typing import Dict, List
from loguru import logger


class RiskManager:
    """Manage trading risk parameters"""
    
    def __init__(self, max_daily_loss: float = 0.05, max_position_size: float = 0.1, max_leverage: float = 1.0):
        """Initialize risk manager"""
        self.max_daily_loss = max_daily_loss
        self.max_position_size = max_position_size
        self.max_leverage = max_leverage
        self.current_loss = 0.0
        self.positions = {}
        logger.info("Risk manager initialized")
    
    def calculate_position_size(self, account_balance: float, risk_per_trade: float = 0.02, stop_loss_pct: float = 0.02) -> float:
        """Calculate position size based on risk parameters"""
        risk_amount = account_balance * risk_per_trade
        position_size = risk_amount / stop_loss_pct
        max_position = account_balance * self.max_position_size
        
        position_size = min(position_size, max_position)
        logger.info(f"Calculated position size: {position_size}")
        return position_size
    
    def can_open_position(self, symbol: str, position_size: float, account_balance: float) -> bool:
        """Check if position can be opened"""
        # Check if daily loss limit exceeded
        if self.current_loss >= (account_balance * self.max_daily_loss):
            logger.warning("Daily loss limit exceeded")
            return False
        
        # Check max position size
        if position_size > (account_balance * self.max_position_size):
            logger.warning(f"Position size exceeds limit")
            return False
        
        return True
    
    def add_position(self, symbol: str, entry_price: float, quantity: float, stop_loss: float):
        """Add an open position"""
        self.positions[symbol] = {
            'entry_price': entry_price,
            'quantity': quantity,
            'stop_loss': stop_loss,
            'take_profit': entry_price * 1.05  # 5% take profit
        }
        logger.info(f"Position added: {symbol} x{quantity} @ {entry_price}")
    
    def check_stop_loss(self, symbol: str, current_price: float) -> bool:
        """Check if stop loss is triggered"""
        if symbol not in self.positions:
            return False
        
        if current_price <= self.positions[symbol]['stop_loss']:
            logger.warning(f"Stop loss triggered for {symbol}")
            return True
        return False
    
    def check_take_profit(self, symbol: str, current_price: float) -> bool:
        """Check if take profit is reached"""
        if symbol not in self.positions:
            return False
        
        if current_price >= self.positions[symbol]['take_profit']:
            logger.info(f"Take profit reached for {symbol}")
            return True
        return False
    
    def close_position(self, symbol: str, exit_price: float) -> Dict:
        """Close a position and calculate P&L"""
        if symbol not in self.positions:
            return {}
        
        pos = self.positions[symbol]
        pnl = (exit_price - pos['entry_price']) * pos['quantity']
        pnl_pct = ((exit_price - pos['entry_price']) / pos['entry_price']) * 100
        
        if pnl < 0:
            self.current_loss += abs(pnl)
        
        result = {
            'symbol': symbol,
            'pnl': pnl,
            'pnl_pct': pnl_pct,
            'quantity': pos['quantity']
        }
        
        del self.positions[symbol]
        logger.info(f"Position closed: {symbol} P&L: {pnl}")
        return result
