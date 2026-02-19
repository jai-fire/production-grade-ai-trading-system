"""LLM Integration for trading analysis"""
import os
from loguru import logger
import openai

class LLMClient:
    """OpenAI LLM client for trading decisions"""
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key
        logger.info("LLM client initialized")
    
    def analyze_signal(self, symbol: str, signal: dict) -> str:
        """Analyze trading signal using LLM"""
        prompt = f"""Analyze this crypto trading signal for {symbol}:
        Signal: {signal}
        Provide buy/sell recommendation with reasoning."""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=200
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"LLM analysis failed: {e}")
            return "Unable to analyze"
    
    def generate_report(self, trades: list) -> str:
        """Generate trade report using LLM"""
        prompt = f"""Generate a brief trading performance report:
        Total trades: {len(trades)}
        Trades data: {trades[:5]}
        Provide key insights and recommendations."""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            return "Unable to generate report"
