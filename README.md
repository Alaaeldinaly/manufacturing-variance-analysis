# Manufacturing Schedule Variance & Operational Efficiency Analysis

## 📌 Business Overview
This project provides an executive analysis of 1,000 hybrid manufacturing operations to identify schedule variances, operational bottlenecks, and energy inefficiencies using **Python** and **Power BI**.

## 📊 Key Findings
- **Execution vs. Setup Delay:** Machine processing time matches schedule duration perfectly ($\Delta T_{\text{Processing}} = 0$). Delays occur exclusively due to **Start Lag** during prep/setup.
- **Start Lag Threshold:**
  - `Completed`: Starts within $[-5, +5]$ minutes.
  - `Delayed`: Starts with $+10$ to $+30$ minutes delay (Average delay: **20.1 minutes**).
  - `Failed`: Represents **12.9%** of total jobs without execution start timestamps.
- **Machine Bottlenecks:** Machine **M05** registered the highest delay rate (**24.9%**), whereas **M04** registered the highest failure rate (**17.6%**).

## 🚀 How to Run
1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/manufacturing-variance-analysis.git](https://github.com/your-username/manufacturing-variance-analysis.git)