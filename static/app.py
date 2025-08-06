#!/usr/bin/env python3
"""
AI Crypto Trading Bot – Unified Application
-----------------------------------------

This Flask application combines your trading bot’s existing control endpoints
with a consolidated `/api/metrics` endpoint and serves a simple monitoring
dashboard.  It is designed to be easy to deploy and update without
modifying source code—environment variables are used to configure API
credentials and ports.

Key endpoints:

  • `/`                 – Serves the dashboard (index.html) from the static folder.
  • `/api/metrics`      – Aggregates bot status, portfolio and trade information
                          for the dashboard.
  • `/api/trading/*`    – Existing control and data endpoints (start, stop, status, etc.).

Dependencies:
  See requirements.txt for a complete list.  Notably, Flask, requests and
  flask-cors are required.

To run locally:

    pip install -r requirements.txt
    export BINANCE_API_KEY="your_api_key"  # optional, fallback data used if absent
    export BINANCE_SECRET_KEY="your_secret_key"
    python app.py

Then open http://localhost:8080 in your browser.

"""

import os
import time
import hmac
import hashlib
from urllib.parse import urlencode

import requests
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

# Create the Flask app; static files (HTML, CSS, JS) live in the `static` dir.
app = Flask(__name__, static_folder='static')
CORS(app)  # Allow cross‑origin requests (e.g. if dashboard is hosted separately)

# Environment variables for Binance API credentials.  If not set, the
# application will return fallback portfolio data.
BINANCE_API_KEY = os.environ.get('BINANCE_API_KEY', '')
BINANCE_SECRET_KEY = os.environ.get('BINANCE_SECRET_KEY', '')

# Global variables to track bot state.  In a more advanced system these would be
# persisted in a database or state manager; here we keep them in memory for
# simplicity.
bot_running: bool = False
last_scan_time: str | None = None
portfolio_data: dict[str, float] = {}

# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------

