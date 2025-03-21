import streamlit as st
import requests
import plotly.express as px
import pandas as pd
import random

# --------------------------------------------------
# CONFIGURATION & CONSTANTS
# --------------------------------------------------
# Flask API URL for stock data and news (ensure your Flask API is running)
API_BASE_URL = "http://localhost:5000"

st.set_page_config(page_title="Financial Analysis Dashboard", layout="wide")

# --------------------------------------------------
# TAB LAYOUT: Stock Analysis & Financial Forecasting
# --------------------------------------------------
tabs = st.tabs(["Stock Analysis & News", "Financial Forecasting Report"])

# --------------------------------------------------
# TAB 1: Stock Analysis & News
# --------------------------------------------------
with tabs[0]:
    st.title("📈 Financial Analysis Dashboard")
    
    # Sidebar: Stock Analysis input
    st.sidebar.header("Stock Analysis")
    stock_symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, TSLA)", "")
    
    if stock_symbol:
        with st.spinner("Fetching stock data..."):
            response = requests.get(f"{API_BASE_URL}/stock", params={"symbol": stock_symbol})
            if response.status_code == 200:
                stock_data = pd.DataFrame(response.json())
                if not stock_data.empty:
                    st.subheader(f"Stock Data for {stock_symbol}")
                    st.dataframe(stock_data)
                    
                    # Plot closing prices
                    fig = px.line(stock_data, x=stock_data.index, y="Close", title=f"{stock_symbol} Closing Prices")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error("No data available for the given stock symbol.")
            else:
                st.error("Failed to fetch stock data. Please check the symbol and try again.")
    
    # Sidebar: Financial News
    st.sidebar.header("Latest Financial News")
    if st.sidebar.button("Get News"):
        with st.spinner("Fetching latest news..."):
            news_response = requests.get(f"{API_BASE_URL}/news")
            if news_response.status_code == 200:
                news = news_response.json().get("latest_news", [])
                if news:
                    st.subheader("📰 Latest Financial News")
                    for idx, headline in enumerate(news, start=1):
                        st.write(f"{idx}. {headline}")
                else:
                    st.info("No recent financial news available.")
            else:
                st.error("Failed to fetch financial news.")
    
    st.sidebar.markdown("---")
    st.sidebar.info("Built with ❤️ using Streamlit & Flask")

