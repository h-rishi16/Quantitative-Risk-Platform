# Git Aliases for Easy Code Quality Management

## Add these to your ~/.gitconfig or run these commands:

```bash
# Quick format and commit workflow
git config --global alias.qc '!f(){ ./format-code.sh && git add . && git commit -m "$1" && git push origin main; }; f'

# Just format code
git config --global alias.fmt '!./format-code.sh'

# Format, add, and commit (without push)
git config --global alias.fac '!f(){ ./format-code.sh && git add . && git commit -m "$1"; }; f'
```

## Usage Examples:

```bash
# Format code only
git fmt

# Format, commit, and push in one command
git qc "Add new risk calculation feature"

# Format, add, and commit (but don't push yet)
git fac "Work in progress on portfolio analysis"
```

## Your New Workflow:

1. **Make code changes**
2. **Run**: `git qc "Your commit message"`
3. **Done!** CI/CD will pass

This makes maintaining code quality effortless while keeping all the benefits of professional CI/CD! 