"""
Data processing utilities for portfolio and returns data
"""

import logging
from io import StringIO
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class DataProcessor:
    """Handles data validation and processing for portfolio analysis"""

    def __init__(self):
        self.portfolio_weights = None
        self.historical_returns = None
        self.assets = None

    def validate_portfolio_weights(self, df: pd.DataFrame) -> bool:
        """Validate portfolio weights CSV format"""
        try:
            # Check required columns
            required_cols = ["asset", "weight"]
            if not all(col in df.columns for col in required_cols):
                logger.error(
                    f"Missing required columns. Expected: {required_cols}, Got: {list(df.columns)}"
                )
                return False

            # Check weights are numeric and sum to ~1.0
            if not pd.api.types.is_numeric_dtype(df["weight"]):
                logger.error("Weight column must be numeric")
                return False

            weight_sum = df["weight"].sum()
            if not (0.95 <= weight_sum <= 1.05):  # Allow small rounding errors
                logger.error(f"Portfolio weights must sum to 1.0, got {weight_sum:.4f}")
                return False

            # Check for negative weights
            if (df["weight"] < 0).any():
                logger.error("Portfolio weights cannot be negative")
                return False

            logger.info(
                f"Portfolio weights validated: {len(df)} assets, sum={weight_sum:.4f}"
            )
            return True

        except Exception as e:
            logger.error(f"Error validating portfolio weights: {e}")
            return False

    def validate_historical_returns(
        self, df: pd.DataFrame, portfolio_assets: List[str]
    ) -> bool:
        """Validate historical returns CSV format"""
        try:
            # Check for date column
            if "date" not in df.columns:
                logger.error("Historical returns must have a 'date' column")
                return False

            # Check that portfolio assets are present
            missing_assets = set(portfolio_assets) - set(df.columns)
            if missing_assets:
                logger.error(f"Missing return data for assets: {missing_assets}")
                return False

            # Validate returns are numeric
            for asset in portfolio_assets:
                if not pd.api.types.is_numeric_dtype(df[asset]):
                    logger.error(f"Returns for {asset} must be numeric")
                    return False

            # Check for sufficient data points
            if len(df) < 30:
                logger.warning(
                    f"Limited historical data: {len(df)} observations. Recommend at least 30."
                )

            logger.info(
                f"Historical returns validated: {len(df)} observations for {len(portfolio_assets)} assets"
            )
            return True

        except Exception as e:
            logger.error(f"Error validating historical returns: {e}")
            return False

    def load_portfolio_weights(self, csv_content: str) -> Optional[pd.DataFrame]:
        """Load and validate portfolio weights from CSV content"""
        try:
            df = pd.read_csv(StringIO(csv_content))

            if self.validate_portfolio_weights(df):
                # Normalize weights to ensure they sum to exactly 1.0
                df["weight"] = df["weight"] / df["weight"].sum()
                self.portfolio_weights = df
                self.assets = df["asset"].tolist()
                return df
            else:
                return None

        except Exception as e:
            logger.error(f"Error loading portfolio weights: {e}")
            return None

    def load_historical_returns(self, csv_content: str) -> Optional[pd.DataFrame]:
        """Load and validate historical returns from CSV content"""
        try:
            df = pd.read_csv(StringIO(csv_content))

            # Convert date column
            df["date"] = pd.to_datetime(df["date"])

            if self.assets and self.validate_historical_returns(df, self.assets):
                self.historical_returns = df
                return df
            else:
                return None

        except Exception as e:
            logger.error(f"Error loading historical returns: {e}")
            return None

    def get_portfolio_data(self) -> Optional[Dict]:
        """Get processed portfolio data for risk calculations"""
        if self.portfolio_weights is None or self.historical_returns is None:
            logger.error("Both portfolio weights and historical returns must be loaded")
            return None

        try:
            # Extract returns matrix
            returns_matrix = self.historical_returns[self.assets].values
            weights_array = (
                self.portfolio_weights.set_index("asset")
                .loc[self.assets]["weight"]
                .values
            )

            # Calculate portfolio statistics
            asset_returns = {}
            asset_volatilities = {}

            for i, asset in enumerate(self.assets):
                returns = returns_matrix[:, i]
                asset_returns[asset] = np.mean(returns) * 252  # Annualize
                asset_volatilities[asset] = np.std(returns) * np.sqrt(252)  # Annualize

            # Calculate correlation matrix
            correlation_matrix = np.corrcoef(returns_matrix.T)

            return {
                "assets": self.assets,
                "weights": weights_array,
                "returns_matrix": returns_matrix,
                "expected_returns": asset_returns,
                "volatilities": asset_volatilities,
                "correlation_matrix": correlation_matrix,
                "num_observations": len(self.historical_returns),
            }

        except Exception as e:
            logger.error(f"Error processing portfolio data: {e}")
            return None

    def calculate_portfolio_statistics(self) -> Dict:
        """Calculate basic portfolio statistics"""
        data = self.get_portfolio_data()
        if not data:
            return {}

        try:
            weights = data["weights"]
            returns_matrix = data["returns_matrix"]
            correlation_matrix = data["correlation_matrix"]

            # Portfolio return time series
            portfolio_returns = np.dot(returns_matrix, weights)

            # Portfolio statistics
            portfolio_mean = np.mean(portfolio_returns) * 252  # Annualized
            portfolio_vol = np.std(portfolio_returns) * np.sqrt(252)  # Annualized

            # Sharpe ratio (assuming 0% risk-free rate)
            sharpe_ratio = portfolio_mean / portfolio_vol if portfolio_vol > 0 else 0

            # Maximum drawdown
            cumulative_returns = np.cumprod(1 + portfolio_returns)
            rolling_max = np.maximum.accumulate(cumulative_returns)
            drawdowns = (cumulative_returns - rolling_max) / rolling_max
            max_drawdown = np.min(drawdowns)

            return {
                "portfolio_return": portfolio_mean,
                "portfolio_volatility": portfolio_vol,
                "sharpe_ratio": sharpe_ratio,
                "max_drawdown": max_drawdown,
                "num_assets": len(self.assets),
                "observation_period": len(portfolio_returns),
                "correlation_range": [
                    correlation_matrix.min(),
                    correlation_matrix.max(),
                ],
                "portfolio_returns_series": portfolio_returns,
            }

        except Exception as e:
            logger.error(f"Error calculating portfolio statistics: {e}")
            return {}


