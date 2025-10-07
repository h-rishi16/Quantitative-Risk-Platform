# User Guide

## Getting Started

This guide will help you get started with the Quantitative Risk Modeling Platform for calculating portfolio risk metrics using Monte Carlo simulations.

## Overview

The Risk Modeling Platform provides two main interfaces:
1. **Web Interface** (Streamlit) - User-friendly dashboard for interactive analysis
2. **API Interface** (FastAPI) - Programmatic access for developers and integration

## Web Interface Guide

### 1. Accessing the Platform

Open your web browser and navigate to:
- **Local Development**: http://localhost:8501
- **Production**: https://your-domain.com

### 2. Navigation

The platform has four main pages accessible via the sidebar:

#### Portfolio Overview
- High-level portfolio metrics and performance indicators
- Key statistics and trend visualizations

#### Risk Dashboard  
- Comprehensive risk metrics display
- VaR calculations and risk indicators

#### Monte Carlo Simulation
- **Main workflow for risk analysis**
- File upload and parameter configuration
- Results visualization and analysis

#### API Testing
- Direct API endpoint testing
- Sample requests and responses

### 3. Monte Carlo Simulation Workflow

This is the core functionality for calculating portfolio risk metrics.

#### Step 1: Prepare Your Data

You need two CSV files:

**Portfolio Weights CSV** (`portfolio_weights.csv`):
```csv
asset,weight
AAPL,0.40
GOOGL,0.30
MSFT,0.30
```

Requirements:
- Must have `asset` and `weight` columns
- Weights must sum to 1.0 (100%)
- Asset names should match the historical returns file

**Historical Returns CSV** (`historical_returns.csv`):
```csv
date,AAPL,GOOGL,MSFT
2024-01-01,0.015,-0.008,0.012
2024-01-02,-0.012,0.025,0.008
2024-01-03,0.008,0.015,-0.005
```

Requirements:
- Must have a `date` column
- Asset columns should match portfolio weights
- Returns should be in decimal format (0.01 = 1%)
- Minimum 30 observations recommended

#### Step 2: Upload Files

1. Navigate to the **Monte Carlo Simulation** page
2. Use the file upload widgets to select your CSV files
3. The system will validate your files and show:
   - SUCCESS: File loaded successfully
   - WARNING: Validation warnings (if any)
   - ERROR: Errors that need fixing

#### Step 3: Configure Parameters

Set your simulation parameters:

- **Number of Simulations**: 1,000 to 100,000
  - More simulations = higher accuracy but longer computation time
  - Recommended: 10,000 for most use cases

- **Time Horizon**: 1 to 365 days
  - 1 day = daily VaR
  - 10 days = 10-day VaR (common for regulatory reporting)

- **Confidence Levels**: Select multiple levels
  - 95% = 1-in-20 worst case
  - 99% = 1-in-100 worst case
  - 99.9% = 1-in-1000 worst case

#### Step 4: Run Simulation

1. Click **"Run Monte Carlo VaR"**
2. Wait for the calculation to complete (progress bar shown)
3. Results will appear automatically below

#### Step 5: Interpret Results

**VaR Metrics:**
- **Value at Risk (VaR)**: Maximum expected loss at given confidence level
- **Conditional VaR (CVaR)**: Average loss beyond the VaR threshold
- **Dollar Values**: Absolute portfolio loss amounts

**Portfolio Statistics:**
- **Mean Return**: Expected daily return
- **Volatility**: Standard deviation of returns
- **Skewness**: Asymmetry of return distribution
- **Kurtosis**: Tail thickness of return distribution

**Visualization:**
- Interactive histogram showing return distribution
- VaR thresholds marked on the chart
- Zoom and pan capabilities

### 4. Sample Data

If you don't have your own data, use the sample data provided:

1. Click **"📥 Download Sample Portfolio"** 
2. Click **"📥 Download Sample Returns"**
3. Upload both files to test the system

## Common Use Cases

### Daily Risk Monitoring
- Time Horizon: 1 day
- Confidence Levels: 95%, 99%
- Simulations: 10,000

### Regulatory Reporting
- Time Horizon: 10 days  
- Confidence Levels: 99%
- Simulations: 25,000+

### Stress Testing
- Time Horizon: 21 days (1 month)
- Confidence Levels: 99%, 99.9%
- Simulations: 50,000+

## Troubleshooting

### File Upload Issues

**"Weights don't sum to 1.0"**
- Check that portfolio weights add up to exactly 1.0
- Round to appropriate decimal places

**"Missing return data for assets"**
- Ensure all portfolio assets have columns in returns file
- Check spelling and case sensitivity

**"Invalid date format"**
- Use YYYY-MM-DD format for dates
- Ensure dates are in chronological order

### Calculation Issues

**"API Connection Error"**
- Verify backend server is running
- Check if API status shows "SUCCESS: API Online"

**"Calculation timeout"**
- Reduce number of simulations
- Check for extremely large datasets

### Performance Tips

**Faster Calculations:**
- Use fewer simulations for initial testing
- Reduce time horizon for quicker results

**Better Accuracy:**
- Use more historical data (1+ years recommended)
- Increase simulation count for final analysis
- Ensure data quality and completeness

## Best Practices

### Data Quality
- Use daily return data for at least 1 year
- Handle missing data appropriately
- Check for outliers and data errors
- Use consistent data sources

### Parameter Selection
- Match time horizon to your use case
- Start with 10,000 simulations, increase if needed
- Use multiple confidence levels for comprehensive analysis

### Result Interpretation
- Compare results across different time periods
- Validate against other risk models
- Consider market conditions and portfolio composition
- Document assumptions and methodology

## Getting Help

- Check the **API Testing** page for technical details
- Review error messages for specific guidance
- Consult the API documentation for programmatic usage
- Submit issues on GitHub for bugs or feature requests