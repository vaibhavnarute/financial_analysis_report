import streamlit as st
import pandas as pd
import random
import json

#########################
# BACKEND LOGIC SECTION #
#########################

def generate_forecast(industry, metrics, market_condition, investment_goal, time_frame):
    """
    Placeholder function that uses user inputs to produce a mock forecast.
    Replace this with real forecasting or analysis logic.
    """
    forecast_data = {
        "Industry": industry,
        "Analyzed Metrics": metrics,
        "Market Condition": market_condition,
        "Investment Goal": investment_goal,
        "Time Frame": time_frame,
        "Forecast Growth Rate (%)": round(random.uniform(3.0, 15.0), 2),
        "Risk Level": random.choice(["Low", "Moderate", "High"])
    }
    return forecast_data

def analyze_industry(industry):
    """
    Placeholder function to fetch or analyze industry data.
    In a real app, you'd pull data from a database or an API.
    """
    industry_insights = {
        "Technology": "High innovation, but also high volatility",
        "Healthcare": "Steady growth, regulated environment",
        "Manufacturing": "Capital intensive, cyclical demand",
        "Finance": "Sensitive to interest rates & regulations",
        "Retail": "Consumer-driven, heavily influenced by market trends"
    }
    return industry_insights.get(industry, "No insights available")

def analyze_metrics(metrics):
    """
    Placeholder function to show how you'd analyze selected financial metrics.
    """
    metric_summaries = {
        "Revenue Growth": "Measures how quickly a company's sales are growing",
        "Profit Margins": "Shows profitability relative to revenue",
        "Cash Flow": "Indicates liquidity & operational health",
        "Market Cap": "Represents the company's valuation on the stock market",
        "P/E Ratio": "Price-to-Earnings, used to gauge valuation"
    }
    results = {}
    for m in metrics:
        results[m] = metric_summaries.get(m, "No data")
    return results

#########################
# FRONTEND (STREAMLIT)  #
#########################

st.title("Financial Analysis & Forecasting Tool")

# Industry Focus
industry_options = ["Technology", "Healthcare", "Manufacturing", "Finance", "Retail"]
industry_focus = st.selectbox("Industry Focus", industry_options)

# Financial Metrics to Analyze
metrics = ["Revenue Growth", "Profit Margins", "Cash Flow", "Market Cap", "P/E Ratio"]
selected_metrics = st.multiselect("Financial Metrics to Analyze", metrics, default=["Revenue Growth", "Profit Margins"])

# Market Conditions
market_condition = st.text_input("Market Conditions (e.g., Inflation Rate, Interest Rate)")

# Investment Goals
investment_goals = ["Short-term Gains", "Long-term Stability", "Risk Management"]
investment_goal = st.selectbox("Investment Goals", investment_goals)

# Time Frame
time_frame_options = ["Quarterly", "Annual", "5-Year Outlook"]
time_frame = st.selectbox("Time Frame", time_frame_options)

# Generate Forecast Button
if st.button("Generate Forecast"):
    # 1. Analyze industry
    industry_insight = analyze_industry(industry_focus)
    
    # 2. Analyze selected metrics
    metric_analysis = analyze_metrics(selected_metrics)
    
    # 3. Generate forecast based on user inputs
    forecast_result = generate_forecast(
        industry=industry_focus,
        metrics=selected_metrics,
        market_condition=market_condition,
        investment_goal=investment_goal,
        time_frame=time_frame
    )
    
    # Display JSON outputs (optional)
    st.subheader("Industry Insight")
    st.write(industry_insight)
    
    st.subheader("Selected Metrics Analysis")
    st.json(metric_analysis)
    
    st.subheader("Forecast Results")
    st.json(forecast_result)
    
    st.success("Forecast Generated Successfully!")
    
    # Build the formatted report as a markdown string
    report = f"""
# Financial Analysis Report

**Industry:** {forecast_result.get("Industry", "N/A")}  
**Investment Goal:** {forecast_result.get("Investment Goal", "N/A")}  
**Time Frame:** {forecast_result.get("Time Frame", "N/A")}  

---

## Selected Metrics Analysis:
"""
    for metric, description in metric_analysis.items():
        report += f"- **{metric}:** {description}\n"

    report += f"""

## Forecast Results:
- **Forecast Growth Rate (%):** {forecast_result.get("Forecast Growth Rate (%)", "N/A")}%  
- **Risk Level:** {forecast_result.get("Risk Level", "N/A")}  
- **Market Condition:** {forecast_result.get("Market Condition", "N/A")}

---
    """
    
    st.markdown(report)
