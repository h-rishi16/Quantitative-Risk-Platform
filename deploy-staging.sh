#!/bin/bash

# Staging Deployment Script for Quantitative Risk Platform
# This script deploys the application to a staging environment

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.staging.yml"
PROJECT_NAME="risk-platform-staging"
STAGING_PORT_API=8003
STAGING_PORT_UI=8502

echo -e "${BLUE}🚀 Quantitative Risk Platform - Staging Deployment${NC}"
echo "=================================================="

# Function to print colored output
print_step() {
    echo -e "${BLUE}📋 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Docker is running
print_step "Checking Docker availability..."
if ! docker info >/dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker first."
    exit 1
fi
print_success "Docker is running"

# Check if Docker Compose is available
print_step "Checking Docker Compose availability..."
if ! docker compose version >/dev/null 2>&1; then
    print_error "Docker Compose is not available. Please install Docker Compose."
    exit 1
fi
print_success "Docker Compose is available"

# Create necessary directories
print_step "Creating necessary directories..."
mkdir -p logs
mkdir -p database
mkdir -p monitoring
print_success "Directories created"

# Create database initialization script for staging
print_step "Creating staging database initialization script..."
cat > database/init_staging.sql << 'EOF'
-- Staging Database Initialization Script
-- Create necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create staging tables (simplified for staging)
CREATE TABLE IF NOT EXISTS portfolio_snapshots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    portfolio_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    assets JSONB NOT NULL,
    weights JSONB NOT NULL,
    total_value DECIMAL(15,2) DEFAULT 0.00
);

CREATE TABLE IF NOT EXISTS risk_calculations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    portfolio_id UUID REFERENCES portfolio_snapshots(id),
    calculation_type VARCHAR(50) NOT NULL,
    confidence_levels JSONB,
    var_results JSONB,
    calculated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert sample data for staging
INSERT INTO portfolio_snapshots (portfolio_name, assets, weights, total_value) VALUES
('Staging Test Portfolio', '["AAPL", "GOOGL", "MSFT"]', '[0.4, 0.3, 0.3]', 1000000.00)
ON CONFLICT DO NOTHING;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_portfolio_created_at ON portfolio_snapshots(created_at);
CREATE INDEX IF NOT EXISTS idx_risk_calc_portfolio_id ON risk_calculations(portfolio_id);
CREATE INDEX IF NOT EXISTS idx_risk_calc_type ON risk_calculations(calculation_type);
EOF
print_success "Database initialization script created"

# Create Prometheus configuration for staging
print_step "Creating Prometheus configuration for staging..."
cat > monitoring/prometheus.staging.yml << 'EOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'risk-platform-api-staging'
    static_configs:
      - targets: ['backend:8002']
    metrics_path: '/metrics'
    scrape_interval: 30s

  - job_name: 'risk-platform-ui-staging'
    static_configs:
      - targets: ['frontend:8501']
    metrics_path: '/metrics'
    scrape_interval: 30s
EOF
print_success "Prometheus configuration created"

# Stop existing staging containers if running
print_step "Stopping existing staging containers..."
docker compose -f $COMPOSE_FILE -p $PROJECT_NAME down --remove-orphans || true
print_success "Existing containers stopped"

# Pull latest images
print_step "Pulling latest base images..."
docker compose -f $COMPOSE_FILE pull --ignore-pull-failures || true
print_success "Base images updated"

# Build the application
print_step "Building application containers..."
docker compose -f $COMPOSE_FILE -p $PROJECT_NAME build --no-cache
print_success "Application containers built"

# Start services
print_step "Starting staging services..."
docker compose -f $COMPOSE_FILE -p $PROJECT_NAME up -d
print_success "Staging services started"

# Wait for services to be healthy
print_step "Waiting for services to be healthy..."
sleep 30

# Check service health
print_step "Checking service health..."

# Check API health
API_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$STAGING_PORT_API/health || echo "000")
if [ "$API_HEALTH" = "200" ]; then
    print_success "API service is healthy (HTTP $API_HEALTH)"
else
    print_warning "API service may not be ready yet (HTTP $API_HEALTH)"
fi

# Check if UI is accessible
UI_CHECK=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$STAGING_PORT_UI || echo "000")
if [ "$UI_CHECK" = "200" ]; then
    print_success "UI service is accessible (HTTP $UI_CHECK)"
else
    print_warning "UI service may not be ready yet (HTTP $UI_CHECK)"
fi

# Display deployment information
echo ""
echo -e "${GREEN}🎉 Staging Deployment Complete!${NC}"
echo "=================================="
echo ""
echo -e "${BLUE}📍 Service URLs:${NC}"
echo "   • API (Backend):  http://localhost:$STAGING_PORT_API"
echo "   • UI (Frontend):  http://localhost:$STAGING_PORT_UI"
echo "   • Health Check:   http://localhost:$STAGING_PORT_API/health"
echo "   • API Docs:       http://localhost:$STAGING_PORT_API/docs"
echo "   • Database:       localhost:5433 (risk_platform_staging)"
echo "   • Redis Cache:    localhost:6380"
echo "   • Prometheus:     http://localhost:9091"
echo ""
echo -e "${BLUE}🔧 Management Commands:${NC}"
echo "   • View logs:      docker compose -f $COMPOSE_FILE -p $PROJECT_NAME logs -f"
echo "   • Stop services:  docker compose -f $COMPOSE_FILE -p $PROJECT_NAME down"
echo "   • Restart:        docker compose -f $COMPOSE_FILE -p $PROJECT_NAME restart"
echo "   • Remove all:     docker compose -f $COMPOSE_FILE -p $PROJECT_NAME down -v"
echo ""
echo -e "${BLUE}📊 Container Status:${NC}"
docker compose -f $COMPOSE_FILE -p $PROJECT_NAME ps

# Test API endpoints
echo ""
print_step "Testing API endpoints..."
sleep 5

# Test health endpoint
echo "Testing health endpoint..."
if curl -s http://localhost:$STAGING_PORT_API/health | grep -q "healthy"; then
    print_success "Health endpoint is working"
else
    print_warning "Health endpoint test failed"
fi

# Test sample data endpoint
echo "Testing sample data endpoint..."
if curl -s http://localhost:$STAGING_PORT_API/sample_data | grep -q "portfolio_weights"; then
    print_success "Sample data endpoint is working"
else
    print_warning "Sample data endpoint test failed"
fi

echo ""
print_success "Staging deployment validation complete!"
echo ""
echo -e "${YELLOW}💡 Next steps:${NC}"
echo "   1. Open http://localhost:$STAGING_PORT_UI in your browser"
echo "   2. Test the Monte Carlo VaR calculations"
echo "   3. Check the API documentation at http://localhost:$STAGING_PORT_API/docs"
echo "   4. Monitor logs: docker compose -f $COMPOSE_FILE -p $PROJECT_NAME logs -f"
echo ""