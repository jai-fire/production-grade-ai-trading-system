"""Binance API Client for real-time data and trading"""

import os
import time
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import pandas as pd
from binance.client import Client
from binance.exceptions import BinanceAPIException
from loguru import logger


class BinanceClient:
    """Wrapper around Binance API client"""
    
    def __init__(self, api_key: str = None, api_secret: str = None, testnet: bool = False):
        """Initialize Binance client with API credentials"""
        self.api_key = api_key or os.getenv('BINANCE_API_KEY')
        self.api_secret = api_secret or os.getenv('BINANCE_API_SECRET')
        self.testnet = testnet
        
        try:
            self.client = Client(self.api_key, self.api_secret)
            if testnet:
                self.client.API_URL = 'https://testnet.binance.vision/api'
            logger.info("Binance client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Binance client: {e}")
            raise
    
    def get_klines(self, symbol: str, interval: str, limit: int = 500) -> pd.DataFrame:
        """Get OHLCV data for a trading pair"""
        try:
            klines = self.client.get_klines(
                symbol=symbol,
                interval=interval,
                limit=limit
            )
            df = pd.DataFrame(klines, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_trades',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
            ])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
            
            numeric_cols = ['open', 'high', 'low', 'close', 'volume']
            df[numeric_cols] = df[numeric_cols].astype(float)
            
            return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
        except BinanceAPIException as e:
            logger.error(f"Binance API error getting klines: {e}")
            raise
    
    def get_ticker(self, symbol: str) -> Dict:
        """Get current ticker information"""
        try:
            ticker = self.client.get_symbol_info(symbol)
            return ticker
        except BinanceAPIException as e:
            logger.error(f"Failed to get ticker for {symbol}: {e}")
            raise
    
    def get_account_balance(self) -> Dict[str, float]:
        """Get account balances"""
        try:
            account = self.client.get_account()
            balances = {}
            for asset in account['balances']:
                if float(asset['free']) > 0 or float(asset['locked']) > 0:
                    balances[asset['asset']] = {
                        'free': float(asset['free']),
                        'locked': float(asset['locked']),
                        'total': float(asset['free']) + float(asset['locked'])
                    }
            return balances
        except BinanceAPIException as e:
            logger.error(f"Failed to get account balance: {e}")
            raise
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> Dict:
        """Place a limit order"""
        try:
            order = self.client.order_limit(
                symbol=symbol,
                side=side.upper(),
                quantity=quantity,
                price=price
            )
            logger.info(f"Order placed: {side} {quantity} {symbol} at {price}")
            return order
        except BinanceAPIException as e:
            logger.error(f"Failed to place order: {e}")
            raise
    
    def place_market_order(self, symbol: str, side: str, quantity: float) -> Dict:
        """Place a market order"""
        try:
            order = self.client.order_market(
                symbol=symbol,
                side=side.upper(),
                quantity=quantity
            )
            logger.info(f"Market order placed: {side} {quantity} {symbol}")
            return order
        except BinanceAPIException as e:
            logger.error(f"Failed to place market order: {e}")
            raise
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict:
        """Cancel an existing order"""
        try:
            result = self.client.cancel_order(symbol=symbol, orderId=order_id)
            logger.info(f"Order {order_id} cancelled")
            return result
        except BinanceAPIException as e:
            logger.error(f"Failed to cancel order: {e}")
            raise
    
    def get_open_orders(self, symbol: str = None) -> List[Dict]:
        """Get all open orders"""
        try:
            if symbol:
                orders = self.client.get_open_orders(symbol=symbol)
            else:
                orders = self.client.get_open_orders()
            return orders
        except BinanceAPIException as e:
            logger.error(f"Failed to get open orders: {e}")
            raise
    
    def get_order_status(self, symbol: str, order_id: int) -> Dict:
        """Get status of a specific order"""
        try:
            order = self.client.get_order(symbol=symbol, orderId=order_id)
            return order
        except BinanceAPIException as e:
            logger.error(f"Failed to get order status: {e}")
            raise