# --------------------------------------------------
# TAB 2: Financial Forecasting Report
# --------------------------------------------------
with tabs[1]:
    st.title("Financial Analysis & Forecasting Report")
    
    # Input: Industry Focus
    industry_options = ["Technology", "Healthcare", "Manufacturing", "Finance", "Retail"]
    industry_focus = st.selectbox("Industry Focus", industry_options)
    
    # Input: Financial Metrics to Analyze
    metrics_options = ["Revenue Growth", "Profit Margins", "Cash Flow", "Market Cap", "P/E Ratio"]
    selected_metrics = st.multiselect("Financial Metrics to Analyze", metrics_options, 
                                      default=["Revenue Growth", "Profit Margins"])
    
    # Input: Market Conditions
    market_condition = st.text_input("Market Conditions (e.g., Inflation Rate, Interest Rate, Geopolitical Factors)")
    
    # Input: Investment Goals
    investment_goals = ["Short-term Gains", "Long-term Stability", "Risk Management"]
    investment_goal = st.selectbox("Investment Goals", investment_goals)
    
    # Input: Time Frame
    time_frame_options = ["Quarterly", "Annual", "5-Year Outlook"]
    time_frame = st.selectbox("Time Frame", time_frame_options)
    
    # --------------------------------------------------
    # BACKEND LOGIC FOR FORECASTING
    # --------------------------------------------------
    def generate_forecast(industry, metrics, market_condition, investment_goal, time_frame):
        """
        Generates a detailed mock forecast report using the provided inputs.
        Replace this placeholder logic with real generative AI interactions if needed.
        """
        forecast_data = {
            "Industry": industry,
            "Analyzed Metrics": metrics,
            "Market Condition": market_condition,
            "Investment Goal": investment_goal,
            "Time Frame": time_frame,
            "Forecast Growth Rate (%)": round(random.uniform(3.0, 15.0), 2),
            "Risk Level": random.choice(["Low", "Moderate", "High"]),
            "Market Trend Analysis": f"In the {industry} sector, current trends show moderate growth driven by key factors including innovation and regulatory shifts.",
            "Company Financial Projection": f"Based on selected metrics, the company's financials project stable revenue growth with improving profit margins over the {time_frame.lower()} period.",
            "Investment Strategy Recommendations": f"To achieve {investment_goal.lower()}, a diversified approach is recommended that leverages sector-specific strengths in {industry}.",
            "Model Critique": "The report provides coherent insights with clear financial terminology. However, integration with real-time data and further prompt refinement would enhance actionable recommendations."
        }
        return forecast_data

    def analyze_industry(industry):
        """
        Returns industry-specific insights.
        """
        industry_insights = {
            "Technology": "High innovation, rapid change, and potential volatility characterize the tech sector.",
            "Healthcare": "Steady growth, regulatory oversight, and high demand for services define the healthcare industry.",
            "Manufacturing": "Capital-intensive with cyclical demand, manufacturing trends are influenced by global supply chains.",
            "Finance": "Highly sensitive to interest rates and economic cycles, the finance sector is dynamic and regulated.",
            "Retail": "Driven by consumer spending and market trends, the retail sector faces both growth opportunities and challenges."
        }
        return industry_insights.get(industry, "No insights available.")

    def analyze_metrics(metrics):
        """
        Provides a summary analysis for each selected financial metric.
        """
        metric_summaries = {
            "Revenue Growth": "Measures how quickly a company's sales are growing.",
            "Profit Margins": "Indicates profitability relative to revenue.",
            "Cash Flow": "Reflects liquidity and the company's ability to fund operations.",
            "Market Cap": "Represents the company's overall market value.",
            "P/E Ratio": "Evaluates the company's share price relative to its earnings."
        }
        results = {}
        for m in metrics:
            results[m] = metric_summaries.get(m, "No data available.")
        return results

    # --------------------------------------------------
    # FINANCIAL FORECASTING: GENERATE REPORT
    # --------------------------------------------------
    if st.button("Generate Forecast"):
        # Analyze inputs and generate forecast
        industry_insight = analyze_industry(industry_focus)
        metric_analysis = analyze_metrics(selected_metrics)
        forecast_result = generate_forecast(
            industry=industry_focus,
            metrics=selected_metrics,
            market_condition=market_condition,
            investment_goal=investment_goal,
            time_frame=time_frame
        )
        
        # Build the formatted report as a Markdown string
        report = f"""
# AI-Generated Financial Forecasting and Analysis Report

**Industry Focus:** {forecast_result.get("Industry", "N/A")}  
**Investment Goal:** {forecast_result.get("Investment Goal", "N/A")}  
**Time Frame:** {forecast_result.get("Time Frame", "N/A")}  

---

## Selected Metrics Analysis:
"""
        for metric, description in metric_analysis.items():
            report += f"- **{metric}:** {description}\n"
    
        report += f"""

---

## Forecast Results:
- **Forecast Growth Rate (%):** {forecast_result.get("Forecast Growth Rate (%)", "N/A")}%  
- **Risk Level:** {forecast_result.get("Risk Level", "N/A")}  
- **Market Condition:** {forecast_result.get("Market Condition", "N/A")}  

### Detailed Analysis:
- **Market Trend Analysis:**  
  {forecast_result.get("Market Trend Analysis", "N/A")}
  
- **Company Financial Projection:**  
  {forecast_result.get("Company Financial Projection", "N/A")}
  
- **Investment Strategy Recommendations:**  
  {forecast_result.get("Investment Strategy Recommendations", "N/A")}

---

## Model Critique:
{forecast_result.get("Model Critique", "N/A")}

---
"""
        # Display the generated report
        st.subheader("Financial Analysis Report")
        st.markdown(report)
        
        # Download button for the report as a Markdown file
        st.download_button(label="Download Report", data=report, file_name="financial_analysis_report.md", mime="text/markdown")
    
    # --------------------------------------------------
    # Display Refined Prompts for Financial Analysis
    # --------------------------------------------------
    st.markdown("## Refined Prompts for Financial Forecasting and Analysis")
    
    refined_prompts = {
        "Market Trend Analysis Prompt": (
            "Generate a detailed market trend analysis report for the healthcare sector, focusing on current inflation rates, "
            "geopolitical factors, and regulatory changes over the next quarter. Provide actionable insights and risk assessments."
        ),
        "Company-Specific Financial Projection Prompt": (
            "Produce a comprehensive financial projection report for a mid-sized healthcare company, highlighting revenue growth, "
            "profit margins, and cash flow trends on an annual basis. Include recommendations for achieving long-term stability."
        ),
        "Investment Strategy Recommendations Prompt": (
            "Create an investment strategy report for the healthcare industry, targeting short-term gains. Evaluate market conditions "
            "and provide actionable recommendations for risk management and portfolio diversification over a 5-year outlook."
        )
    }
    
    for title, prompt in refined_prompts.items():
        st.markdown(f"**{title}:**")
        st.code(prompt, language="text")
