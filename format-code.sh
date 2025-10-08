#!/bin/bash
# Auto-format Python code before committing
# Run this script before every git commit to pass CI/CD checks

echo "🔧 Auto-formatting Python code..."

# Format with Black (exclude virtual environments)
echo "  ├── Running Black formatter..."
black . --exclude=".venv|venv|env"

# Sort imports with isort (compatible with Black)
echo "  ├── Sorting imports with isort..."
isort . --profile black

# Verify formatting is correct
echo "  └── Verifying formatting..."
black --check --diff . --exclude=".venv|venv|env" > /dev/null 2>&1
BLACK_STATUS=$?
isort --check-only --diff --profile black . > /dev/null 2>&1
ISORT_STATUS=$?

if [ $BLACK_STATUS -eq 0 ] && [ $ISORT_STATUS -eq 0 ]; then
    echo "✅ Code formatting complete! CI/CD checks will pass."
else
    echo "⚠️  Some files were formatted. Please review changes before committing."
fi

echo ""
echo "💡 Ready to commit? Run:"
echo "   git add ."
echo "   git commit -m 'Your commit message'"
echo "   git push origin main"