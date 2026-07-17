# Enterprise Financial Analytics & BI Dashboard: Microsoft (MSFT) Case Study
*A Portfolio-Grade Business Intelligence & Data Analytics Capstone Project*

---

## 🏆 Recruiter-Friendly Project Title
**Microsoft (MSFT) Enterprise Financial Intelligence & Market Valuation Dashboard: An End-to-End BI and Corporate Finance Case Study (FY2020 - FY2025)**

---

## 📌 Project Overview
This repository hosts a portfolio-grade, end-to-end data analytics and business intelligence project focused on the financial statements and market performance of **Microsoft Corporation (NASDAQ: MSFT)**. 

The case study spans **Fiscal Years 2020 through 2025** and demonstrates a complete data lifecycle:
1. **Data Ingestion:** Extracting stock history via Yahoo Finance and compiling financial metrics from audited SEC Form 10-K filings.
2. **Automated Cleaning Pipeline:** Resolving missing records, sign errors, and string typos programmatically via Python.
3. **Exploratory Data Analysis (EDA):** Visualizing operational expenses, profitability ratios, and segment contributions.
4. **Database Querying (SQL):** Constructing complex relational queries to perform DuPont ROE analysis and rolling stock averages.
5. **Business Intelligence (Power BI Layout):** Modeling data and defining calculated DAX measures for executive reporting.
6. **Insight Storytelling:** Fusing data analytics with corporate finance to deliver 25 actionable business insights and 20 strategic recommendations.

---

## 🛠️ Tech Stack & Skills Highlighted
* **Data Engineering & Scripting:** Python (`pandas`, `numpy`, `requests`, `matplotlib`, `seaborn`, `plotly`)
* **Database & Querying:** SQL (PostgreSQL/MySQL/SQL Server compliant - Window functions, CTEs, Joins, Aggregations)
* **Business Intelligence:** Power BI (Data modeling, Star Schema, dynamic DAX measures, Executive layout design)
* **Financial Analysis:** DuPont ROE Decomposition, Profitability Margins, FCF conversion, Leverage & Solvency ratios.
* **Dashboard Hosting:** Streamlit (For presenting the interactive web application portfolio)

---

## 📁 Repository Structure
```
├── data/
│   ├── raw_annual_financials.csv      # Original financial variables from SEC filings
│   ├── raw_segment_financials.csv     # Segment-level data (Intelligent Cloud, PBP, MPC)
│   ├── raw_quarterly_financials.csv   # Quarterly financial statement breakdowns
│   ├── raw_stock_history.csv          # Stock price records downloaded from Yahoo Finance
│   ├── cleaned_financial_metrics.csv  # Cleaned, standardized annual financials
│   ├── cleaned_segment_financials.csv # Standardized segment revenue & operating income
│   └── cleaned_stock.csv              # Standardized stock data with moving averages (SMA)
├── sql/
│   └── queries.sql                    # SQL scripts for DuPont ROE and stock metrics
├── src/
│   ├── fetch_and_generate.py          # Data ingestion script
│   ├── data_cleaning.py               # Preprocessing and feature engineering pipeline
│   └── eda_analysis.py                # Exploratory analysis and plot generation
├── app.py                             # Interactive Streamlit Portfolio Dashboard
├── requirements.txt                   # Project dependencies
├── business_report.md                 # Detailed Deloitte/McKinsey-style business report
├── presentation.md                    # Consulting-style 16-slide PowerPoint layout
└── interview_prep.md                  # 100 Q&As for job interview preparation
```

---

