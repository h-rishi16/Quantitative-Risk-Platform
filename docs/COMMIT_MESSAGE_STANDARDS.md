# Commit Message Standards

This document establishes professional commit message standards for the Quantitative Risk Platform project.

## Format Structure

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type (Required)
- **feat**: New feature for the user
- **fix**: Bug fix for the user
- **docs**: Changes to documentation
- **style**: Formatting, missing semicolons, etc; no production code change
- **refactor**: Refactoring production code, eg. renaming a variable
- **test**: Adding missing tests, refactoring tests; no production code change
- **chore**: Updating grunt tasks etc; no production code change
- **perf**: Performance improvements
- **ci**: Changes to CI configuration files and scripts
- **build**: Changes that affect the build system or external dependencies

### Scope (Optional)
- **api**: Backend API changes
- **frontend**: Frontend/UI changes
- **models**: Risk modeling components
- **config**: Configuration changes
- **deps**: Dependency updates
- **deploy**: Deployment related changes

### Subject (Required)
- Use imperative mood: "fix bug" not "fixed bug" or "fixes bug"
- Don't capitalize first letter
- No period at the end
- Maximum 50 characters

### Body (Optional)
- Wrap at 72 characters
- Explain what and why, not how
- Use bullet points if needed

### Footer (Optional)
- Reference issues: "Closes #123"
- Breaking changes: "BREAKING CHANGE: ..."

## Examples

### Good Examples

```
feat(api): add portfolio risk calculation endpoint

- Implement Monte Carlo VaR calculation
- Add input validation for portfolio data
- Include confidence interval parameters
- Return results in JSON format

Closes #45
```

```
fix(frontend): resolve chart rendering issue with large datasets

The plotly charts were not rendering properly when portfolio 
contained more than 1000 assets. Updated data aggregation 
logic to handle large datasets efficiently.

Fixes #67
```

```
docs: update deployment guide with production requirements

- Add system requirements section
- Include environment variable examples
- Update troubleshooting section
```

```
refactor(models): optimize Monte Carlo simulation performance

Reduced simulation time by 40% through vectorized operations
and improved random number generation.
```

### Poor Examples (Avoid These)

```
❌ "Fixed stuff"
❌ "WIP"
❌ "Update file.py"
❌ "🚀 Add new feature"
❌ "FINAL VERSION"
❌ "asdf"
❌ "Merge branch 'feature'"
```

## Quick Reference

### Common Patterns for This Project

**New Features:**
```
feat(api): implement stress testing endpoints
feat(frontend): add portfolio optimization dashboard
feat(models): integrate Black-Scholes option pricing
```

**Bug Fixes:**
```
fix(api): correct VaR calculation for edge cases
fix(frontend): resolve data upload validation errors
fix(models): handle division by zero in correlation matrix
```

**Documentation:**
```
docs: update API documentation with new endpoints
docs: add mathematical formulas to risk model guide
docs: improve setup instructions for Windows users
```

**Maintenance:**
```
chore(deps): update numpy to version 1.25.0
chore(config): update production environment variables
chore: remove deprecated portfolio analysis methods
```

**Performance:**
```
perf(models): optimize correlation matrix calculations
perf(api): implement caching for historical data queries
```

**CI/CD:**
```
ci: add automated security scanning to workflow
ci: update deployment pipeline for production
```

## Tools and Automation

### Git Hooks (Optional)
You can set up a commit message hook to validate format:

```bash
# Create .git/hooks/commit-msg
#!/bin/sh
commit_regex='^(feat|fix|docs|style|refactor|test|chore|perf|ci|build)(\(.+\))?: .{1,50}'

if ! grep -qE "$commit_regex" "$1"; then
    echo "Invalid commit message format!"
    echo "Format: type(scope): subject"
    echo "Example: feat(api): add new risk calculation endpoint"
    exit 1
fi
```

### VS Code Integration
Install the "Conventional Commits" extension for VS Code to get commit message templates.

## Benefits

1. **Professional Appearance**: Clean, consistent commit history
2. **Easy Navigation**: Quickly understand what each commit does
3. **Automated Tools**: Enable automatic changelog generation
4. **Team Collaboration**: Clear communication about changes
5. **Industry Standards**: Follows widely adopted conventions

## Implementation

Starting immediately, all commits should follow this format. The existing commit history remains unchanged to preserve git integrity.

## Resources

- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [Angular Commit Message Guidelines](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit)
- [Semantic Versioning](https://semver.org/)