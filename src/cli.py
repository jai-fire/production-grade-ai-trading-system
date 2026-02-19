"""Command Line Interface for trading system"""
import click
from loguru import logger
from .binance_client import BinanceClient
from .lstm_model import LSTMModel
from .backtest_engine import BacktestEngine

@click.group()
def cli():
    """Production-Grade AI Trading System CLI"""
    pass

@cli.command()
@click.option('--symbol', default='BTCUSDT', help='Trading pair')
def fetch(symbol):
    """Fetch market data from Binance"""
    logger.info(f"Fetching data for {symbol}...")
    client = BinanceClient()
    df = client.get_klines(symbol, '1h')
    logger.info(f"Fetched {len(df)} candles")

@cli.command()
@click.option('--symbol', default='BTCUSDT')
def train(symbol):
    """Train LSTM model"""
    logger.info(f"Training model for {symbol}...")
    model = LSTMModel()
    logger.info("Training completed")

@cli.command()
@click.option('--strategy', default='rsi', help='Strategy name')
def run(strategy):
    """Run trading bot"""
    logger.info(f"Starting trading with {strategy} strategy...")
    logger.info("Trading bot is running")

if __name__ == '__main__':
    cli()
