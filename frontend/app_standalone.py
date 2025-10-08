"""
Standalone Streamlit Frontend Application for Risk Modeling Platform
No backend required - all calculations done client-side
"""

import json
import time
from typing import Dict, List
import sys
import os

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Add backend to path for importing risk engines
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    from risk_engines.monte_carlo import MonteCarloVaR, SimulationConfig
    from data_processing.data_processor import DataProcessor
    BACKEND_AVAILABLE = True
except ImportError:
    BACKEND_AVAILABLE = False
    st.warning("Backend risk engines not available. Using simplified calculations.")

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
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 0.75rem;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
</style>
""",
    unsafe_allow_html=True,
)

def simple_monte_carlo_var(returns_data, weights, confidence_levels=[0.95, 0.99], num_simulations=10000):
    """
    Simplified Monte Carlo VaR calculation without backend dependencies
    """
    # Convert to numpy arrays
    returns_array = np.array(returns_data)
    weights_array = np.array(weights)
    
    # Calculate portfolio returns
    portfolio_returns = np.dot(returns_array, weights_array)
    
    # Calculate statistics
    mean_return = np.mean(portfolio_returns)
    std_return = np.std(portfolio_returns)
    
    # Monte Carlo simulation using normal distribution
    np.random.seed(42)  # For reproducibility
    simulated_returns = np.random.normal(mean_return, std_return, num_simulations)
    
    # Calculate VaR and CVaR
    results = {}
    for conf_level in confidence_levels:
        var_percentile = (1 - conf_level) * 100
        var_value = np.percentile(simulated_returns, var_percentile)
        cvar_value = np.mean(simulated_returns[simulated_returns <= var_value])
        
        results[conf_level] = {
            'var': var_value,
            'cvar': cvar_value,
            'var_dollar': var_value * 1000000,  # Assume $1M portfolio
            'cvar_dollar': cvar_value * 1000000
        }
    
    return {
        'results': results,
        'portfolio_stats': {
            'mean': mean_return,
            'std': std_return,
            'simulations': num_simulations,
            'min': np.min(simulated_returns),
            'max': np.max(simulated_returns)
        },
        'simulated_returns': simulated_returns
    }

def portfolio_overview():
    """Portfolio Overview Page"""
    st.header("📊 Portfolio Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Sample Portfolio")
        sample_data = pd.DataFrame({
            'Asset': ['AAPL', 'GOOGL', 'MSFT', 'TSLA'],
            'Weight': [0.3, 0.25, 0.25, 0.2],
            'Expected Return': [0.12, 0.15, 0.10, 0.20],
            'Volatility': [0.25, 0.30, 0.22, 0.45]
        })
        st.dataframe(sample_data, use_container_width=True)
        
    with col2:
        st.subheader("Portfolio Allocation")
        fig = px.pie(sample_data, values='Weight', names='Asset', 
                    title="Portfolio Weights")
        st.plotly_chart(fig, use_container_width=True)

def risk_dashboard():
    """Risk Dashboard Page"""
    st.header("⚡ Risk Dashboard")
    
    # Risk metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Portfolio VaR (95%)", "-$45,231", delta="-2.3%")
    with col2:
        st.metric("Portfolio CVaR (95%)", "-$52,890", delta="-2.8%")
    with col3:
        st.metric("Sharpe Ratio", "1.25", delta="0.15")
    with col4:
        st.metric("Max Drawdown", "-8.5%", delta="1.2%")
    
    # Risk decomposition
    st.subheader("Risk Decomposition")
    risk_contrib = pd.DataFrame({
        'Asset': ['AAPL', 'GOOGL', 'MSFT', 'TSLA'],
        'Risk Contribution': [0.35, 0.28, 0.22, 0.15],
        'Weight': [0.3, 0.25, 0.25, 0.2]
    })
    
    fig = px.bar(risk_contrib, x='Asset', y='Risk Contribution',
                title="Risk Contribution by Asset")
    st.plotly_chart(fig, use_container_width=True)

def monte_carlo_simulation():
    """Monte Carlo Simulation Page"""
    st.header("🎲 Monte Carlo VaR Simulation")
    
    # Input parameters
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Simulation Parameters")
        num_simulations = st.slider("Number of Simulations", 1000, 100000, 10000, step=1000)
        confidence_levels = st.multiselect(
            "Confidence Levels", 
            [0.90, 0.95, 0.99, 0.999], 
            default=[0.95, 0.99]
        )
        
    with col2:
        st.subheader("Portfolio Configuration")
        
        # Simple portfolio input
        assets = ['AAPL', 'GOOGL', 'MSFT', 'TSLA']
        weights = []
        
        for asset in assets:
            weight = st.slider(f"{asset} Weight", 0.0, 1.0, 0.25, 0.05)
            weights.append(weight)
        
        # Normalize weights
        total_weight = sum(weights)
        if total_weight > 0:
            weights = [w/total_weight for w in weights]
            st.info(f"Weights normalized to sum to 1.0")
    
    # Sample historical returns (simplified)
    if st.button("Run Monte Carlo Simulation", type="primary"):
        with st.spinner("Running simulation..."):
            # Generate sample returns data
            np.random.seed(42)
            n_days = 252  # One year of trading days
            returns_data = np.random.normal(0.001, 0.02, (n_days, len(assets)))  # Daily returns
            
            # Add some correlation structure
            correlation_matrix = np.array([
                [1.0, 0.7, 0.6, 0.4],
                [0.7, 1.0, 0.5, 0.3],
                [0.6, 0.5, 1.0, 0.5],
                [0.4, 0.3, 0.5, 1.0]
            ])
            
            # Apply correlation (simplified)
            L = np.linalg.cholesky(correlation_matrix)
            correlated_returns = np.dot(returns_data, L.T)
            
            # Run simulation
            results = simple_monte_carlo_var(
                correlated_returns, weights, confidence_levels, num_simulations
            )
            
            # Display results
            st.success("Simulation completed!")
            
            # VaR Results
            st.subheader("📈 VaR Results")
            results_df = []
            for conf_level, result in results['results'].items():
                results_df.append({
                    'Confidence Level': f"{conf_level:.1%}",
                    'VaR (%)': f"{result['var']:.4f}",
                    'CVaR (%)': f"{result['cvar']:.4f}",
                    'VaR ($1M Portfolio)': f"${result['var_dollar']:,.0f}",
                    'CVaR ($1M Portfolio)': f"${result['cvar_dollar']:,.0f}"
                })
            
            st.dataframe(pd.DataFrame(results_df), use_container_width=True)
            
            # Portfolio Statistics
            st.subheader("📊 Portfolio Statistics")
            stats = results['portfolio_stats']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Mean Return", f"{stats['mean']:.4f}")
                st.metric("Volatility", f"{stats['std']:.4f}")
            with col2:
                st.metric("Min Return", f"{stats['min']:.4f}")
                st.metric("Max Return", f"{stats['max']:.4f}")
            with col3:
                st.metric("Simulations", f"{stats['simulations']:,}")
            
            # Distribution plot
            st.subheader("📈 Return Distribution")
            fig = px.histogram(
                x=results['simulated_returns'],
                nbins=50,
                title="Simulated Portfolio Returns Distribution"
            )
            
            # Add VaR lines
            for conf_level, result in results['results'].items():
                fig.add_vline(
                    x=result['var'], 
                    line_dash="dash", 
                    line_color="red",
                    annotation_text=f"VaR {conf_level:.1%}"
                )
            
            st.plotly_chart(fig, use_container_width=True)

def file_upload_analysis():
    """File Upload and Analysis"""
    st.header("📁 Upload Your Data")
    
    st.info("Upload your portfolio data (CSV format) for custom risk analysis")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("File uploaded successfully!")
            
            st.subheader("Data Preview")
            st.dataframe(df.head(), use_container_width=True)
            
            st.subheader("Data Summary")
            st.write(df.describe())
            
            if st.button("Analyze Risk"):
                st.info("Risk analysis would be performed here with uploaded data")
                
        except Exception as e:
            st.error(f"Error reading file: {e}")

def main():
    """Main application"""
    st.markdown(
        '<h1 class="main-header">Quantitative Risk Modeling Platform</h1>',
        unsafe_allow_html=True,
    )
    
    # Status indicator
    st.success("✅ Standalone Mode - No backend required!")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    st.sidebar.info("Standalone Risk Platform")

    page = st.sidebar.selectbox(
        "Select Page",
        [
            "Portfolio Overview",
            "Risk Dashboard", 
            "Monte Carlo Simulation",
            "Upload Data"
        ],
    )

    if page == "Portfolio Overview":
        portfolio_overview()
    elif page == "Risk Dashboard":
        risk_dashboard()
    elif page == "Monte Carlo Simulation":
        monte_carlo_simulation()
    elif page == "Upload Data":
        file_upload_analysis()

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Quantitative Risk Platform**")
    st.sidebar.markdown("Built with Streamlit")

if __name__ == "__main__":
    main()