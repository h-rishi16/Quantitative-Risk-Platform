# Configuration Files

This directory contains all configuration templates and examples for the Quantitative Risk Modeling Platform.

## Files

### Environment Configuration
- `.env.example` - Template for development environment variables
- `.env.staging.example` - Template for staging environment variables

## Usage

1. Copy the appropriate example file to create your environment configuration:
   ```bash
   cp config/.env.example .env
   cp config/.env.staging.example .env.staging
   ```

2. Edit the copied files with your specific configuration values

## Security Note

Never commit actual `.env` files with real credentials to version control. Only commit the `.example` templates.