# Utility functions
def create_sample_data():
    """Create sample data for testing"""
    # Sample portfolio weights
    portfolio_data = {
        "asset": ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"],
        "weight": [0.25, 0.20, 0.20, 0.15, 0.20],
    }

    # Sample historical returns (50 days)
    np.random.seed(42)
    dates = pd.date_range("2024-01-01", periods=50, freq="D")

    returns_data = {"date": dates}
    for asset in portfolio_data["asset"]:
        # Generate correlated returns
        returns_data[asset] = np.random.normal(0.001, 0.02, 50)  # Daily returns

    portfolio_df = pd.DataFrame(portfolio_data)
    returns_df = pd.DataFrame(returns_data)

    return portfolio_df, returns_df


def validate_api_request(request_data: Dict) -> Tuple[bool, str]:
    """Validate API request data"""
    required_fields = ["weights", "historical_returns", "assets"]

    for field in required_fields:
        if field not in request_data:
            return False, f"Missing required field: {field}"

    # Additional validations
    weights = request_data["weights"]
    if not isinstance(weights, list) or len(weights) == 0:
        return False, "Weights must be a non-empty list"

    if not np.isclose(sum(weights), 1.0, rtol=0.01):
        return False, f"Weights must sum to 1.0, got {sum(weights):.4f}"

    returns = request_data["historical_returns"]
    if not isinstance(returns, list) or len(returns) == 0:
        return False, "Historical returns must be a non-empty list"

    return True, "Valid"


# Example usage
if __name__ == "__main__":
    # Test data processing
    processor = DataProcessor()

    # Create sample data
    portfolio_df, returns_df = create_sample_data()

    print("Sample Portfolio:")
    print(portfolio_df)
    print(f"\nPortfolio weights sum: {portfolio_df['weight'].sum():.4f}")

    print("\nSample Returns (first 5 rows):")
    print(returns_df.head())

    # Test loading from CSV strings
    portfolio_csv = portfolio_df.to_csv(index=False)
    returns_csv = returns_df.to_csv(index=False)

    if processor.load_portfolio_weights(portfolio_csv):
        print("\n✅ Portfolio weights loaded successfully")

        if processor.load_historical_returns(returns_csv):
            print("✅ Historical returns loaded successfully")

            # Get portfolio data
            portfolio_data = processor.get_portfolio_data()
            if portfolio_data:
                print(f"\n📊 Portfolio Analysis:")
                print(f"Assets: {portfolio_data['assets']}")
                print(f"Weights: {portfolio_data['weights']}")
                print(f"Observations: {portfolio_data['num_observations']}")

                # Calculate statistics
                stats = processor.calculate_portfolio_statistics()
                if stats:
                    print(f"\n📈 Portfolio Statistics:")
                    print(f"Expected Return: {stats['portfolio_return']:.2%}")
                    print(f"Volatility: {stats['portfolio_volatility']:.2%}")
                    print(f"Sharpe Ratio: {stats['sharpe_ratio']:.3f}")
                    print(f"Max Drawdown: {stats['max_drawdown']:.2%}")
            else:
                print("❌ Failed to process portfolio data")
        else:
            print("❌ Failed to load historical returns")
    else:
        print("❌ Failed to load portfolio weights")
