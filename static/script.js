// script.js
// This script fetches metrics from the Flask backend and updates the UI.

// API endpoint for metrics.  Because index.html and this script are served from
// the same host as the Flask app, we can use a relative path.
const API_ENDPOINT = '/api/metrics';
const FALLBACK_FILE = 'metrics-example.json';

let portfolioChart;
let allocationChart;

async function fetchMetrics() {
  try {
    const response = await fetch(API_ENDPOINT, { cache: 'no-store' });
    if (!response.ok) {
      throw new Error('API response not OK');
    }
    return await response.json();
  } catch (error) {
    console.warn('Metrics API error:', error.message);
    // Try the fallback file if the API fails
    const resp = await fetch(FALLBACK_FILE);
    return await resp.json();
  }
}

function formatUptime(seconds) {
  if (typeof seconds !== 'number') return seconds || '–';
  const days = Math.floor(seconds / 86400);
  seconds %= 86400;
  const hrs = Math.floor(seconds / 3600);
  seconds %= 3600;
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  let str = '';
  if (days > 0) str += `${days}d `;
  if (hrs > 0 || days > 0) str += `${hrs}h `;
  if (mins > 0 || hrs > 0 || days > 0) str += `${mins}m `;
  str += `${secs}s`;
  return str;
}

function setBadge(element, status) {
  element.classList.remove('badge-online', 'badge-offline', 'badge-unknown', 'badge-warning', 'bg-primary', 'bg-success', 'bg-secondary', 'bg-danger', 'bg-warning');
  let text = status;
  switch (status) {
    case 'online':
    case 'connected':
    case 'valid':
      element.classList.add('badge-online');
      text = 'Online';
      break;
    case 'offline':
    case 'disconnected':
    case 'invalid':
      element.classList.add('badge-offline');
      text = 'Offline';
      break;
    case 'warning':
      element.classList.add('badge-warning');
      text = 'Warning';
      break;
    case 'unknown':
    default:
      element.classList.add('badge-unknown');
      text = 'Unknown';
      break;
  }
  element.textContent = text;
}

function updateDashboard(data) {
  // Update system status
  const statusEl = document.getElementById('bot-status');
  const uptimeEl = document.getElementById('bot-uptime');
  const tasksEl = document.getElementById('tasks-count');
  const errorEl = document.getElementById('error-count');
  const statusText = data.status || 'unknown';
  statusEl.textContent = statusText.charAt(0).toUpperCase() + statusText.slice(1);
  statusEl.className = '';
  statusEl.classList.add('fw-bold');
  if (statusText === 'online') statusEl.classList.add('text-success');
  else if (statusText === 'offline') statusEl.classList.add('text-danger');
  else statusEl.classList.add('text-secondary');
  if (typeof data.uptime === 'number') uptimeEl.textContent = formatUptime(data.uptime);
  else uptimeEl.textContent = data.uptime || '–';
  tasksEl.textContent = data.scheduled_tasks ?? '–';
  errorEl.textContent = data.error_count ?? '–';
  // Trades
  document.getElementById('trade-count').textContent = data.trades_last_24h ?? '–';
  document.getElementById('win-rate').textContent = data.win_rate !== undefined ? `${Math.round((data.win_rate || 0) * 100)}%` : '–';
  document.getElementById('last-trade').textContent = data.last_trade_time ? new Date(data.last_trade_time).toLocaleString() : '–';
  // Enhanced features
  if (data.enhanced_features) {
    setBadge(document.getElementById('whale-detection'), data.enhanced_features.whale_detection ?? 'unknown');
    setBadge(document.getElementById('macd-status'), data.enhanced_features.macd_analysis ?? 'unknown');
    setBadge(document.getElementById('position-sizing'), data.enhanced_features.position_sizing ?? 'unknown');
    setBadge(document.getElementById('pre-market-scanning'), data.enhanced_features.pre_market_scanning ?? 'unknown');
  }
  // API connectivity
  if (data.api_status) {
    setBadge(document.getElementById('binance-status'), data.api_status.binance_connection ?? 'unknown');
    setBadge(document.getElementById('auth-status'), data.api_status.auth_status ?? 'unknown');
    setBadge(document.getElementById('rate-limit'), data.api_status.rate_limit_status ?? 'unknown');
  }
  // Charts
  const timestamps = data.portfolio_history?.timestamps ?? [];
  const values = data.portfolio_history?.values ?? [];
  const labels = timestamps.map(ts => ts ? new Date(ts).toLocaleString() : '');
  updatePortfolioChart(labels, values);
  const allocation = data.asset_allocation ?? {};
  updateAllocationChart(Object.keys(allocation), Object.values(allocation));
  // Update last updated time
  document.getElementById('last-updated').textContent = new Date().toLocaleString();
}

function updatePortfolioChart(labels, values) {
  const ctx = document.getElementById('portfolioValueChart').getContext('2d');
  if (portfolioChart) {
    portfolioChart.data.labels = labels;
    portfolioChart.data.datasets[0].data = values;
    portfolioChart.update();
  } else {
    portfolioChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Portfolio Value (USD)',
            data: values,
            borderColor: 'rgba(13, 110, 253, 0.8)',
            backgroundColor: 'rgba(13, 110, 253, 0.3)',
            fill: true,
            tension: 0.2
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            title: {
              display: true,
              text: 'Time'
            }
          },
          y: {
            title: {
              display: true,
              text: 'Value (USD)'
            },
            beginAtZero: false
          }
        }
      }
    });
  }
}

function updateAllocationChart(labels, values) {
  const ctx = document.getElementById('assetAllocationChart').getContext('2d');
  const backgroundColors = [
    '#0d6efd', '#198754', '#dc3545', '#ffc107', '#6610f2', '#6f42c1', '#d63384'
  ];
  if (allocationChart) {
    allocationChart.data.labels = labels;
    allocationChart.data.datasets[0].data = values;
    allocationChart.update();
  } else {
    allocationChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [
          {
            data: values,
            backgroundColor: backgroundColors.slice(0, labels.length),
            borderColor: '#fff',
            borderWidth: 1
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'right'
          }
        }
      }
    });
  }
}

async function refreshMetrics() {
  const data = await fetchMetrics();
  updateDashboard(data);
}

// Initial fetch
refreshMetrics();
// Periodically refresh every minute
setInterval(refreshMetrics, 60000);