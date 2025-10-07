"""
Streamlit Frontend Application for Risk Modeling Platform with File Upload
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List
import requests
import json
import time

# Configure page
st.set_page_config(
    page_title="Quantitative Risk Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .risk-high { border-left-color: #ff4444; }
    .risk-medium { border-left-color: #ffaa00; }
    .risk-low { border-left-color: #44ff44; }
</style>
""",
    unsafe_allow_html=True,
)


def check_api_status():
    """Check if the backend API is running"""
    try:
        response = requests.get("http://localhost:8002/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def main():
    """Main application"""
    st.markdown(
        '<h1 class="main-header">🏦 Quantitative Risk Modeling Platform</h1>',
        unsafe_allow_html=True,
    )

    # API Status indicator
    api_status = check_api_status()
    if api_status:
        st.success("🟢 Backend API Connected")
    else:
        st.error("🔴 Backend API Disconnected - Please start the backend server")

    # Sidebar navigation
    st.sidebar.title("Navigation")

    # Show API status in sidebar too
    if api_status:
        st.sidebar.success("🟢 API Online")
    else:
        st.sidebar.error("🔴 API Offline")

    page = st.sidebar.selectbox(
        "Select Page",
        [
            "Portfolio Overview",
            "Risk Dashboard",
            "Monte Carlo Simulation",
            "API Testing",
        ],
    )

    if page == "Portfolio Overview":
        portfolio_overview()
    elif page == "Risk Dashboard":
        risk_dashboard()
    elif page == "Monte Carlo Simulation":
        monte_carlo_simulation()
    elif page == "API Testing":
        api_testing()


def portfolio_overview():
    """Portfolio overview page"""
    st.header("📈 Portfolio Overview")

    # Sample portfolio data
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Portfolio Value", "$10,000,000", "2.5%")
    with col2:
        st.metric("Daily P&L", "$45,230", "0.45%")
    with col3:
        st.metric("YTD Return", "12.8%", "2.1%")
    with col4:
        st.metric("Volatility", "18.5%", "-1.2%")


def risk_dashboard():
    """Risk metrics dashboard"""
    st.header("⚠️ Risk Dashboard")

    # VaR metrics
    st.subheader("Value at Risk Metrics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("95% VaR", "$234,500", "-$12,300")
    with col2:
        st.metric("99% VaR", "$456,700", "-$23,100")
    with col3:
        st.metric("99.9% VaR", "$678,900", "-$34,500")


def monte_carlo_simulation():
    """Monte Carlo simulation page with file upload and real API integration"""
    st.header("🎲 Monte Carlo Simulation")

    st.markdown(
        """
    Upload your portfolio data and run Monte Carlo simulations to estimate portfolio risk metrics.
    
    **Required Files:**
    1. **Portfolio Weights CSV**: `asset,weight` (weights must sum to 1.0)
    2. **Historical Returns CSV**: `date,asset1,asset2,...` (daily returns data)
    """
    )

    # File upload section
    st.subheader("📁 Upload Portfolio Data")

    # Create two columns for file uploads
    upload_col1, upload_col2 = st.columns(2)

    with upload_col1:
        st.markdown("**Portfolio Weights CSV**")
        portfolio_file = st.file_uploader(
            "Choose portfolio weights file",
            type=["csv"],
            key="portfolio_upload",
            help="CSV file with columns: asset, weight",
        )

        if portfolio_file:
            try:
                portfolio_df = pd.read_csv(portfolio_file)
                st.success(f"✅ Loaded {len(portfolio_df)} assets")
                st.dataframe(portfolio_df, use_container_width=True)

                # Validate weights
                weight_sum = portfolio_df["weight"].sum()
                if abs(weight_sum - 1.0) > 0.01:
                    st.warning(f"⚠️ Weights sum to {weight_sum:.3f}, should be 1.0")
                else:
                    st.success(f"✅ Weights sum to {weight_sum:.3f}")

            except Exception as e:
                st.error(f"❌ Error loading portfolio file: {e}")
                portfolio_file = None

    with upload_col2:
        st.markdown("**Historical Returns CSV**")
        returns_file = st.file_uploader(
            "Choose historical returns file",
            type=["csv"],
            key="returns_upload",
            help="CSV file with date column and asset return columns",
        )

        if returns_file:
            try:
                returns_df = pd.read_csv(returns_file)
                st.success(f"✅ Loaded {len(returns_df)} observations")

                # Show preview
                st.markdown("**Preview (first 5 rows):**")
                st.dataframe(returns_df.head(), use_container_width=True)

                # Validate data compatibility
                if portfolio_file:
                    portfolio_assets = set(portfolio_df["asset"].tolist())
                    returns_assets = set(returns_df.columns.tolist()) - {"date"}

                    missing_assets = portfolio_assets - returns_assets
                    if missing_assets:
                        st.error(f"❌ Missing return data for: {missing_assets}")
                    else:
                        st.success("✅ All portfolio assets have return data")

            except Exception as e:
                st.error(f"❌ Error loading returns file: {e}")
                returns_file = None

    # Download sample data section
    st.subheader("📋 Sample Data")
    sample_col1, sample_col2 = st.columns(2)

    with sample_col1:
        sample_portfolio = """asset,weight
AAPL,0.40
GOOGL,0.30
MSFT,0.30"""
        st.download_button(
            label="📥 Download Sample Portfolio",
            data=sample_portfolio,
            file_name="portfolio_weights.csv",
            mime="text/csv",
            help="Download sample portfolio weights CSV",
        )

    with sample_col2:
        # Get sample returns data
        try:
            with open(
                "/Users/hrishi/Projects/Risk Model/sample_data/historical_returns.csv",
                "r",
            ) as f:
                sample_returns = f.read()
            st.download_button(
                label="📥 Download Sample Returns",
                data=sample_returns,
                file_name="historical_returns.csv",
                mime="text/csv",
                help="Download sample historical returns CSV",
            )
        except:
            st.button("📥 Sample Returns (unavailable)", disabled=True)

    # Only show simulation parameters if files are uploaded
    if portfolio_file and returns_file:
        st.subheader("⚙️ Simulation Parameters")

        # Simulation parameters section
        col1, col2 = st.columns([1, 2])

        with col1:
            num_simulations = st.number_input(
                "Number of Simulations",
                min_value=1000,
                max_value=100000,
                value=10000,
                step=1000,
            )
            time_horizon = st.number_input(
                "Time Horizon (days)", min_value=1, max_value=365, value=1
            )
            confidence_levels = st.multiselect(
                "Confidence Levels", [0.90, 0.95, 0.99, 0.999], default=[0.95, 0.99]
            )

            if st.button(
                "🚀 Run Monte Carlo VaR", type="primary", use_container_width=True
            ):
                if confidence_levels:
                    run_monte_carlo_simulation(
                        portfolio_df,
                        returns_df,
                        num_simulations,
                        time_horizon,
                        confidence_levels,
                    )
                else:
                    st.warning("Please select at least one confidence level.")

        with col2:
            display_simulation_results()

    else:
        st.info(
            "📁 Please upload both portfolio weights and historical returns files to proceed."
        )


def run_monte_carlo_simulation(
    portfolio_df, returns_df, num_simulations, time_horizon, confidence_levels
):
    """Run the Monte Carlo simulation via API"""
    # Show progress
    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        status_text.text("Preparing data for API call...")
        progress_bar.progress(25)

        # Prepare data for API call
        assets = portfolio_df["asset"].tolist()
        weights = portfolio_df["weight"].tolist()

        # Convert returns data to matrix format
        returns_matrix = returns_df[assets].values.tolist()

        # API request payload
        api_data = {
            "assets": assets,
            "weights": weights,
            "historical_returns": returns_matrix,
            "confidence_levels": confidence_levels,
            "num_simulations": num_simulations,
            "time_horizon": time_horizon,
        }

        status_text.text("Calling Monte Carlo API...")
        progress_bar.progress(50)

        # Call the API
        api_url = "http://localhost:8002/monte_carlo_var"
        response = requests.post(api_url, json=api_data, timeout=60)

        progress_bar.progress(75)
        status_text.text("Processing results...")

        if response.status_code == 200:
            results = response.json()
            progress_bar.progress(100)
            status_text.text("✅ Monte Carlo simulation completed!")

            # Store results in session state
            st.session_state["var_results"] = results
            st.rerun()

        else:
            st.error(f"API Error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        st.error(
            f"Connection Error: Could not connect to API. Make sure the backend is running.\nError: {str(e)}"
        )
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
    finally:
        progress_bar.empty()
        status_text.empty()


def display_simulation_results():
    """Display Monte Carlo simulation results"""
    if "var_results" in st.session_state:
        results = st.session_state["var_results"]

        st.subheader("🎯 VaR Results")

        # Display VaR metrics
        for var_result in results["var_results"]:
            conf = var_result["confidence_level"]
            col_var, col_cvar = st.columns(2)

            with col_var:
                st.metric(
                    f"{conf:.0%} VaR",
                    f"{var_result['var_value']:.4f}",
                    delta=f"${var_result['var_dollar']:,.0f}",
                )
            with col_cvar:
                st.metric(
                    f"{conf:.0%} CVaR",
                    f"{var_result['cvar_value']:.4f}",
                    delta=f"${var_result['cvar_dollar']:,.0f}",
                )

        # Portfolio Statistics
        st.subheader("📈 Portfolio Statistics")
        stats = results["portfolio_statistics"]

        col1_stats, col2_stats, col3_stats, col4_stats = st.columns(4)
        with col1_stats:
            st.metric("Mean Return", f"{stats['mean_return']:.4f}")
        with col2_stats:
            st.metric("Volatility", f"{stats['std_return']:.4f}")
        with col3_stats:
            st.metric("Skewness", f"{stats['skewness']:.3f}")
        with col4_stats:
            st.metric("Kurtosis", f"{stats['kurtosis']:.3f}")

        # Visualization
        st.subheader("📊 Return Distribution")

        # Generate distribution for visualization
        np.random.seed(42)
        simulated_returns = np.random.normal(
            stats["mean_return"], stats["std_return"], 10000
        )

        fig = go.Figure()
        fig.add_trace(
            go.Histogram(
                x=simulated_returns, nbinsx=50, name="Portfolio Returns", opacity=0.7
            )
        )

        # Add VaR lines
        for var_result in results["var_results"]:
            conf = var_result["confidence_level"]
            var_val = -var_result["var_value"]
            fig.add_vline(
                x=var_val,
                line_dash="dash",
                line_color="red" if conf == 0.95 else "darkred",
                annotation_text=f"{conf:.0%} VaR",
            )

        fig.update_layout(
            title="Monte Carlo Return Distribution (Live Results from Uploaded Data)",
            xaxis_title="Portfolio Returns",
            yaxis_title="Frequency",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Show raw results in expander
        with st.expander("🔍 View Raw API Response"):
            st.json(results)

    else:
        st.info("👆 Upload your data and run the simulation to see results here!")


def api_testing():
    """API testing page for advanced users"""
    st.header("🔧 API Testing")

    st.markdown(
        """
    Test the backend API endpoints directly. This page is useful for developers and advanced users
    who want to integrate with the API programmatically.
    """
    )

    # API endpoint testing
    st.subheader("📡 API Endpoints")

    # Health check
    if st.button("Test Health Endpoint"):
        try:
            response = requests.get("http://localhost:8002/health")
            if response.status_code == 200:
                st.success("✅ API Health Check Passed")
                st.json(response.json())
            else:
                st.error(f"❌ Health check failed: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Connection error: {e}")

    # Sample data endpoint
    if st.button("Get Sample Data"):
        try:
            response = requests.get("http://localhost:8002/sample_data")
            if response.status_code == 200:
                st.success("✅ Sample data retrieved")
                data = response.json()
                st.json(data)
            else:
                st.error(f"❌ Failed to get sample data: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Connection error: {e}")

    # JSON API test
    st.subheader("🧪 Test Monte Carlo API with JSON")

    sample_json = {
        "assets": ["AAPL", "GOOGL", "MSFT"],
        "weights": [0.4, 0.3, 0.3],
        "historical_returns": [
            [0.01, -0.005, 0.008],
            [-0.012, 0.02, 0.005],
            [0.008, 0.015, -0.003],
        ],
        "confidence_levels": [0.95, 0.99],
        "num_simulations": 1000,
        "time_horizon": 1,
    }

    if st.button("🚀 Test with Sample JSON"):
        try:
            response = requests.post(
                "http://localhost:8002/monte_carlo_var", json=sample_json, timeout=30
            )
            if response.status_code == 200:
                st.success("✅ Monte Carlo API test successful")
                st.json(response.json())
            else:
                st.error(f"❌ API test failed: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"❌ API test error: {e}")

    # Show sample JSON
    st.subheader("📋 Sample JSON Request")
    st.code(json.dumps(sample_json, indent=2), language="json")


if __name__ == "__main__":
    main()
