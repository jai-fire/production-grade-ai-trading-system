"""Real-time Trading Dashboard with Dash"""
import dash
from dash import dcc, html, callback
import plotly.graph_objects as go
from loguru import logger

class TradingDashboard:
    """Web dashboard for trading system"""
    def __init__(self, host='0.0.0.0', port=8050):
        self.host = host
        self.port = port
        self.app = dash.Dash(__name__)
        self.setup_layout()
        logger.info(f"Dashboard initialized at {host}:{port}")
    
    def setup_layout(self):
        """Setup dashboard layout"""
        self.app.layout = html.Div([
            html.H1('Trading System Dashboard'),
            dcc.Graph(id='price-chart'),
            html.Div(id='metrics'),
            dcc.Interval(id='interval', interval=60000, n_intervals=0)
        ])
    
    def run(self):
        """Run dashboard server"""
        logger.info("Starting dashboard server...")
        self.app.run_server(host=self.host, port=self.port, debug=False)
    
    def create_price_chart(self, df):
        """Create price chart"""
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['close']))
        return fig
    
    def update_metrics(self, trades: list, balance: float):
        """Update performance metrics"""
        if not trades:
            return "No trades yet"
        win_rate = len([t for t in trades if t > 0]) / len(trades)
        return f"Trades: {len(trades)} | Win Rate: {win_rate:.1%} | Balance: {balance}"
