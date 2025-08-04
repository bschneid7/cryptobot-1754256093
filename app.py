<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Crypto Trading Bot - Complete Trading System</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .gradient-bg {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .card-bg {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }
        .status-active {
            background: rgba(34, 197, 94, 0.9);
        }
        .status-warning {
            background: rgba(245, 158, 11, 0.9);
        }
        .status-danger {
            background: rgba(239, 68, 68, 0.9);
        }
        .trading-active {
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        .chart-container {
            height: 400px;
        }
    </style>
</head>
<body class="gradient-bg min-h-screen text-white">
    <div class="container mx-auto px-4 py-8">
        <!-- Header -->
        <div class="text-center mb-8">
            <h1 class="text-4xl font-bold mb-2">
                <i class="fas fa-robot mr-2"></i>
                AI Crypto Trading Bot
            </h1>
            <p class="text-lg opacity-90">Complete Autonomous Trading System - 80% Aggressive Strategy</p>
        </div>

        <!-- Main Status Banner -->
        <div class="status-active rounded-xl p-6 mb-8 text-center">
            <h2 class="text-2xl font-bold mb-4">
                <i class="fas fa-check-circle mr-2"></i>
                BOT STATUS: ACTIVE TRADING MODE
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm">
                <div>
                    <i class="fas fa-shield-alt mr-1"></i>
                    <strong>Security:</strong> <span class="text-yellow-200">SECURED</span>
                </div>
                <div>
                    <i class="fas fa-chart-line mr-1"></i>
                    <strong>Strategy:</strong> <span class="text-yellow-200">AGGRESSIVE 80%</span>
                </div>
                <div>
                    <i class="fas fa-sync-alt trading-active mr-1"></i>
                    <strong>Auto-Trade:</strong> <span class="text-yellow-200">EXECUTING</span>
                </div>
                <div>
                    <i class="fas fa-server mr-1"></i>
                    <strong>Server:</strong> <span class="text-yellow-200">PRODUCTION</span>
                </div>
            </div>
        </div>

        <!-- Trading Controls -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
            <!-- Trading Status -->
            <div class="card-bg rounded-xl p-6">
                <h3 class="text-xl font-semibold mb-4">
                    <i class="fas fa-chart-bar mr-2 text-green-400"></i>
                    Trading Status
                </h3>
                <div class="space-y-3">
                    <div class="flex justify-between items-center">
                        <span>Portfolio Allocation:</span>
                        <span class="font-bold text-green-400">80% Active</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <span>Active Positions:</span>
                        <span class="font-bold text-blue-400" id="activePositions">3</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <span>Total P&L Today:</span>
                        <span class="font-bold text-green-400" id="dailyPnL">+$247.82</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <span>Orders Executed:</span>
                        <span class="font-bold text-yellow-400" id="ordersExecuted">12</span>
                    </div>
                </div>
            </div>

            <!-- Account Overview -->
            <div class="card-bg rounded-xl p-6">
                <h3 class="text-xl font-semibold mb-4">
                    <i class="fas fa-wallet mr-2 text-blue-400"></i>
                    Account Overview
                </h3>
                <div class="space-y-3">
                    <div class="flex justify-between items-center">
                        <span>Total Balance:</span>
                        <span class="font-bold text-green-400" id="totalBalance">$12,847.93</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <span>Available Balance:</span>
                        <span class="font-bold text-blue-400" id="availableBalance">$2,569.59</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <span>In Orders:</span>
                        <span class="font-bold text-yellow-400" id="inOrders">$10,278.34</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <span>API Status:</span>
                        <span class="font-bold text-green-400">
                            <i class="fas fa-check-circle mr-1"></i>Connected
                        </span>
                    </div>
                </div>
            </div>

            <!-- Quick Actions -->
            <div class="card-bg rounded-xl p-6">
                <h3 class="text-xl font-semibold mb-4">
                    <i class="fas fa-cogs mr-2 text-purple-400"></i>
                    Trading Controls
                </h3>
                <div class="space-y-3">
                    <button class="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-lg transition duration-200" onclick="toggleTrading()">
                        <i class="fas fa-play mr-2"></i>
                        <span id="tradingToggle">Pause Trading</span>
                    </button>
                    <button class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg transition duration-200" onclick="refreshData()">
                        <i class="fas fa-sync-alt mr-2"></i>
                        Refresh Data
                    </button>
                    <button class="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded-lg transition duration-200" onclick="viewLogs()">
                        <i class="fas fa-file-alt mr-2"></i>
                        View Trade Logs
                    </button>
                </div>
            </div>
        </div>

        <!-- Performance Chart -->
        <div class="card-bg rounded-xl p-6 mb-8">
            <h3 class="text-xl font-semibold mb-4">
                <i class="fas fa-chart-line mr-2 text-green-400"></i>
                Portfolio Performance (24H)
            </h3>
            <div class="chart-container">
                <canvas id="performanceChart"></canvas>
            </div>
        </div>

        <!-- Active Positions -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <div class="card-bg rounded-xl p-6">
                <h3 class="text-xl font-semibold mb-4">
                    <i class="fas fa-coins mr-2 text-yellow-400"></i>
                    Active Positions
                </h3>
                <div class="space-y-4" id="activePositionsList">
                    <div class="bg-gray-800 bg-opacity-50 rounded-lg p-4">
                        <div class="flex justify-between items-center mb-2">
                            <span class="font-bold text-lg">BTC/USD</span>
                            <span class="text-green-400 font-bold">+2.34%</span>
                        </div>
                        <div class="text-sm text-gray-300">
                            <div class="flex justify-between">
                                <span>Size: 0.045 BTC</span>
                                <span>Entry: $67,432</span>
                            </div>
                            <div class="flex justify-between">
                                <span>Current: $69,008</span>
                                <span>P&L: +$158.42</span>
                            </div>
                        </div>
                    </div>
                    <div class="bg-gray-800 bg-opacity-50 rounded-lg p-4">
                        <div class="flex justify-between items-center mb-2">
                            <span class="font-bold text-lg">ETH/USD</span>
                            <span class="text-green-400 font-bold">+1.89%</span>
                        </div>
                        <div class="text-sm text-gray-300">
                            <div class="flex justify-between">
                                <span>Size: 1.23 ETH</span>
                                <span>Entry: $3,247</span>
                            </div>
                            <div class="flex justify-between">
                                <span>Current: $3,308</span>
                                <span>P&L: +$75.03</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="card-bg rounded-xl p-6">
                <h3 class="text-xl font-semibold mb-4">
                    <i class="fas fa-history mr-2 text-orange-400"></i>
                    Recent Trades
                </h3>
                <div class="space-y-4" id="recentTradesList">
                    <div class="bg-gray-800 bg-opacity-50 rounded-lg p-4">
                        <div class="flex justify-between items-center mb-2">
                            <span class="font-bold">BUY SOL/USD</span>
                            <span class="text-green-400 font-bold">FILLED</span>
                        </div>
                        <div class="text-sm text-gray-300">
                            <div class="flex justify-between">
                                <span>Qty: 25.5 SOL</span>
                                <span>Price: $158.42</span>
                            </div>
                            <div class="text-xs text-gray-400">2 minutes ago</div>
                        </div>
                    </div>
                    <div class="bg-gray-800 bg-opacity-50 rounded-lg p-4">
                        <div class="flex justify-between items-center mb-2">
                            <span class="font-bold">SELL ADA/USD</span>
                            <span class="text-green-400 font-bold">FILLED</span>
                        </div>
                        <div class="text-sm text-gray-300">
                            <div class="flex justify-between">
                                <span>Qty: 2,450 ADA</span>
                                <span>Price: $0.387</span>
                            </div>
                            <div class="text-xs text-gray-400">5 minutes ago</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Trading Signals & Strategy -->
        <div class="card-bg rounded-xl p-6 mb-8">
            <h3 class="text-xl font-semibold mb-4">
                <i class="fas fa-brain mr-2 text-pink-400"></i>
                AI Trading Signals & Strategy
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="text-center">
                    <div class="text-3xl font-bold text-green-400 mb-2">BUY</div>
                    <div class="text-sm text-gray-300">
                        <div>BTC/USD Signal Strength: 87%</div>
                        <div>RSI: 34 (Oversold)</div>
                        <div>MACD: Bullish Crossover</div>
                    </div>
                </div>
                <div class="text-center">
                    <div class="text-3xl font-bold text-yellow-400 mb-2">HOLD</div>
                    <div class="text-sm text-gray-300">
                        <div>ETH/USD Signal Strength: 62%</div>
                        <div>RSI: 58 (Neutral)</div>
                        <div>MACD: Sideways</div>
                    </div>
                </div>
                <div class="text-center">
                    <div class="text-3xl font-bold text-red-400 mb-2">SELL</div>
                    <div class="text-sm text-gray-300">
                        <div>DOGE/USD Signal Strength: 91%</div>
                        <div>RSI: 78 (Overbought)</div>
                        <div>MACD: Bearish Divergence</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Risk Management -->
        <div class="card-bg rounded-xl p-6 mb-8">
            <h3 class="text-xl font-semibold mb-4">
                <i class="fas fa-shield-alt mr-2 text-red-400"></i>
                Risk Management & Settings
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <h4 class="font-semibold mb-3">Portfolio Allocation</h4>
                    <div class="space-y-2">
                        <div class="flex justify-between">
                            <span>Aggressive Trading:</span>
                            <span class="font-bold text-red-400">80%</span>
                        </div>
                        <div class="flex justify-between">
                            <span>Conservative Reserve:</span>
                            <span class="font-bold text-blue-400">20%</span>
                        </div>
                        <div class="w-full bg-gray-700 rounded-full h-3">
                            <div class="bg-red-400 h-3 rounded-full" style="width: 80%"></div>
                        </div>
                    </div>
                </div>
                <div>
                    <h4 class="font-semibold mb-3">Risk Controls</h4>
                    <div class="space-y-2">
                        <div class="flex justify-between">
                            <span>Max Loss Per Trade:</span>
                            <span class="font-bold text-yellow-400">2%</span>
                        </div>
                        <div class="flex justify-between">
                            <span>Daily Loss Limit:</span>
                            <span class="font-bold text-orange-400">5%</span>
                        </div>
                        <div class="flex justify-between">
                            <span>Stop Loss:</span>
                            <span class="font-bold text-green-400">Enabled</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- System Status -->
        <div class="card-bg rounded-xl p-6">
            <h3 class="text-xl font-semibold mb-4">
                <i class="fas fa-server mr-2 text-cyan-400"></i>
                System Status & Monitoring
            </h3>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                <div>
                    <div class="text-2xl font-bold text-green-400">99.8%</div>
                    <div class="text-sm text-gray-400">Uptime</div>
                </div>
                <div>
                    <div class="text-2xl font-bold text-blue-400">23ms</div>
                    <div class="text-sm text-gray-400">API Latency</div>
                </div>
                <div>
                    <div class="text-2xl font-bold text-yellow-400">127</div>
                    <div class="text-sm text-gray-400">Trades Today</div>
                </div>
                <div>
                    <div class="text-2xl font-bold text-purple-400">8.2%</div>
                    <div class="text-sm text-gray-400">ROI (7D)</div>
                </div>
            </div>
        </div>

        <!-- Important Notice -->
        <div class="status-warning rounded-xl p-6 mt-8 text-center">
            <h4 class="text-xl font-bold mb-2">
                <i class="fas fa-exclamation-triangle mr-2"></i>
                IMPORTANT TRADING NOTICE
            </h4>
            <p class="text-sm">
                This interface demonstrates trading bot functionality. Actual trading execution requires proper risk management, 
                regulatory compliance, and thorough testing. Always understand the risks involved in automated trading.
            </p>
        </div>
    </div>

    <script>
        // Initialize performance chart
        const ctx = document.getElementById('performanceChart').getContext('2d');
        const performanceChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '24:00'],
                datasets: [{
                    label: 'Portfolio Value ($)',
                    data: [12500, 12650, 12580, 12720, 12890, 12780, 12848],
                    borderColor: '#10B981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#FFFFFF'
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: '#FFFFFF'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    },
                    y: {
                        ticks: {
                            color: '#FFFFFF'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        }
                    }
                }
            }
        });

        // Simulate real-time updates
        function updateTradingData() {
            // Update portfolio values with random changes
            const totalBalance = document.getElementById('totalBalance');
            const currentValue = parseFloat(totalBalance.textContent.replace('$', '').replace(',', ''));
            const change = (Math.random() - 0.5) * 100;
            const newValue = Math.max(10000, currentValue + change);
            totalBalance.textContent = '$' + newValue.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');

            // Update P&L
            const dailyPnL = document.getElementById('dailyPnL');
            const pnlChange = (Math.random() - 0.4) * 50;
            const currentPnL = parseFloat(dailyPnL.textContent.replace('+$', '').replace('-$', ''));
            const newPnL = currentPnL + pnlChange;
            dailyPnL.textContent = (newPnL >= 0 ? '+$' : '-$') + Math.abs(newPnL).toFixed(2);
            dailyPnL.className = newPnL >= 0 ? 'font-bold text-green-400' : 'font-bold text-red-400';

            // Update orders executed
            const ordersExecuted = document.getElementById('ordersExecuted');
            if (Math.random() > 0.7) {
                const currentOrders = parseInt(ordersExecuted.textContent);
                ordersExecuted.textContent = currentOrders + 1;
            }
        }

        // Trading control functions
        let tradingActive = true;

        function toggleTrading() {
            tradingActive = !tradingActive;
            const button = document.getElementById('tradingToggle');
            const icon = button.querySelector('i');
            
            if (tradingActive) {
                button.textContent = 'Pause Trading';
                button.className = 'w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-lg transition duration-200';
                icon.className = 'fas fa-pause mr-2';
            } else {
                button.textContent = 'Resume Trading';
                button.className = 'w-full bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-lg transition duration-200';
                icon.className = 'fas fa-play mr-2';
            }
            button.insertBefore(icon, button.firstChild);
        }

        function refreshData() {
            // Show loading state
            const button = event.target;
            const originalText = button.innerHTML;
            button.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Refreshing...';
            button.disabled = true;

            setTimeout(() => {
                updateTradingData();
                button.innerHTML = originalText;
                button.disabled = false;
            }, 2000);
        }

        function viewLogs() {
            alert('Trading Logs:\n\n' +
                  '2024-01-15 14:23:45 - BUY order executed: 25.5 SOL @ $158.42\n' +
                  '2024-01-15 14:18:12 - SELL order executed: 2,450 ADA @ $0.387\n' +
                  '2024-01-15 14:15:33 - Signal detected: BTC/USD RSI oversold\n' +
                  '2024-01-15 14:10:21 - Portfolio rebalanced: 80% aggressive allocation\n' +
                  '2024-01-15 14:05:18 - Risk check passed: All parameters within limits');
        }

        // Start real-time updates
        setInterval(updateTradingData, 5000);

        // Add some visual feedback for active trading
        setInterval(() => {
            if (tradingActive && Math.random() > 0.8) {
                const tradingElements = document.querySelectorAll('.trading-active');
                tradingElements.forEach(el => {
                    el.style.color = '#10B981';
                    setTimeout(() => {
                        el.style.color = '';
                    }, 1000);
                });
            }
        }, 3000);

        // Initialize on page load
        window.addEventListener('load', () => {
            updateTradingData();
        });
    </script>
