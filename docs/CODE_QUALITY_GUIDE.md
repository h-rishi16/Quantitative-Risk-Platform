# 🔧 Code Quality Workflow Guide

## Why We Use Code Formatting

Your project has **CI/CD (Continuous Integration)** set up to maintain high code quality. This automatically:
- ✅ **Tests your code** when you push changes
- ✅ **Checks formatting** with Black and isort  
- ✅ **Runs linting** with flake8
- ✅ **Prevents deployment** if code quality issues exist

## Quick Workflow (Before Every Commit)

### Step 1: Make Your Code Changes
Edit your Python files as needed.

### Step 2: Auto-Format Your Code
```bash
./format-code.sh
```
This will:
- Format code with **Black**
- Sort imports with **isort**
- Verify everything is ready for CI/CD

### Step 3: Commit and Push
```bash
git add .
git commit -m "Your descriptive commit message"
git push origin main
```

## Alternative: Manual Commands

If you prefer running commands manually:

```bash
# Format code
black . --exclude=".venv|venv|env"

# Sort imports
isort . --profile black

# Check if ready (optional)
black --check --diff .
isort --check-only --diff --profile black .
```

## What Happens in CI/CD

When you push code, GitHub Actions automatically:

1. **🏗️ Sets up Python 3.11 environment**
2. **📦 Installs all dependencies**
3. **🧹 Checks code formatting** (Black & isort)
4. **🔍 Runs linting** (flake8)
5. **🧪 Runs unit tests** (pytest)
6. **✅ Passes = Ready for deployment**
7. **❌ Fails = Fix issues and try again**

## Benefits of This Approach

- **🚀 Professional code quality** standards
- **🤝 Consistent formatting** across the team
- **🐛 Catches issues early** before deployment
- **📈 Maintainable codebase** over time
- **⚡ Deployment confidence** - if CI passes, it works

## Troubleshooting

### If CI/CD Still Fails:
1. Run `./format-code.sh` again
2. Check for any error messages
3. Fix any remaining issues manually
4. Commit and push again

### Skip Formatting Checks (Not Recommended):
If you need to push urgently without formatting:
```bash
git commit -m "urgent fix" --no-verify
```

## For Render Deployment

**Important**: Code formatting does **NOT** affect your app's functionality on Render. It's purely for code quality and team collaboration. Your app will deploy and run perfectly regardless of formatting - the CI/CD is just ensuring professional standards.

---
*This workflow ensures your quantitative risk platform maintains enterprise-level code quality! 🎯*