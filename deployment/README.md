# Deployment

This directory contains all deployment-related files and scripts for the Quantitative Risk Modeling Platform.

## Files

### Docker Compose Files
- `docker-compose.yml` - Main development environment setup
- `docker-compose.staging.yml` - Staging environment configuration
- `docker-compose.prod.yml` - Production environment setup

### Deployment Scripts
- `deploy-staging.sh` - Automated staging deployment script
- `trigger-staging.sh` - Manual staging deployment trigger script

## Usage

### Development Environment
```bash
cd deployment
docker-compose up -d
```

### Staging Environment
```bash
cd deployment
docker-compose -f docker-compose.staging.yml up -d
```

### Production Environment
```bash
cd deployment
docker-compose -f docker-compose.prod.yml up -d
```

### Manual Staging Deployment
```bash
cd deployment
./trigger-staging.sh
```

## Prerequisites

- Docker and Docker Compose installed
- Environment files configured (see `config/` directory)
- GitHub tokens configured for automated deployments