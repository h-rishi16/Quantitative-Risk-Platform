# Git Commit Message Templates

# Use these templates as examples for professional commit messages

# ==========================================
# FEATURE COMMITS
# ==========================================

# New API endpoint
feat(api): add portfolio risk metrics endpoint

Implement comprehensive risk calculation endpoint that accepts
portfolio data and returns VaR, CVaR, and correlation metrics.

- Add input validation for portfolio weights
- Implement Monte Carlo simulation
- Include confidence interval calculations
- Return JSON response with risk metrics

Closes #123

# New frontend feature
feat(frontend): implement real-time risk dashboard

Add interactive dashboard displaying live portfolio risk metrics
with automatic refresh every 30 seconds.

- Real-time chart updates using WebSocket connection
- Responsive design for mobile and desktop
- Export functionality for risk reports

# New risk model
feat(models): integrate GARCH volatility forecasting

Add GARCH(1,1) model for improved volatility predictions in
VaR calculations, reducing forecast errors by 15%.

# ==========================================
# BUG FIXES
# ==========================================

# API bug fix
fix(api): resolve memory leak in Monte Carlo simulations

Fixed memory allocation issue that caused server crashes
during large portfolio calculations with >10,000 simulations.

Fixes #456

# Frontend bug fix
fix(frontend): correct chart rendering for negative returns

Plotly charts now properly display negative portfolio returns
without axis scaling issues.

# Model bug fix
fix(models): handle singular covariance matrices

Add regularization to prevent numerical errors when
correlation matrix is not positive definite.

# ==========================================
# DOCUMENTATION
# ==========================================

# API documentation
docs(api): update endpoint documentation with examples

- Add request/response examples for all endpoints
- Include error code descriptions
- Update authentication section

# General documentation
docs: improve setup instructions for development environment

Add detailed steps for setting up virtual environment,
installing dependencies, and running tests locally.

# Mathematical documentation
docs(models): add mathematical formulations for VaR calculations

Include LaTeX formulas and derivations for Monte Carlo,
Historical Simulation, and Parametric VaR methods.

# ==========================================
# REFACTORING
# ==========================================

# Code cleanup
refactor(models): optimize correlation matrix calculations

Improve performance by 60% using vectorized operations
and caching frequently accessed matrix operations.

# API restructuring
refactor(api): reorganize endpoint structure for better REST compliance

Move portfolio-specific endpoints under /portfolios/ prefix
and standardize response formats across all endpoints.

# ==========================================
# PERFORMANCE
# ==========================================

# Performance improvement
perf(api): implement Redis caching for market data

Reduce API response time by 80% by caching frequently
requested market data with 1-hour TTL.

# Database optimization
perf(models): optimize database queries for historical data

Use batch queries and connection pooling to reduce
data retrieval time for backtesting operations.

# ==========================================
# MAINTENANCE
# ==========================================

# Dependency updates
chore(deps): update numpy to 1.25.0 and pandas to 2.1.0

Update mathematical libraries to latest stable versions
for improved performance and security patches.

# Configuration changes
chore(config): update production environment variables

Add new environment variables for enhanced logging
and monitoring in production deployment.

# Cleanup
chore: remove deprecated portfolio analysis methods

Clean up legacy code that is no longer used after
migration to new risk calculation engine.

# ==========================================
# CI/CD AND BUILD
# ==========================================

# CI pipeline
ci: add automated performance testing to GitHub Actions

Include benchmark tests that fail if API response time
exceeds acceptable thresholds.

# Build system
build: update Docker configuration for production deployment

Optimize Docker image size and add health check endpoints
for container orchestration.

# ==========================================
# TESTING
# ==========================================

# Test additions
test(models): add comprehensive unit tests for VaR calculations

Achieve 95% code coverage for risk calculation modules
with edge case testing for extreme market scenarios.

# Test fixes
test(api): fix flaky integration tests for portfolio endpoints

Stabilize tests by using deterministic random seeds
and proper test data cleanup.

# ==========================================
# STYLE AND FORMATTING
# ==========================================

# Code formatting
style: apply Black code formatting to Python files

Ensure consistent code style across all Python modules
following PEP 8 guidelines.

# Import organization
style: organize imports using isort

Sort and group imports consistently across all modules
for better code readability.