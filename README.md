# AI Crypto Trading Bot – Easy Deployment Package

Welcome!  This folder contains everything you need to run your AI crypto trading bot **and** monitor it with a simple dashboard.  You don’t need to be a programmer—just follow the steps below.

## 📦 What’s inside?

- **app.py** – The main program.  It runs your trading bot and makes data available over the web.
- **static/** – A folder full of web files:
  - `index.html` – the dashboard you look at in your browser.
  - `style.css` – colours and layout for the dashboard.
  - `script.js` – small program that fetches data and updates the dashboard.
  - `metrics-example.json` – a backup file used if your bot isn’t running.
- **requirements.txt** – a list of Python libraries you need.
- **Procfile** and **runtime.txt** – extra files for platforms like Heroku or Azure App Service.
- **README.md** – this guide.

## 🚀 How to run it (step by step)

1. **Install Python** if you haven’t already (version 3.9 or higher is fine).

2. **Open a terminal** (Command Prompt on Windows, Terminal on Mac/Linux) and go into this folder.  For example:

   ```bash
   cd path/to/crypto_bot_full_app
   ```

3. **Install the required Python libraries**.  Type:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set your Binance API keys (optional but recommended)**.  In the same terminal, type:

   ```bash
   export BINANCE_API_KEY="your_api_key_here"
   export BINANCE_SECRET_KEY="your_secret_key_here"
   ```

   Replace `your_api_key_here` and `your_secret_key_here` with your real API keys.  If you skip this step, the bot will use fallback values and the dashboard will still work—but it won’t show real balances.

5. **Run the bot**.  Type:

   ```bash
   python app.py
   ```

   The program will start and tell you it’s running on a port (by default **8080**).

6. **Open the dashboard**.  In your browser, go to:

   - `http://localhost:8080` on the computer where you ran the program.

   You should see the dashboard update every minute.  Green means your bot is “online”; red means it’s “offline”.

## 🛠 Controlling the bot

The bot provides a few special web addresses (called **API endpoints**) that let you start and stop trading or trigger a market scan.  You don’t need to use these unless you want to:

- `POST /api/trading/start` – Start trading
- `POST /api/trading/stop` – Stop trading
- `POST /api/trading/scan` – Run a quick market scan
- `GET /api/trading/status` – Check if the bot is running
- `GET /api/trading/portfolio` – View current portfolio balances
- `GET /api/metrics` – Get all the dashboard data in one place

You can call these with tools like **cURL** or Postman, or build buttons into a future version of the dashboard.

## 🌐 Deploying to the cloud

To run this bot and dashboard on a service like Azure or Heroku, upload the entire folder to your GitHub repository and configure your chosen platform:

1. **Azure App Service** – Choose Node or Python runtime (Python recommended).  Point it to `app.py` as the entry point.  Add your API keys as environment variables in the App Service settings.
2. **Heroku** – Create a new Heroku app, connect your GitHub repository, and deploy.  Heroku will detect the `Procfile` and run `gunicorn app:app`.  Set the environment variables in Heroku’s Config Vars.

Once deployed, the dashboard will be available at your cloud URL (e.g. `https://yourapp.azurewebsites.net`).

## 🔧 Want to customise?

- **Change colours or layout:** Edit `static/style.css`.
- **Adjust the data refresh rate:** Open `static/script.js` and change `setInterval(refreshMetrics, 60000)` to a different number of milliseconds (e.g. `30000` for 30 seconds).
- **Add new charts or metrics:** The dashboard uses [Chart.js](https://www.chartjs.org/), which is easy to extend.  See the examples in `script.js` for how data is turned into charts.

## ❓ Questions or issues?

If you run into problems, check the terminal for error messages.  They usually explain what’s wrong (for example, missing API keys or a network error).  Feel free to reach out with specific questions and I’ll be happy to help!

---

Happy trading!  📈🚀