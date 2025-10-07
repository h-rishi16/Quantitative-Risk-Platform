"""
Monte Carlo Value at Risk (VaR) Implementation
==============================================

This module implements Monte Carlo simulation for Value at Risk calculation,
a key risk metric used in quantitative finance and banking.

Mathematical Foundation:
- Uses Geometric Brownian Motion: dS_t = μS_t dt + σS_t dW_t
- Simulates portfolio returns over specified time horizon
- Calculates VaR at various confidence levels (95%, 99%, 99.9%)

Features:
- Multiple stochastic processes support
- Correlation handling for multi-asset portfolios
- Conditional VaR (Expected Shortfall) calculation
- Stress testing capabilities
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import warnings
from scipy import stats
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StochasticProcess(Enum):
    """Supported stochastic processes for simulation"""

    GEOMETRIC_BROWNIAN_MOTION = "gbm"
    MEAN_REVERSION = "mean_reversion"
    JUMP_DIFFUSION = "jump_diffusion"


@dataclass
class AssetParameters:
    """Parameters for individual asset simulation"""

    symbol: str
    current_price: float
    expected_return: float  # Annual expected return (μ)
    volatility: float  # Annual volatility (σ)
    weight: float  # Portfolio weight

    def __post_init__(self):
        """Validate parameters"""
        if self.volatility < 0:
            raise ValueError(f"Volatility must be non-negative for {self.symbol}")
        if not 0 <= self.weight <= 1:
            raise ValueError(f"Weight must be between 0 and 1 for {self.symbol}")


@dataclass
class SimulationConfig:
    """Configuration for Monte Carlo simulation"""

    num_simulations: int = 10000
    time_horizon: int = 252  # Trading days (1 year)
    confidence_levels: List[float] = None
    random_seed: Optional[int] = None

    def __post_init__(self):
        if self.confidence_levels is None:
            self.confidence_levels = [0.95, 0.99, 0.999]

        # Validate confidence levels
        for cl in self.confidence_levels:
            if not 0 < cl < 1:
                raise ValueError(f"Confidence level {cl} must be between 0 and 1")


@dataclass
class VaRResults:
    """Results from VaR calculation"""

    var_estimates: Dict[float, float]  # confidence_level: VaR value
    cvar_estimates: Dict[float, float]  # confidence_level: CVaR value
    portfolio_returns: np.ndarray
    percentiles: Dict[float, float]
    statistics: Dict[str, float]


class MonteCarloVaR:
    """
    Monte Carlo Value at Risk Calculator

    Implements Monte Carlo simulation for portfolio risk assessment using
    various stochastic processes. Supports multi-asset portfolios with
    correlation structure. Can work with either AssetParameters or raw data.
    """

    def __init__(
        self,
        assets: Optional[List[AssetParameters]] = None,
        correlation_matrix: Optional[np.ndarray] = None,
    ):
        """
        Initialize Monte Carlo VaR calculator

        Args:
            assets: List of asset parameters (optional if using from_data method)
            correlation_matrix: Correlation matrix between assets (optional)
        """
        if assets is not None:
            self.assets = assets
            self.num_assets = len(assets)

            # Validate and set correlation matrix
            if correlation_matrix is not None:
                self._validate_correlation_matrix(correlation_matrix)
                self.correlation_matrix = correlation_matrix
            else:
                # Use identity matrix (no correlation)
                self.correlation_matrix = np.eye(self.num_assets)

            # Validate portfolio weights sum to 1
            total_weight = sum(asset.weight for asset in assets)
            if not np.isclose(total_weight, 1.0, rtol=1e-5):
                raise ValueError(
                    f"Portfolio weights must sum to 1.0, got {total_weight}"
                )

            logger.info(f"Initialized Monte Carlo VaR for {self.num_assets} assets")
        else:
            # Will be initialized later with from_data method
            self.assets = None
            self.num_assets = 0
            self.correlation_matrix = None

    @classmethod
    def from_data(
        cls,
        asset_names: List[str],
        weights: np.ndarray,
        expected_returns: np.ndarray,
        volatilities: np.ndarray,
        correlation_matrix: np.ndarray,
    ):
        """
        Create MonteCarloVaR instance from raw data arrays

        Args:
            asset_names: List of asset names
            weights: Portfolio weights array
            expected_returns: Expected returns array (annualized)
            volatilities: Volatility array (annualized)
            correlation_matrix: Asset correlation matrix
        """
        # Create AssetParameters from raw data
        assets = []
        for i, name in enumerate(asset_names):
            assets.append(
                AssetParameters(
                    symbol=name,
                    current_price=100.0,  # Dummy price, not used in calculations
                    expected_return=expected_returns[i],
                    volatility=volatilities[i],
                    weight=weights[i],
                )
            )

        instance = cls(assets, correlation_matrix)
        return instance

    @classmethod
    def from_historical_data(
        cls,
        asset_names: List[str],
        weights: np.ndarray,
        returns_matrix: np.ndarray,
        correlation_matrix: Optional[np.ndarray] = None,
    ):
        """
        Create MonteCarloVaR instance from historical returns data

        Args:
            asset_names: List of asset names
            weights: Portfolio weights array
            returns_matrix: Historical returns matrix (observations x assets)
            correlation_matrix: Correlation matrix (computed if not provided)
        """
        # Calculate statistics from historical data
        expected_returns = np.mean(returns_matrix, axis=0) * 252  # Annualize
        volatilities = np.std(returns_matrix, axis=0) * np.sqrt(252)  # Annualize

        if correlation_matrix is None:
            correlation_matrix = np.corrcoef(returns_matrix.T)

        return cls.from_data(
            asset_names, weights, expected_returns, volatilities, correlation_matrix
        )

    def _validate_correlation_matrix(self, corr_matrix: np.ndarray) -> None:
        """Validate correlation matrix properties"""
        if corr_matrix.shape != (self.num_assets, self.num_assets):
            raise ValueError(
                f"Correlation matrix shape {corr_matrix.shape} doesn't match number of assets {self.num_assets}"
            )

        if not np.allclose(corr_matrix, corr_matrix.T):
            raise ValueError("Correlation matrix must be symmetric")

        eigenvals = np.linalg.eigvals(corr_matrix)
        if np.any(eigenvals < -1e-8):
            raise ValueError("Correlation matrix must be positive semi-definite")

        if not np.allclose(np.diag(corr_matrix), 1.0):
            raise ValueError("Correlation matrix diagonal elements must be 1.0")

    def simulate_portfolio_returns(
        self,
        config: SimulationConfig,
        process: StochasticProcess = StochasticProcess.GEOMETRIC_BROWNIAN_MOTION,
    ) -> np.ndarray:
        """
        Simulate portfolio returns using Monte Carlo method

        Args:
            config: Simulation configuration
            process: Stochastic process to use

        Returns:
            Array of simulated portfolio returns
        """
        if config.random_seed is not None:
            np.random.seed(config.random_seed)

        logger.info(f"Starting simulation with {config.num_simulations:,} paths")

        # Time step
        dt = 1.0 / config.time_horizon

        # Generate correlated random numbers
        random_numbers = self._generate_correlated_randoms(
            config.num_simulations, config.time_horizon
        )

        # Simulate each asset
        portfolio_returns = np.zeros(config.num_simulations)

        for i, asset in enumerate(self.assets):
            if process == StochasticProcess.GEOMETRIC_BROWNIAN_MOTION:
                asset_returns = self._simulate_gbm(
                    asset, random_numbers[i], dt, config.time_horizon
                )
            elif process == StochasticProcess.MEAN_REVERSION:
                asset_returns = self._simulate_mean_reversion(
                    asset, random_numbers[i], dt, config.time_horizon
                )
            else:
                raise NotImplementedError(f"Process {process} not implemented")

            # Add weighted asset returns to portfolio
            portfolio_returns += asset.weight * asset_returns

        logger.info("Portfolio simulation completed")
        return portfolio_returns

    def _generate_correlated_randoms(
        self, num_sims: int, time_horizon: int
    ) -> np.ndarray:
        """Generate correlated random numbers using Cholesky decomposition"""
        # Cholesky decomposition for correlation
        try:
            chol_matrix = np.linalg.cholesky(self.correlation_matrix)
        except np.linalg.LinAlgError:
            # If Cholesky fails, use eigenvalue decomposition
            eigenvals, eigenvecs = np.linalg.eigh(self.correlation_matrix)
            eigenvals = np.maximum(eigenvals, 1e-8)  # Ensure positive eigenvalues
            chol_matrix = eigenvecs @ np.diag(np.sqrt(eigenvals))

        # Generate independent random numbers
        independent_randoms = np.random.normal(
            0, 1, (self.num_assets, num_sims, time_horizon)
        )

        # Apply correlation structure
        correlated_randoms = np.zeros_like(independent_randoms)
        for sim in range(num_sims):
            for t in range(time_horizon):
                correlated_randoms[:, sim, t] = (
                    chol_matrix @ independent_randoms[:, sim, t]
                )

        return correlated_randoms

    def _simulate_gbm(
        self, asset: AssetParameters, randoms: np.ndarray, dt: float, time_horizon: int
    ) -> np.ndarray:
        """
        Simulate asset returns using Geometric Brownian Motion

        dS_t = μS_t dt + σS_t dW_t

        Solution: S_t = S_0 * exp((μ - σ²/2)t + σW_t)
        """
        num_sims = randoms.shape[0]

        # GBM parameters
        drift = asset.expected_return - 0.5 * asset.volatility**2

        # Cumulative random walks
        cumulative_randoms = np.cumsum(randoms * np.sqrt(dt), axis=1)

        # Final asset prices
        final_prices = asset.current_price * np.exp(
            drift * (time_horizon * dt) + asset.volatility * cumulative_randoms[:, -1]
        )

        # Calculate returns
        returns = (final_prices - asset.current_price) / asset.current_price

        return returns

    def _simulate_mean_reversion(
        self, asset: AssetParameters, randoms: np.ndarray, dt: float, time_horizon: int
    ) -> np.ndarray:
        """
        Simulate asset returns using Ornstein-Uhlenbeck mean reversion process

        dX_t = θ(μ - X_t)dt + σdW_t
        """
        # Mean reversion parameters (simplified)
        theta = 0.5  # Mean reversion speed
        mu = asset.expected_return  # Long-term mean

        num_sims = randoms.shape[0]
        prices = np.full(num_sims, asset.current_price)

        for t in range(time_horizon):
            log_prices = np.log(prices)
            d_log_prices = theta * (
                np.log(asset.current_price) + mu - log_prices
            ) * dt + asset.volatility * randoms[:, t] * np.sqrt(dt)
            prices *= np.exp(d_log_prices)

        returns = (prices - asset.current_price) / asset.current_price
        return returns

    def calculate_var(self, config: SimulationConfig, **kwargs) -> VaRResults:
        """
        Calculate Value at Risk using Monte Carlo simulation

        Args:
            config: Simulation configuration
            **kwargs: Additional parameters for simulation

        Returns:
            VaRResults object containing VaR estimates and statistics
        """
        # Simulate portfolio returns
        portfolio_returns = self.simulate_portfolio_returns(config, **kwargs)

        # Calculate VaR for each confidence level
        var_estimates = {}
        cvar_estimates = {}
        percentiles = {}

        for confidence_level in config.confidence_levels:
            # VaR is the negative of the percentile (loss perspective)
            percentile = (1 - confidence_level) * 100
            var_value = -np.percentile(portfolio_returns, percentile)
            var_estimates[confidence_level] = var_value
            percentiles[confidence_level] = percentile

            # Conditional VaR (Expected Shortfall)
            # Average of returns worse than VaR
            tail_returns = portfolio_returns[portfolio_returns <= -var_value]
            if len(tail_returns) > 0:
                cvar_estimates[confidence_level] = -np.mean(tail_returns)
            else:
                cvar_estimates[confidence_level] = var_value

        # Calculate portfolio statistics
        statistics = {
            "mean_return": np.mean(portfolio_returns),
            "std_return": np.std(portfolio_returns),
            "skewness": stats.skew(portfolio_returns),
            "kurtosis": stats.kurtosis(portfolio_returns),
            "min_return": np.min(portfolio_returns),
            "max_return": np.max(portfolio_returns),
            "num_simulations": config.num_simulations,
        }

        logger.info(
            f"VaR calculation completed for {len(config.confidence_levels)} confidence levels"
        )

        return VaRResults(
            var_estimates=var_estimates,
            cvar_estimates=cvar_estimates,
            portfolio_returns=portfolio_returns,
            percentiles=percentiles,
            statistics=statistics,
        )

    def stress_test(
        self, stress_scenarios: Dict[str, Dict[str, float]], config: SimulationConfig
    ) -> Dict[str, VaRResults]:
        """
        Perform stress testing by modifying asset parameters

        Args:
            stress_scenarios: Dictionary of scenario_name -> {parameter: multiplier}
            config: Simulation configuration

        Returns:
            Dictionary of scenario results
        """
        results = {}
        original_assets = [asset for asset in self.assets]  # Copy original parameters

        for scenario_name, modifications in stress_scenarios.items():
            logger.info(f"Running stress test scenario: {scenario_name}")

            # Apply stress modifications
            for i, asset in enumerate(self.assets):
                if "volatility_multiplier" in modifications:
                    asset.volatility *= modifications["volatility_multiplier"]
                if "return_shift" in modifications:
                    asset.expected_return += modifications["return_shift"]

            # Calculate VaR under stress
            results[scenario_name] = self.calculate_var(config)

            # Restore original parameters
            self.assets = [asset for asset in original_assets]

        return results

    def generate_report(
        self, results: VaRResults, portfolio_value: float = 1000000
    ) -> str:
        """
        Generate a comprehensive VaR report

        Args:
            results: VaR calculation results
            portfolio_value: Total portfolio value for absolute VaR calculation

        Returns:
            Formatted report string
        """
        report = []
        report.append("=" * 60)
        report.append("MONTE CARLO VALUE AT RISK REPORT")
        report.append("=" * 60)
        report.append("")

        # Portfolio composition
        report.append("Portfolio Composition:")
        report.append("-" * 25)
        for asset in self.assets:
            report.append(
                f"{asset.symbol}: {asset.weight:.1%} (μ={asset.expected_return:.2%}, σ={asset.volatility:.2%})"
            )
        report.append("")

        # Portfolio statistics
        stats = results.statistics
        report.append("Portfolio Statistics:")
        report.append("-" * 25)
        report.append(f"Expected Return: {stats['mean_return']:.4f}")
        report.append(f"Volatility: {stats['std_return']:.4f}")
        report.append(f"Skewness: {stats['skewness']:.4f}")
        report.append(f"Kurtosis: {stats['kurtosis']:.4f}")
        report.append(f"Simulations: {stats['num_simulations']:,}")
        report.append("")

        # VaR estimates
        report.append("Value at Risk Estimates:")
        report.append("-" * 30)
        report.append(
            f"{'Confidence':<12} {'VaR (%)':<10} {'VaR ($)':<15} {'CVaR (%)':<10} {'CVaR ($)':<15}"
        )
        report.append("-" * 65)

        for conf_level in sorted(results.var_estimates.keys()):
            var_pct = results.var_estimates[conf_level]
            cvar_pct = results.cvar_estimates[conf_level]
            var_dollar = var_pct * portfolio_value
            cvar_dollar = cvar_pct * portfolio_value

            report.append(
                f"{conf_level:.1%}        {var_pct:.4f}    ${var_dollar:>12,.0f}   {cvar_pct:.4f}    ${cvar_dollar:>12,.0f}"
            )

        report.append("")
        report.append("Notes:")
        report.append(
            "- VaR represents the maximum expected loss at given confidence level"
        )
        report.append(
            "- CVaR (Conditional VaR) represents the expected loss beyond VaR threshold"
        )
        report.append("- All values assume normal market conditions")

        return "\n".join(report)


# Example usage and testing
if __name__ == "__main__":
    # Example portfolio setup
    assets = [
        AssetParameters("AAPL", 150.0, 0.12, 0.25, 0.4),  # Apple
        AssetParameters("GOOGL", 2500.0, 0.15, 0.30, 0.3),  # Google
        AssetParameters("MSFT", 300.0, 0.10, 0.22, 0.3),  # Microsoft
    ]

    # Correlation matrix (example)
    correlation_matrix = np.array(
        [
            [1.0, 0.6, 0.7],  # AAPL correlations
            [0.6, 1.0, 0.5],  # GOOGL correlations
            [0.7, 0.5, 1.0],  # MSFT correlations
        ]
    )

    # Initialize VaR calculator
    mc_var = MonteCarloVaR(assets, correlation_matrix)

    # Simulation configuration
    config = SimulationConfig(
        num_simulations=50000,
        time_horizon=252,  # 1 year
        confidence_levels=[0.95, 0.99, 0.999],
        random_seed=42,
    )

    # Calculate VaR
    print("Calculating Monte Carlo VaR...")
    results = mc_var.calculate_var(config)

    # Generate and print report
    report = mc_var.generate_report(results, portfolio_value=10_000_000)
    print(report)

    # Stress testing example
    stress_scenarios = {
        "Market Crash": {"volatility_multiplier": 2.0, "return_shift": -0.10},
        "High Volatility": {"volatility_multiplier": 1.5},
    }

    print("\n" + "=" * 60)
    print("STRESS TESTING RESULTS")
    print("=" * 60)

    stress_results = mc_var.stress_test(stress_scenarios, config)
    for scenario, result in stress_results.items():
        print(f"\nScenario: {scenario}")
        print(f"99% VaR: {result.var_estimates[0.99]:.4f}")
        print(f"99% CVaR: {result.cvar_estimates[0.99]:.4f}")