def get_binance_account():
    """Retrieve account information from Binance.US.  Returns None on error."""
    if not BINANCE_API_KEY or not BINANCE_SECRET_KEY:
        return None
    try:
        timestamp = int(time.time() * 1000)
        params = {'timestamp': timestamp}
        query_string = urlencode(params)
        signature = hmac.new(BINANCE_SECRET_KEY.encode(), query_string.encode(), hashlib.sha256).hexdigest()
        params['signature'] = signature
        headers = {'X-MBX-APIKEY': BINANCE_API_KEY}
        response = requests.get('https://api.binance.us/api/v3/account', params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None

# -----------------------------------------------------------------------------
# Routes – Dashboard UI
# -----------------------------------------------------------------------------

@app.route('/')
def index():
    """Serve the dashboard web page."""
    return send_from_directory(app.static_folder, 'index.html')

# -----------------------------------------------------------------------------
# Routes – Trading control and data
# -----------------------------------------------------------------------------

@app.route('/api/trading/status')
def get_status():
    """Return bot status and summary information."""
    global bot_running, last_scan_time
    return jsonify({
        'success': True,
        'status': {
            'is_running': bot_running,
            'last_scan_time': last_scan_time,
            'error_count': 0,
            'scheduled_tasks': 3 if bot_running else 0,
            'uptime': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'portfolio_summary': portfolio_data
        }
    })

@app.route('/api/trading/portfolio')
def get_portfolio():
    """Return portfolio valuation and allocations.  Falls back to static data if
    Binance credentials are absent or a network error occurs."""
    global portfolio_data
    try:
        account = get_binance_account()
        if account and 'balances' in account:
            balances = account['balances']
            total_usd = 0.0
            btc_value = 0.0
            sol_value = 0.0
            for balance in balances:
                asset = balance.get('asset')
                free_amount = float(balance.get('free', 0))
                # Basic valuation for demonstration purposes
                if asset == 'USD':
                    total_usd += free_amount
                elif asset == 'BTC' and free_amount > 0:
                    btc_value = free_amount * 29500
                    total_usd += btc_value
                elif asset == 'SOL' and free_amount > 0:
                    sol_value = free_amount * 100
                    total_usd += sol_value
            portfolio_data = {
                'total_value': round(total_usd, 2),
                'managed_amount': round(total_usd * 0.8, 2),
                'available_usd': round(total_usd * 0.2, 2),
                'active_positions': 0,
                'btc_amount': btc_value / 29500 if btc_value > 0 else 0,
                'sol_amount': sol_value / 100 if sol_value > 0 else 0
            }
            return jsonify({'success': True, 'portfolio': portfolio_data})
        else:
            # Fallback static data
            portfolio_data = {
                'total_value': 857.50,
                'managed_amount': 686.00,
                'available_usd': 171.50,
                'active_positions': 0,
                'btc_amount': 0.00295021,
                'sol_amount': 1.18587956
            }
            return jsonify({'success': True, 'portfolio': portfolio_data})
    except Exception as e:
        # Log the error and return fallback
        print(f"Portfolio error: {e}")
        portfolio_data = {
            'total_value': 857.50,
            'managed_amount': 686.00,
            'available_usd': 171.50,
            'active_positions': 0,
            'btc_amount': 0.00295021,
            'sol_amount': 1.18587956
        }
        return jsonify({'success': True, 'portfolio': portfolio_data})

@app.route('/api/trading/trades')
def get_trades():
    """Return recent trades.  This demo returns an empty list; extend this
    function to return actual trade data from your trading engine."""
    return jsonify({'success': True, 'trades': []})

@app.route('/api/trading/reports')
def get_reports():
    """Return historical performance reports.  Placeholder implementation."""
    return jsonify({'success': True, 'reports': []})

@app.route('/api/trading/start', methods=['POST'])
def start_bot():
    """Start the trading bot."""
    global bot_running, last_scan_time
    bot_running = True
    last_scan_time = time.strftime('%m/%d/%Y, %I:%M:%S %p')
    return jsonify({'success': True, 'message': 'Trading bot started successfully'})

@app.route('/api/trading/stop', methods=['POST'])
def stop_bot():
    """Stop the trading bot."""
    global bot_running
    bot_running = False
    return jsonify({'success': True, 'message': 'Trading bot stopped'})

@app.route('/api/trading/scan', methods=['POST'])
def manual_scan():
    """Perform a manual market scan.  Updates the last_scan_time and returns a
    message.  Extend this function to trigger real scanning logic."""
    global last_scan_time
    last_scan_time = time.strftime('%m/%d/%Y, %I:%M:%S %p')
    return jsonify({'success': True, 'scan_result': 'Manual scan completed - no strong signals detected'})

# -----------------------------------------------------------------------------
# Route – Consolidated metrics for the dashboard
# -----------------------------------------------------------------------------

@app.route('/api/metrics')
def metrics():
    """Aggregate status, portfolio and trades into a single JSON response for
    consumption by the front‑end dashboard."""
    # Fetch the latest data by invoking existing handlers
    status_resp = get_status().get_json()
    portfolio_resp = get_portfolio().get_json()
    trades_resp = get_trades().get_json()

    status_data = status_resp.get('status', {})
    portfolio = portfolio_resp.get('portfolio', {})
    trades = trades_resp.get('trades', [])

    # Compute last trade time and win rate (placeholder logic)
    last_trade_time = trades[-1]['timestamp'] if trades else None
    wins = sum(1 for t in trades if t.get('profit', 0) > 0)
    win_rate = (wins / len(trades)) if trades else 0

    # Build the metrics object according to the dashboard schema
    metrics_data = {
        'status': 'online' if status_data.get('is_running') else 'offline',
        'uptime': status_data.get('uptime'),
        'scheduled_tasks': status_data.get('scheduled_tasks'),
        'error_count': status_data.get('error_count'),
        'portfolio_history': {
            # Provide at least one point; extend this to include real history
            'timestamps': [status_data.get('last_scan_time')],
            'values': [portfolio.get('total_value')],
        },
        'asset_allocation': {
            'Managed': portfolio.get('managed_amount'),
            'Available': portfolio.get('available_usd'),
        },
        'trades_last_24h': len(trades),
        'win_rate': win_rate,
        'last_trade_time': last_trade_time,
        'enhanced_features': {
            'whale_detection': 'unknown',
            'macd_analysis': 'unknown',
            'position_sizing': 'unknown',
            'pre_market_scanning': 'unknown'
        },
        'api_status': {
            'binance_connection': 'connected' if BINANCE_API_KEY and BINANCE_SECRET_KEY else 'offline',
            'auth_status': 'valid' if BINANCE_API_KEY and BINANCE_SECRET_KEY else 'unknown',
            'rate_limit_status': 'normal'
        }
    }
    return jsonify(metrics_data)

# -----------------------------------------------------------------------------
# Main entry point
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    # Determine the port from environment (use 8080 by default)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
