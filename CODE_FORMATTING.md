# Code Formatting Guide

This project uses automated code formatting to maintain consistent code style.

## Before Every Commit

Run the formatting script:
```bash
./format-code.sh
```

## Manual Commands

If you prefer to run commands individually:

```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Check formatting (without changing files)
black --check --diff .
isort --check-only --diff .
```

## VS Code Setup (Optional)

Add these settings to your VS Code settings.json:
```json
{
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

## Why We Use Formatting

- **Consistency**: All code looks the same regardless of who wrote it
- **CI/CD**: GitHub Actions requires properly formatted code
- **Readability**: Clean, consistent code is easier to understand
- **Professional**: Industry standard practice

## Deployment Note

**Important**: Code formatting is only required for GitHub CI/CD checks. Your app will deploy and run perfectly on Render regardless of formatting - this is purely for code quality and maintainability.