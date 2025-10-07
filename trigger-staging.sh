#!/bin/bash

# Manual trigger for GitHub Actions staging deployment
# This script triggers the staging deployment workflow manually

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Triggering GitHub Actions Staging Deployment${NC}"
echo "================================================="

# Repository information
REPO_OWNER="h-rishi16"
REPO_NAME="Quantitative-Risk-Platform"
WORKFLOW_FILE="staging.yml"

echo -e "${BLUE}📋 Repository: ${REPO_OWNER}/${REPO_NAME}${NC}"
echo -e "${BLUE}📋 Workflow: ${WORKFLOW_FILE}${NC}"

# Check if GitHub token is available
if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${YELLOW}⚠️  GITHUB_TOKEN not set${NC}"
    echo "To manually trigger the workflow:"
    echo "1. Go to: https://github.com/${REPO_OWNER}/${REPO_NAME}/actions"
    echo "2. Click on 'Deploy to Staging' workflow"
    echo "3. Click 'Run workflow' button"
    echo "4. Optionally add a deployment reason"
    echo "5. Click 'Run workflow'"
    echo ""
    echo "Or set GITHUB_TOKEN and run this script:"
    echo "export GITHUB_TOKEN='your_github_token'"
    echo "./trigger-staging.sh"
    exit 0
fi

# Trigger the workflow
echo -e "${BLUE}🔄 Triggering staging deployment workflow...${NC}"

RESPONSE=$(curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/actions/workflows/${WORKFLOW_FILE}/dispatches" \
  -d '{
    "ref": "main",
    "inputs": {
      "deploy_reason": "Manual staging deployment triggered via script"
    }
  }')

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Staging deployment workflow triggered successfully!${NC}"
    echo ""
    echo -e "${BLUE}📍 Monitor the deployment:${NC}"
    echo "   🔗 Actions: https://github.com/${REPO_OWNER}/${REPO_NAME}/actions"
    echo "   🔗 Workflow: https://github.com/${REPO_OWNER}/${REPO_NAME}/actions/workflows/${WORKFLOW_FILE}"
    echo ""
    echo -e "${BLUE}📊 Expected staging services (after deployment):${NC}"
    echo "   🌐 Frontend UI: Available via GitHub Actions runner"
    echo "   🔌 Backend API: Available via GitHub Actions runner"
    echo "   🏥 Health Check: Automated in workflow"
    echo "   📚 API Docs: Automated testing in workflow"
    echo ""
    echo -e "${YELLOW}💡 Note: This is running on GitHub's infrastructure${NC}"
    echo "   The staging environment will be available during the workflow execution"
    echo "   for testing and validation purposes."
else
    echo -e "${RED}❌ Failed to trigger workflow${NC}"
    echo "Response: $RESPONSE"
    exit 1
fi