# 🚀 Trader Sentiment Analysis

> A cryptocurrency market analysis project that studies the relationship between trader performance and market sentiment using the Fear & Greed Index.

---

## 📌 Overview

This project analyzes historical cryptocurrency trading data alongside the **Crypto Fear & Greed Index** to understand how market sentiment affects trader behavior and profitability.

The analysis combines trader activity with sentiment categories such as:

* 😨 Extreme Fear
* 😟 Fear
* 😐 Neutral
* 🙂 Greed
* 🚀 Extreme Greed

The project performs:

* Data cleaning
* Data transformation
* Sentiment mapping
* Statistical analysis
* Correlation analysis
* Visualization of trading performance

---

# 📂 Project Structure

```bash
Assignment1-main/
│
├── analysis_script.py
├── Trader_Sentiment_Analysis_Report.docx
├── README.md
└── .gitignore
```

---

# ✨ Features

## 📊 Data Processing

* Loads historical trading datasets
* Loads Fear & Greed Index data
* Cleans and preprocesses datasets
* Converts timestamps into normalized dates
* Merges sentiment data with trading activity

---

## 🧠 Sentiment Analysis

The project categorizes market sentiment into:

* Fear
* Neutral
* Greed

It then computes:

* ✅ Win Rate
* 💰 Average PnL
* 📈 Median PnL
* 🏆 Total PnL

---

## 📉 Trading Insights

The analysis includes:

* Long vs Short position analysis
* Trade size behavior
* Account-wise profitability
* Coin-level profitability
* Daily sentiment vs profitability correlation

---

## 📷 Visualization

The script generates insightful visualizations such as:

* Win Rate by Sentiment
* Average Profit/Loss by Sentiment
* Trading Performance Comparison
* Sentiment Distribution Charts

---

# 🛠️ Technologies Used

| Technology | Purpose               |
| ---------- | --------------------- |
| Python     | Core Programming      |
| Pandas     | Data Analysis         |
| NumPy      | Numerical Computation |
| Matplotlib | Data Visualization    |
| PyArrow    | Parquet File Support  |

---

# ⚙️ Installation

## 1️⃣ Clone the Repository

```bash
git clone <repository-url>
cd Assignment1-main
```

---

## 2️⃣ Install Required Dependencies

```bash
pip install pandas numpy matplotlib pyarrow
```

---

# 📁 Required Input Files

Place the following CSV files in the project directory before running the script.

---

## 📄 historical_data.csv

Contains:

* Trade timestamps
* Trader account details
* Coin names
* Trade direction
* Closed PnL
* Position size

---

## 📄 fear_greed_index.csv

Contains:

* Date
* Fear & Greed classification
* Index value

---

# ▶️ Running the Project

Run the analysis script using:

```bash
python analysis_script.py
```

---

# 📤 Output

The project generates:

* Cleaned merged dataset
* Statistical summaries
* Correlation analysis
* Performance insights
* Data visualizations
* Exported parquet dataset

Generated file:

```bash
merged.parquet
```

---

# 📌 Key Analysis Metrics

## 📈 Performance Metrics

* Win Rate
* Average Profit/Loss
* Median Profit/Loss
* Total Profit/Loss

---

## 🧾 Behavioral Metrics

* Long vs Short Bias
* Trade Size Trends
* Sentiment-based Trading Behavior

---

## 🌍 Market Metrics

* Fear & Greed Correlation
* Daily Profitability Trends

---

# 🔍 Example Insights

This project helps answer questions like:

* Do traders perform better during fear or greed?
* Are traders more aggressive during extreme sentiment?
* Which cryptocurrencies perform best under different market conditions?
* Does market sentiment significantly influence profitability?

---

# 🚀 Future Improvements

Possible future enhancements include:

* Interactive Dashboards
* Real-Time Sentiment Integration
* Machine Learning Prediction Models
* Automated Strategy Backtesting
* Advanced Statistical Analysis

---

# 👨‍💻 Author

### Data Science Assignment Project

Developed for sentiment-driven cryptocurrency trading analysis.
