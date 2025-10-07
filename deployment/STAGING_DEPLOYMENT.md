# Staging Deployment Guide

## Quantitative Risk Platform - Staging Environment

This guide covers deploying the Quantitative Risk Modeling Platform to a staging environment for testing and validation before production deployment.

## Prerequisites

### 1. Install Docker Desktop
- **macOS**: Download from [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
- **Windows**: Download from [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
- **Linux**: Install Docker Engine and Docker Compose

### 2. Verify Docker Installation
```bash
docker --version
docker compose --version
```

### 3. System Requirements
- **RAM**: Minimum 8GB (16GB recommended)
- **Storage**: At least 10GB free space
- **CPU**: 4+ cores recommended
- **Ports**: 8003, 8502, 5433, 6380, 9091 should be available

## Quick Start

### Option 1: Automated Deployment Script
```bash
# Make script executable
chmod +x deploy-staging.sh

# Deploy to staging
./deploy-staging.sh
```

### Option 2: Manual Docker Compose
```bash
# Create environment file
cp .env.staging.example .env.staging

# Deploy with Docker Compose
docker compose -f docker-compose.staging.yml -p risk-platform-staging up -d --build

# Check status
docker compose -f docker-compose.staging.yml -p risk-platform-staging ps
```

## Service URLs (After Deployment)

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend UI** | http://localhost:8502 | Main Streamlit application |
| **Backend API** | http://localhost:8003 | FastAPI backend services |
| **API Documentation** | http://localhost:8003/docs | Interactive API documentation |
| **Health Check** | http://localhost:8003/health | Service health status |
| **Database** | localhost:5433 | PostgreSQL staging database |
| **Redis Cache** | localhost:6380 | Redis cache instance |
| **Monitoring** | http://localhost:9091 | Prometheus metrics |

## Staging Environment Features

### Configuration
- **Environment**: Staging isolation with separate ports
- **Debug Mode**: Enabled for detailed logging
- **Database**: Dedicated PostgreSQL staging instance
- **Cache**: Redis with staging-specific configuration
- **Monitoring**: Prometheus metrics collection

### Testing Features
- **Sample Data**: Pre-loaded test portfolios
- **Debug Logging**: Comprehensive request/response logging  
- **Health Checks**: Automated service monitoring
- **Performance Metrics**: Response time and throughput tracking

### Services

#### Backend API (Port 8003)
- FastAPI application with comprehensive risk calculations
- Monte Carlo VaR simulations
- Portfolio optimization algorithms
- RESTful API endpoints with OpenAPI documentation

#### Frontend UI (Port 8502)
- Streamlit-based interactive web interface
- Real-time risk visualization with Plotly
- File upload capabilities for portfolios and returns data
- Interactive Monte Carlo simulation parameters

#### Database (Port 5433)
- PostgreSQL 15 with staging-specific schema
- Portfolio snapshots and risk calculation history
- Sample data for testing scenarios

#### Cache Layer (Port 6380)
- Redis for session management and calculation caching
- Improved performance for repeated calculations

## Testing the Deployment

### 1. Health Checks
```bash
# Check API health
curl http://localhost:8003/health

# Check sample data endpoint
curl http://localhost:8003/sample_data

# Check API documentation
open http://localhost:8003/docs
```

### 2. Frontend Testing
```bash
# Open the Streamlit UI
open http://localhost:8502
```

### 3. Database Testing
```bash
# Connect to staging database
docker exec -it risk-platform-db-staging psql -U risk_user_staging -d risk_platform_staging

# Check tables
\dt

# View sample data
SELECT * FROM portfolio_snapshots;
```

## Management Commands

### View Logs
```bash
# All services
docker compose -f docker-compose.staging.yml -p risk-platform-staging logs -f

# Specific service
docker compose -f docker-compose.staging.yml -p risk-platform-staging logs -f backend
```

### Restart Services
```bash
# Restart all services
docker compose -f docker-compose.staging.yml -p risk-platform-staging restart

# Restart specific service
docker compose -f docker-compose.staging.yml -p risk-platform-staging restart backend
```

### Stop Services
```bash
# Stop all services
docker compose -f docker-compose.staging.yml -p risk-platform-staging down

# Stop and remove volumes (clean slate)
docker compose -f docker-compose.staging.yml -p risk-platform-staging down -v
```

### Update Deployment
```bash
# Pull latest changes and rebuild
git pull origin main
docker compose -f docker-compose.staging.yml -p risk-platform-staging down
docker compose -f docker-compose.staging.yml -p risk-platform-staging up -d --build
```

## Environment Variables

Key staging environment variables (see `.env.staging.example`):

```bash
ENVIRONMENT=staging
DEBUG=true
LOG_LEVEL=DEBUG
API_BASE_URL=http://localhost:8003
POSTGRES_DB=risk_platform_staging
REDIS_PASSWORD=staging_redis_password_2024
```

## Troubleshooting

### Port Conflicts
If ports are already in use, modify the port mappings in `docker-compose.staging.yml`:
```yaml
ports:
  - "8004:8002"  # Change 8003 to 8004
```

### Memory Issues
If containers are getting killed due to memory:
```bash
# Check Docker Desktop memory allocation (8GB+ recommended)
# Reduce number of Monte Carlo simulations in testing
```

### Database Connection Issues
```bash
# Check database container status
docker compose -f docker-compose.staging.yml -p risk-platform-staging ps postgres

# Check database logs
docker compose -f docker-compose.staging.yml -p risk-platform-staging logs postgres
```

### Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER logs/
sudo chown -R $USER:$USER database/
```

## GitHub Actions Integration

The staging environment integrates with GitHub Actions for automated deployment:

- **Trigger**: Push to `main` branch or manual dispatch
- **Testing**: Runs full test suite before deployment
- **Building**: Creates staging-specific Docker images
- **Deployment**: Automated staging environment setup
- **Validation**: Health checks and functionality tests

## Security Notes

**WARNING - Staging Environment Warnings**:
- Uses default passwords (change for production)
- Debug mode enabled (disable for production)
- No SSL/TLS encryption (add for production)
- Open CORS policy (restrict for production)

## Performance Monitoring

### Metrics Available
- API response times
- Database query performance
- Memory and CPU usage
- Request/response rates
- Error rates and types

### Access Monitoring
- **Prometheus**: http://localhost:9091
- **Container Stats**: `docker stats`
- **Logs**: Real-time logging available

## Next Steps

1. **Test Core Functionality**: Upload portfolios and run VaR calculations
2. **Performance Testing**: Load test with multiple concurrent requests
3. **Integration Testing**: Test all API endpoints and UI workflows
4. **Security Review**: Validate authentication and authorization
5. **Production Deployment**: Deploy to production environment

## Support

For issues with staging deployment:
1. Check logs: `docker compose -f docker-compose.staging.yml -p risk-platform-staging logs`
2. Verify Docker resources (memory, disk space)
3. Check port availability
4. Review environment variables
5. Validate sample data loading

---

**CHECKLIST - Staging Deployment Checklist**:
- [ ] Docker Desktop installed and running
- [ ] Ports 8003, 8502, 5433, 6380, 9091 available
- [ ] Minimum 8GB RAM allocated to Docker
- [ ] Git repository up to date
- [ ] Environment variables configured
- [ ] Deployment script executed successfully
- [ ] Health checks passing
- [ ] Frontend accessible
- [ ] API documentation available
- [ ] Database connected and populated
- [ ] Monitoring dashboard accessible