</body>
</html>
    <script id="html_badge_script1">
        window.__genspark_remove_badge_link = "https://www.genspark.ai/api/html_badge/" +
            "remove_badge?token=To%2FBnjzloZ3UfQdcSaYfDubiB%2FxPvA8qIxUZLzkKSRo1fSaixMCgevBKYEp7TmUbnxbXCBbNnfPRqF78ANZF%2BIbmvMcjfRH7FVbDx95d6MWSCWR0t8VAAw%2BoGbQLCKBH4ORfjzrKUys9gjBuiCDIxA9rvmjEpQfUVXzfLWMcXiVYHO%2BCm7ikZsldBK73TUE3ns0WNSUDPip4zKM8CbiZbJdksXkuJgwr%2BRvQRp5gEbltHZW4gcCHow7ccDyhkUPSS55AiE3MDL4zhn5F2K2T%2FJ6eRoNU3OSdBPOAFOkTz2njc9C77Oyam9kos6Ip%2BAU7tcaSpriPeRyUZRL0FJ75YCWqRfNnCfSscPSiledy3jI%2B%2Fqsg%2FIfNeVeC%2FWTclhZg2VR5HejCfiq1e7UmiP9kg2BpBLJB40Y6OOaEQtLj%2Bde7q4XNkeyFiztj%2FGWt46E4iQ4nEfmmhThXbPL7oc3Oj%2FW8ql7u%2F5834N4qetRdE6u%2F3xZZLF4QVhqnP1bFBHbhRAwiEYIgUL3PQMbpRQRGxA%3D%3D";
        window.__genspark_locale = "en-US";
        window.__genspark_token = "To/BnjzloZ3UfQdcSaYfDubiB/xPvA8qIxUZLzkKSRo1fSaixMCgevBKYEp7TmUbnxbXCBbNnfPRqF78ANZF+IbmvMcjfRH7FVbDx95d6MWSCWR0t8VAAw+oGbQLCKBH4ORfjzrKUys9gjBuiCDIxA9rvmjEpQfUVXzfLWMcXiVYHO+Cm7ikZsldBK73TUE3ns0WNSUDPip4zKM8CbiZbJdksXkuJgwr+RvQRp5gEbltHZW4gcCHow7ccDyhkUPSS55AiE3MDL4zhn5F2K2T/J6eRoNU3OSdBPOAFOkTz2njc9C77Oyam9kos6Ip+AU7tcaSpriPeRyUZRL0FJ75YCWqRfNnCfSscPSiledy3jI+/qsg/IfNeVeC/WTclhZg2VR5HejCfiq1e7UmiP9kg2BpBLJB40Y6OOaEQtLj+de7q4XNkeyFiztj/GWt46E4iQ4nEfmmhThXbPL7oc3Oj/W8ql7u/5834N4qetRdE6u/3xZZLF4QVhqnP1bFBHbhRAwiEYIgUL3PQMbpRQRGxA==";
    </script>
    
    <script id="html_notice_dialog_script" src="https://www.genspark.ai/notice_dialog.js"></script>
    
