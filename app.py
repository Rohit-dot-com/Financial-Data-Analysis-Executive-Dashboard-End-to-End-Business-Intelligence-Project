import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from datetime import datetime
import os

# Set page configuration
st.set_page_config(
    page_title="Microsoft (MSFT) Executive Financial Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Glassmorphism Look (Dark Theme Accent)
st.markdown("""
<style>
    /* Main Background & Fonts */
    .stApp {
        background-color: #0c0f1d;
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #070913 !important;
        border-right: 1px solid #1e293b;
    }
    
    /* Headings */
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        color: #ffffff;
    }
    
    /* KPI Card styling with Glassmorphism */
    .kpi-card {
        background: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
        transition: transform 0.2s, border-color 0.2s;
        margin-bottom: 10px;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: rgba(0, 120, 212, 0.4);
    }
    .kpi-title {
        font-size: 14px;
        text-transform: uppercase;
        color: #94a3b8;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
        margin-top: 5px;
        margin-bottom: 5px;
    }
    .kpi-delta {
        font-size: 13px;
        font-weight: 600;
    }
    .delta-up {
        color: #10b981;
    }
    .delta-down {
        color: #ef4444;
    }
    
    /* Styled lists for Insights */
    .insight-box {
        background: rgba(16, 185, 129, 0.05);
        border-left: 4px solid #10b981;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 15px;
    }
    .rec-box {
        background: rgba(0, 120, 212, 0.05);
        border-left: 4px solid #0078d4;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Load clean datasets helper
@st.cache_data
def load_data():
    df_fin = pd.read_csv('data/cleaned_financial_metrics.csv')
    df_seg = pd.read_csv('data/cleaned_segment_financials.csv')
    df_stock = pd.read_csv('data/cleaned_stock.csv')
    df_quart = pd.read_csv('data/raw_quarterly_financials.csv')
    return df_fin, df_seg, df_stock, df_quart

try:
    df_fin, df_seg, df_stock, df_quart = load_data()
except Exception as e:
    st.error(f"Error loading datasets: {e}. Please run the data pipelines first.")
    st.stop()

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/color/144/microsoft.png", width=60)
st.sidebar.title("MSFT BI Portal")
st.sidebar.markdown("*Executive Performance & Market Analytics*")
st.sidebar.write("---")

page = st.sidebar.radio("Navigate Dashboard", [
    "Executive Summary",
    "Segment Performance",
    "Cash Flows & CapEx",
    "Stock Price & Moving Averages",
    "Machine Learning Forecasts",
    "Strategic Insights & Recommendations",
    "Interview Preparation Suite",
    "Data Pipeline Audit Center"
])

st.sidebar.write("---")
# Global filter for Year
years_available = sorted(df_fin['Fiscal Year'].unique())
selected_year = st.sidebar.selectbox("Filter Fiscal Year (Global)", years_available, index=len(years_available)-1)

# Helper function to render a custom KPI card
def render_kpi(title, value, delta_text, is_positive=True):
    delta_class = "delta-up" if is_positive else "delta-down"
    delta_symbol = "▲" if is_positive else "▼"
    return f"""
    <div class="kpi-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-delta {delta_class}">{delta_symbol} {delta_text}</div>
    </div>
    """

# ====================================================================
# PAGE 1: EXECUTIVE SUMMARY
# ====================================================================
if page == "Executive Summary":
    st.title("📊 Microsoft Corporation (MSFT) Executive Summary")
    st.write(f"Analyzing audited performance statements for Fiscal Year {selected_year} relative to historical records.")
    
    # Calculate target values
    row_yr = df_fin[df_fin['Fiscal Year'] == selected_year].iloc[0]
    prev_yr_df = df_fin[df_fin['Fiscal Year'] == (selected_year - 1)]
    
    if len(prev_yr_df) > 0:
        row_prev = prev_yr_df.iloc[0]
        rev_growth = ((row_yr['Revenue'] - row_prev['Revenue']) / row_prev['Revenue']) * 100
        ops_growth = ((row_yr['Operating Income'] - row_prev['Operating Income']) / row_prev['Operating Income']) * 100
        net_growth = ((row_yr['Net Income'] - row_prev['Net Income']) / row_prev['Net Income']) * 100
    else:
        rev_growth, ops_growth, net_growth = 0.0, 0.0, 0.0
        
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(render_kpi("Revenue", f"${row_yr['Revenue']:,.0f}M", f"{rev_growth:.2f}% YoY", rev_growth >= 0), unsafe_allow_html=True)
    with col2:
        st.markdown(render_kpi("Operating Income", f"${row_yr['Operating Income']:,.0f}M", f"{ops_growth:.2f}% YoY", ops_growth >= 0), unsafe_allow_html=True)
    with col3:
        st.markdown(render_kpi("Net Profit Margin", f"{row_yr['Net Profit Margin']*100:.2f}%", f"Margin: {row_yr['Net Profit Margin']*100:.1f}%", True), unsafe_allow_html=True)
    with col4:
        st.markdown(render_kpi("Return on Equity (ROE)", f"{row_yr['Return on Equity (ROE)']*100:.2f}%", f"Leverage: {row_yr['Debt to Equity Ratio']:.2f} D/E", True), unsafe_allow_html=True)
        
    st.write("---")
    
    # Charts Row
    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.subheader("Revenue & Net Income Growth Path (FY2020-FY2025)")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_fin['Fiscal Year'], y=df_fin['Revenue'], name="Revenue ($ Millions)", line=dict(color='#0078d4', width=3.5), fill='tozeroy', fillcolor='rgba(0,120,212,0.1)'))
        fig.add_trace(go.Bar(x=df_fin['Fiscal Year'], y=df_fin['Net Income'], name="Net Income ($ Millions)", marker_color='#107c41', opacity=0.85))
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col_right:
        st.subheader("Revenue Contribution by Segment")
        # Sum segments for the selected year
        seg_yr = df_seg[df_seg['Fiscal Year'] == selected_year]
        fig_pie = px.pie(seg_yr, values='Revenue_B', names='Segment', hole=0.45,
                         color_discrete_sequence=['#0078d4', '#107c41', '#f25f22'])
        fig_pie.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.write("---")
    st.subheader("DuPont ROE Analysis & Balance Sheet Ratios")
    st.write("Decomposing shareholder returns into operating efficiency, asset productivity, and financial leverage multipliers.")
    
    # Dupont Table
    dupont_df = df_fin[['Fiscal Year', 'Net Profit Margin', 'Asset Turnover', 'Debt to Equity Ratio', 'Return on Equity (ROE)']].copy()
    dupont_df['Net Profit Margin %'] = np.round(dupont_df['Net Profit Margin'] * 100, 2)
    dupont_df['Return on Equity %'] = np.round(dupont_df['Return on Equity (ROE)'] * 100, 2)
    
    st.table(dupont_df[['Fiscal Year', 'Net Profit Margin %', 'Asset Turnover', 'Debt to Equity Ratio', 'Return on Equity %']])

# ====================================================================
# PAGE 2: SEGMENT PERFORMANCE
# ====================================================================
elif page == "Segment Performance":
    st.title("📊 Segment Profitability & Performance Analysis")
    st.write("Drilling down into the performance metrics of Microsoft's three operating divisions: Intelligent Cloud, Productivity, and More Personal Computing.")
    
    # Pivot tables
    df_seg_pivot_rev = df_seg.pivot(index='Fiscal Year', columns='Segment', values='Revenue_B')
    df_seg_pivot_ops = df_seg.pivot(index='Fiscal Year', columns='Segment', values='Operating_Income_B')
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Segment Revenue Trends ($ Billions)")
        fig_rev = go.Figure()
        for col in df_seg_pivot_rev.columns:
            fig_rev.add_trace(go.Bar(x=df_seg_pivot_rev.index, y=df_seg_pivot_rev[col], name=col))
        fig_rev.update_layout(
            barmode='stack',
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0)
        )
        st.plotly_chart(fig_rev, use_container_width=True)
        
    with col2:
        st.subheader("Segment Operating Income Trends ($ Billions)")
        fig_ops = go.Figure()
        for col in df_seg_pivot_ops.columns:
            fig_ops.add_trace(go.Scatter(x=df_seg_pivot_ops.index, y=df_seg_pivot_ops[col], name=col, mode='lines+markers', line=dict(width=2.5)))
        fig_ops.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0)
        )
        st.plotly_chart(fig_ops, use_container_width=True)
        
    st.write("---")
    st.subheader(f"Detailed Division Metrics for FY {selected_year}")
    seg_detail = df_seg[df_seg['Fiscal Year'] == selected_year][['Segment', 'Revenue_B', 'Operating_Income_B', 'Operating Margin']].copy()
    seg_detail['Operating Margin %'] = np.round(seg_detail['Operating Margin'] * 100, 2)
    st.table(seg_detail[['Segment', 'Revenue_B', 'Operating_Income_B', 'Operating Margin %']])

# ====================================================================
# PAGE 3: CASH FLOWS & CAPEX
# ====================================================================
elif page == "Cash Flows & CapEx":
    st.title("💸 Operating Cash Flow & Capital Outlay Dynamics")
    st.write("Examining Microsoft's CapEx surge to fund AI capacity and its direct impact on Free Cash Flow yields.")
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("Cash flow from Operations vs. Capital Expenditures ($M)")
        fig_capex = go.Figure()
        fig_capex.add_trace(go.Bar(x=df_fin['Fiscal Year'], y=df_fin['Cash from Operations'], name="Cash from Operations", marker_color='#107c41'))
        fig_capex.add_trace(go.Bar(x=df_fin['Fiscal Year'], y=df_fin['Capital Expenditures'], name="Capital Expenditures (CapEx)", marker_color='#ef4444'))
        fig_capex.update_layout(
            barmode='group',
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_capex, use_container_width=True)
        
    with col_r:
        st.subheader("Free Cash Flow Compression & Margin Trend")
        fig_fcf = go.Figure()
        fig_fcf.add_trace(go.Scatter(x=df_fin['Fiscal Year'], y=df_fin['Free Cash Flow'], name="Free Cash Flow ($M)", line=dict(color='#0078d4', width=3)))
        fig_fcf.add_trace(go.Scatter(x=df_fin['Fiscal Year'], y=df_fin['FCF Margin %']*100 if 'FCF Margin %' in df_fin.columns else df_fin['FCF Margin']*100, 
                                     name="FCF Margin %", line=dict(color='#ffb900', width=2), yaxis="y2"))
        fig_fcf.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(title="Free Cash Flow ($M)"),
            yaxis2=dict(title="FCF Margin %", overlaying="y", side="right")
        )
        st.plotly_chart(fig_fcf, use_container_width=True)

    st.write("---")
    st.subheader("Waterfall Analysis: Free Cash Flow Drivers (FY24 to FY25)")
    row_24 = df_fin[df_fin['Fiscal Year'] == 2024].iloc[0]
    row_25 = df_fin[df_fin['Fiscal Year'] == 2025].iloc[0]
    
    # Calculate variances
    ops_var = row_25['Cash from Operations'] - row_24['Cash from Operations']
    capex_var = row_25['Capital Expenditures'] - row_24['Capital Expenditures']
    
    fig_wf = go.Figure(go.Waterfall(
        name="FCF Change",
        orientation="v",
        measure=["relative", "relative", "relative", "total"],
        x=["FY24 FCF", "Operating Cash Flow Growth", "Capital Expenditures Growth", "FY25 FCF"],
        text=[f"${row_24['Free Cash Flow']:,.0f}M", f"+${ops_var:,.0f}M", f"-${capex_var:,.0f}M", f"${row_25['Free Cash Flow']:,.0f}M"],
        y=[row_24['Free Cash Flow'], ops_var, -capex_var, row_25['Free Cash Flow']],
        connector={"line":{"color":"#94a3b8"}}
    ))
    fig_wf.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_wf, use_container_width=True)

# ====================================================================
# PAGE 4: STOCK PRICE & MOVING AVERAGES
# ====================================================================
elif page == "Stock Price & Moving Averages":
    st.title("📈 Stock Price & Moving Average Convergence")
    st.write("Interactive market index modeling for Microsoft Corporation (NASDAQ: MSFT).")
    
    # Slicer for Stock dates
    df_stock['Date'] = pd.to_datetime(df_stock['Date'])
    date_min = df_stock['Date'].min().to_pydatetime()
    date_max = df_stock['Date'].max().to_pydatetime()
    
    start_date, end_date = st.slider("Select Date Range", date_min, date_max, (date_min, date_max))
    df_filtered_stock = df_stock[(df_stock['Date'] >= start_date) & (df_stock['Date'] <= end_date)]
    
    st.subheader("Daily Close Price with 50-day and 200-day Simple Moving Averages")
    fig_stock = go.Figure()
    fig_stock.add_trace(go.Scatter(x=df_filtered_stock['Date'], y=df_filtered_stock['Close'], name="MSFT Close", line=dict(color='#0078d4', width=1.5), opacity=0.7))
    fig_stock.add_trace(go.Scatter(x=df_filtered_stock['Date'], y=df_filtered_stock['Sma_50'], name="50-Day SMA", line=dict(color='#d83b01', width=1.2)))
    fig_stock.add_trace(go.Scatter(x=df_filtered_stock['Date'], y=df_filtered_stock['Sma_200'], name="200-Day SMA", line=dict(color='#107c41', width=1.5)))
    
    fig_stock.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title="Date"),
        yaxis=dict(title="Stock Price ($ USD)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0)
    )
    st.plotly_chart(fig_stock, use_container_width=True)

# ====================================================================
# PAGE 5: MACHINE LEARNING FORECASTS
# ====================================================================
elif page == "Machine Learning Forecasts":
    st.title("🔮 Predictive Financial Modeling")
    st.write("Projecting Microsoft's future performance metrics based on historical time-series regression.")
    
    # We will build a simple linear regression on quarterly revenues
    df_quart['Date_Index'] = df_quart['Fiscal Year'] + df_quart['Quarter'].replace({'Q1':0.0, 'Q2':0.25, 'Q3':0.5, 'Q4':0.75})
    
    X = df_quart[['Date_Index']].values
    y = df_quart['Revenue'].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Forecast future index (next 4 quarters)
    future_dates = np.array([2026.0, 2026.25, 2026.5, 2026.75]).reshape(-1, 1)
    predictions = model.predict(future_dates)
    
    # Calculate residuals and confidence interval (2 standard errors)
    residuals = y - model.predict(X)
    std_err = np.std(residuals)
    ci_slider = st.slider("Select Forecast Uncertainty Bounds (Standard Errors)", 1.0, 3.0, 2.0, step=0.5)
    ci_val = std_err * ci_slider
    
    # Prepare plotting dataframe
    hist_df = pd.DataFrame({'Date_Index': X.flatten(), 'Revenue': y, 'Type': 'Historical'})
    fore_df = pd.DataFrame({'Date_Index': future_dates.flatten(), 'Revenue': predictions, 'Type': 'Forecast'})
    
    fig_fore = go.Figure()
    # Historical Trace
    fig_fore.add_trace(go.Scatter(x=hist_df['Date_Index'], y=hist_df['Revenue'], name="Historical Revenue", mode='lines+markers', line=dict(color='#0078d4')))
    # Forecast Trace
    fig_fore.add_trace(go.Scatter(x=fore_df['Date_Index'], y=fore_df['Revenue'], name="Predicted Revenue", mode='lines+markers', line=dict(color='#ffb900', dash='dash')))
    
    # Confidence bounds
    fig_fore.add_trace(go.Scatter(
        x=np.concatenate([fore_df['Date_Index'], fore_df['Date_Index'][::-1]]),
        y=np.concatenate([fore_df['Revenue'] + ci_val, (fore_df['Revenue'] - ci_val)[::-1]]),
        fill='toself',
        fillcolor='rgba(255, 185, 0, 0.15)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        name="Confidence Interval"
    ))
    
    fig_fore.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title="Fiscal Period (Year.Quarter Decimal)"),
        yaxis=dict(title="Quarterly Revenue ($ Millions)")
    )
    st.plotly_chart(fig_fore, use_container_width=True)
    
    st.write("---")
    st.subheader("Forecasted Quarterly Revenues for FY 2026")
    pred_table = pd.DataFrame({
        'Period': ['FY26 Q1', 'FY26 Q2', 'FY26 Q3', 'FY26 Q4'],
        'Predicted Revenue ($M)': np.round(predictions, 2),
        'Lower Bound ($M)': np.round(predictions - ci_val, 2),
        'Upper Bound ($M)': np.round(predictions + ci_val, 2)
    })
    st.table(pred_table)

# ====================================================================
# PAGE 6: STRATEGIC INSIGHTS & RECOMMENDATIONS
# ====================================================================
elif page == "Strategic Insights & Recommendations":
    st.title("💡 Strategic Insights & Consulting Recommendations")
    
    col_ins, col_recs = st.columns(2)
    
    with col_ins:
        st.header("Corporate Financial Insights")
        st.write("Key takeaways from the analysis of Microsoft's statements (FY20-FY25).")
        
        st.markdown("""
        <div class="insight-box">
            <b>1. Intelligent Cloud Dominance:</b> Segment revenue grew at a 20.6% CAGR, representing 43.9% of corporate sales in FY25. This is Microsoft's primary growth engine.
        </div>
        <div class="insight-box">
            <b>2. AI CapEx Inflation:</b> Capital Expenditures grew at a 33.1% CAGR, peaking at $64.6B in FY25 (a 45% YoY increase) to expand AI server clusters.
        </div>
        <div class="insight-box">
            <b>3. Short-Term FCF Compression:</b> The CapEx surge compressed short-term FCF margins to 25.41% in FY25 (down from 30.17% in FY24).
        </div>
        <div class="insight-box">
            <b>4. Exceptional Asset Return (ROE):</b> Return on Equity remains extremely strong at 29.65% in FY25, driven by expanding net profit margins.
        </div>
        <div class="insight-box">
            <b>5. Strong De-leveraging:</b> Retired $30B in long-term debt, lowering the Debt-to-Equity ratio to 0.12 and securing Microsoft's AAA rating.
        </div>
        """, unsafe_allow_html=True)
        
    with col_recs:
        st.header("Actionable Strategy Roadmap")
        st.write("Strategic advice for Microsoft's executive team.")
        
        st.markdown("""
        <div class="rec-box">
            <b>1. Monitor AI Capacity Utilization (Short-Term):</b> Align data center construction with actual customer Azure GPU demand to prevent capacity oversupply.
        </div>
        <div class="rec-box">
            <b>2. Bundled Copilot Subscriptions (Medium-Term):</b> Drive user monetization by bundling Copilot seats into premium enterprise Office 365 agreements.
        </div>
        <div class="rec-box">
            <b>3. Transition Windows to Cloud SaaS (Medium-Term):</b> Migrate Windows licensing to cloud-based subscriptions (Windows 365) to stabilize the More Personal Computing segment.
        </div>
        <div class="rec-box">
            <b>4. In-House Custom Silicon Development (Long-Term):</b> Expand development of custom Cobalt and Maia chips to bypass expensive Nvidia hardware dependencies.
        </div>
        <div class="rec-box">
            <b>5. Invest in Green Power Networks (Long-Term):</b> Establish direct power purchase contracts with carbon-free utility projects to power scale clusters.
        </div>
        """, unsafe_allow_html=True)

# ====================================================================
# PAGE 7: INTERVIEW PREPARATION SUITE
# ====================================================================
elif page == "Interview Preparation Suite":
    st.title("💼 Professional Job Interview Preparation Guide")
    st.write("Access standard QA modules tailored for Business Intelligence, SQL, and Finance recruiting tracks.")
    
    category = st.selectbox("Choose Question Track", ["General & Project Portfolio", "SQL & Database Coding", "Power BI & DAX", "Business Case & Advisory", "Corporate Finance"])
    
    if category == "General & Project Portfolio":
        st.markdown("""
        **Q: Can you walk me through your Microsoft Financial Analytics project?**  
        *A:* This project is an end-to-end Financial Business Intelligence case study of Microsoft Corporation from FY2020 to FY2025. I ingested real financial data from SEC Form 10-K filings and daily stock price records from Yahoo Finance. I built a Python data cleaning pipeline, conducted exploratory data analysis (EDA), drafted advanced SQL query scripts to perform DuPont ROE analysis and rolling stock indicators, designed a Power BI executive dashboard layout, calculated critical corporate finance ratios, and framed actionable strategic recommendations.
        
        **Q: Why did you choose Microsoft as the subject of this case study?**  
        *A:* Microsoft operates a complex hybrid revenue model encompassing SaaS (Office 365), IaaS/PaaS (Azure), licensing (Windows/SQL Server), hardware (Xbox), and advertising. This creates a rich dataset for analysis. In addition, its recent capital allocation pivot—increasing Capital Expenditures by 45% in FY25 to $64.6B to fund AI infrastructure—provides an excellent real-world scenario for testing financial evaluation methods.
        
        **Q: What were the major data issues you resolved in the cleaning phase?**  
        *A:* In the raw dataset, I handled missing data (imputed a missing Operating Cash Flow value in FY2021 by validating it against the original SEC Form 10-K), corrected negative sign entry errors, resolved segment naming typos (such as standardizing 'Intelligent Cloudd' to 'Intelligent Cloud'), and conducted outlier validation on the CapEx surge.
        """)
        
    elif category == "SQL & Database Coding":
        st.markdown("""
        **Q: What SQL window function did you use to calculate YoY growth?**  
        *A:* I used the `LAG` window function to fetch the previous year's revenue and then computed the percentage change:
        ```sql
        SELECT 
            fiscal_year,
            revenue,
            LAG(revenue) OVER (ORDER BY fiscal_year) AS prev_revenue,
            ((revenue - LAG(revenue) OVER (ORDER BY fiscal_year)) / LAG(revenue) OVER (ORDER BY fiscal_year)) * 100 AS yoy_growth
        FROM annual_financials;
        ```
        
        **Q: How do you write a query to calculate a 50-day moving average of close prices?**  
        *A:* Using the `AVG` window function with the `ROWS BETWEEN` clause:
        ```sql
        SELECT 
            trade_date,
            close_price,
            AVG(close_price) OVER (
                ORDER BY trade_date 
                ROWS BETWEEN 49 PRECEDING AND CURRENT ROW
            ) AS sma_50
        FROM stock_history;
        ```
        """)
        
    elif category == "Power BI & DAX":
        st.markdown("""
        **Q: Write a DAX measure to calculate Year-over-Year (YoY) Revenue Growth %**  
        *A:*
        ```dax
        Revenue_Prior_Year = CALCULATE(SUM(AnnualFinancials[Revenue]), SAMEPERIODLASTYEAR('Calendar'[Date]))

        Revenue_YoY_Growth_Pct = 
        VAR CurrentRev = SUM(AnnualFinancials[Revenue])
        VAR PriorRev = [Revenue_Prior_Year]
        RETURN
        IF(
            ISBLANK(PriorRev) || PriorRev = 0,
            BLANK(),
            DIVIDE(CurrentRev - PriorRev, PriorRev)
        )
        ```
        
        **Q: What is filter context in Power BI, and how is it modified?**  
        *A:* Filter context is the set of filters applied to a visual cell during evaluation (e.g., from row/column headers, slicers, or report filters). It is modified in DAX using the `CALCULATE` function, which can add, remove, or override existing filters.
        """)
        
    elif category == "Business Case & Advisory":
        st.markdown("""
        **Q: Microsoft's Intelligent Cloud segment grew revenue by 17.5% in FY25, but segment operating income grew by 18.0%. What does this tell you about the segment's economics?**  
        *A:* This indicates positive operating leverage. Because operating income grew faster than revenue, the operating margin expanded (from 35.86% to 36.02%). This suggests that Microsoft is successfully scaling its infrastructure, spreading fixed costs (data centers, fiber networks) over a larger base of revenue.
        
        **Q: If Microsoft increases its CapEx to $64.6B in FY25, what is the short-term and long-term impact on the balance sheet?**  
        *A:* Short-term, cash balances decrease or debt increases. Property, Plant, and Equipment (PP&E) assets increase, and short-term liabilities may rise. Long-term, accumulated depreciation will increase, dragging down net asset values. If these assets generate high-margin cloud revenue, profit margins will rise. If not, the heavy depreciation will drag down ROA and operating margins.
        """)
        
    elif category == "Corporate Finance":
        st.markdown("""
        **Q: What is the current ROE of Microsoft in FY25, and how do you interpret it?**  
        *A:*
        $$\\text{ROE} = \\frac{\\text{Net Income}}{\\text{Common Equity}} = \\frac{\\$101,832\\text{M}}{\\$343,479\\text{M}} = 29.65\\%$$
        This means Microsoft generates 29.65 cents of profit for every dollar of shareholder equity, reflecting excellent capital allocation.
        
        **Q: What is Microsoft's Debt-to-Equity ratio in FY25?**  
        *A:*
        $$\\text{Debt-to-Equity} = \\frac{\\text{Total Debt}}{\\text{Common Equity}} = \\frac{\\$41,200\\text{M}}{\\$343,479\\text{M}} = 0.12$$
        This indicates a highly conservative capital structure, with debt representing just 12% of equity.
        """)

# ====================================================================
# PAGE 8: DATA PIPELINE AUD CENTER
# ====================================================================
elif page == "Data Pipeline Audit Center":
    st.title("⚙️ Data Cleaning & Processing Center")
    st.write("This audit center details the operations of the Python data pipeline that cleans and standardizes the SEC financials and stock history.")
    
    st.subheader("Pipeline Logs & Transformation Audits")
    st.code("""
>>> Running data cleaning pipeline...
[Imputation] Imputed Cash from Operations for FY2021: 76740.0 million via Exact SEC lookup
[Correction] Corrected negative Total Liabilities for FY2023: -205753 -> 205753 million
Saved cleaned financials to data/cleaned_financial_metrics.csv
Saved cleaned segments to data/cleaned_segment_financials.csv
Saved cleaned stock history to data/cleaned_stock.csv
Data Cleaning & Preprocessing Complete.
    """, language="python")
    
    st.write("---")
    st.subheader("Raw Variable Values vs. Cleaned Dataset Visualizer")
    
    show_cleaned = st.checkbox("Show Cleaned annual statement dataset", value=True)
    if show_cleaned:
        st.dataframe(df_fin)
    else:
        # Load raw from data folder
        df_raw_ann = pd.read_csv('data/raw_annual_financials.csv')
        st.dataframe(df_raw_ann)
