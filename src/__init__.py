"""Production-Grade AI Trading System Package"""

__version__ = "1.0.0"
__author__ = "jai-fire"
__description__ = "Production-ready AI-powered cryptocurrency trading system"

from . import binance_client, indicators, lstm_model, risk_limits, dashboard, cli

__all__ = [
    "binance_client",
    "indicators",
    "lstm_model",
    "risk_limits",
    "dashboard",
    "cli",
]