## 📊 Quick Insights (FY2020 vs FY2025)
* **Revenue CAGR:** **14.52%** (Growing from $143B in FY20 to $281.7B in FY25)
* **Net Income CAGR:** **18.12%** (Growing from $44.2B in FY20 to $101.8B in FY25)
* **Operating Margin:** Expanded from **37.03%** in FY20 to **45.62%** in FY25 (Positive Operating Leverage)
* **Intelligent Cloud Share:** Increased from **33.8%** of total revenue to **43.9%** ($123.8B in FY25)
* **Capital Expenditures:** Surged at a **33.1% CAGR**, peaking at **$64.6B** in FY25 to build global AI infrastructure.
* **Balance Sheet Health:** Debt-to-Equity ratio fell from **0.60** to **0.12**, leaving Microsoft net cash positive.

---

## 🚀 How to Run the Project Locally

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/msft-financial-analytics.git
cd msft-financial-analytics
```

### 2. Set Up a Virtual Environment & Install Dependencies
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
```

### 3. Run the Data Pipeline
Execute the pipeline to regenerate the cleaned datasets and plots:
```bash
python src/fetch_and_generate.py
python src/data_cleaning.py
python src/eda_analysis.py
```

### 4. Run the Streamlit Dashboard
Launch the interactive web application:
```bash
streamlit run app.py
```

---

## 💼 LinkedIn Project Description
*Copy and paste this onto your LinkedIn profile or featured post to showcase your project:*

🚀 **New Project Release: Microsoft (MSFT) Financial Intelligence & Market Valuation Dashboard**

I'm excited to share my latest portfolio project: a deep dive into the financial statement and stock price analytics of Microsoft Corporation (NASDAQ: MSFT) from FY2020 to FY2025. 

Using Python, SQL, and Power BI principles, I trace the financials behind Microsoft's strategic transition into an AI-first cloud provider, evaluating how the company's capital allocation efficiency has adapted to massive capital outlays.

**Key Technical Accomplishments:**
1. **Robust Data Engineering:** Built a Python preprocessing pipeline that automatically handles missing operating cash values, resolves ledger sign errors, and standardizes segment reporting shifts.
2. **Advanced SQL Queries:** Wrote window functions and CTEs to perform DuPont ROE analysis, segment contribution matrices, and 50-day/200-day rolling stock price indicators.
3. **Financial Analytics Framework:** Calculated critical ratios (Gross/Operating Margins, FCF yields, Debt-to-Equity, ROE, ROA) to dissect the drivers of profitability.
4. **Interactive Dashboard App:** Designed an executive-ready dashboard in Streamlit to visualize core trends, budget variances, and forecast stock prices.

**Core Business Insight:** 
While Microsoft's CapEx grew at a **33.1% CAGR** (peaking at a record **$64.6B in FY25** to build AI infrastructure), its Intelligent Cloud segment has scaled efficiently, maintaining operating margins above 36% and driving corporate Return on Equity to **29.7%**.

Check out the full repository and let me know your thoughts! 👇
[Insert GitHub Link]

#DataAnalytics #BusinessIntelligence #PowerBI #SQL #Python #Finance #Microsoft #DataScience

---

## 📄 Resume Project Description
*Add these bullet points to the Projects section of your resume:*

**Microsoft (MSFT) Enterprise Financial Intelligence & Market Valuation Dashboard** | *Python, SQL, Power BI, Streamlit*
* Engineered a Python data pipeline to clean, standardize, and compile Microsoft's SEC Form 10-K financial filings and Yahoo Finance stock history (1,500+ records) spanning FY2020 to FY2025.
* Designed and executed a preprocessing engine that imputed missing cash variables using historical cash conversion ratios (~1.3x) and resolved structural ledger sign errors.
* Developed a database analysis suite using PostgreSQL window functions and CTEs to calculate DuPont ROE breakdowns, quarterly segment contributions, and rolling stock moving averages.
* Designed an executive-grade dashboard layout with interactive KPI trackers, segment decomposition trees, and a waterfall-based budget variance visual.
* Extracted and presented 25 critical business insights analyzing how Microsoft's AI CapEx surge ($64.6B in FY2025) impacts short-term FCF margins (compressed to 25.4%) while expanding long-term operating margins (reaching a record 45.6%).
