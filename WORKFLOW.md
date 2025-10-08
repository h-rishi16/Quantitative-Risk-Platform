# Development Workflow

## Simple 3-Step Process

### 1. Make Your Changes
- Edit your Python files
- Add new features
- Fix bugs

### 2. Format Your Code
```bash
./format-code.sh
```

### 3. Commit and Push
```bash
git add .
git commit -m "your descriptive commit message"
git push origin main
```

## That's It! 🎉

The CI/CD pipeline will:
- ✅ Check your formatting (should pass now)
- ✅ Run tests
- ✅ Deploy if everything passes

## If CI/CD Fails

1. Check the GitHub Actions tab in your repository
2. Look for the specific error
3. Run `./format-code.sh` again
4. Commit and push the fixes

## Quick Commands

```bash
# Format and commit in one go
./format-code.sh && git add . && git commit -m "update: formatted code" && git push origin main

# Check formatting without changing files
black --check --diff .
isort --check-only --diff .
```