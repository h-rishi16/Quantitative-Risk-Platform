#!/bin/bash
# Git commit helper script for professional commit messages
# Usage: ./git-commit.sh

echo "Professional Git Commit Helper"
echo "=============================="

# Function to show commit types
show_types() {
    echo ""
    echo "Available commit types:"
    echo "  feat     - New feature"
    echo "  fix      - Bug fix"
    echo "  docs     - Documentation changes"
    echo "  style    - Code formatting, no logic changes"
    echo "  refactor - Code refactoring"
    echo "  test     - Adding or updating tests"
    echo "  chore    - Maintenance tasks"
    echo "  perf     - Performance improvements"
    echo "  ci       - CI/CD changes"
    echo "  build    - Build system changes"
    echo ""
}

# Function to show common scopes for this project
show_scopes() {
    echo ""
    echo "Common scopes for this project:"
    echo "  api       - Backend API changes"
    echo "  frontend  - Frontend/UI changes"
    echo "  models    - Risk modeling components"
    echo "  config    - Configuration changes"
    echo "  deps      - Dependency updates"
    echo "  deploy    - Deployment related"
    echo ""
}

# Get commit type
show_types
read -p "Enter commit type: " type

# Validate type
valid_types="feat fix docs style refactor test chore perf ci build"
if [[ ! " $valid_types " =~ " $type " ]]; then
    echo "Error: Invalid commit type '$type'"
    show_types
    exit 1
fi

# Get optional scope
show_scopes
read -p "Enter scope (optional, press Enter to skip): " scope

# Build type and scope part
if [ -n "$scope" ]; then
    type_scope="$type($scope)"
else
    type_scope="$type"
fi

# Get subject
echo ""
echo "Subject guidelines:"
echo "- Use imperative mood (e.g., 'add feature' not 'added feature')"
echo "- Don't capitalize first letter"
echo "- No period at the end"
echo "- Maximum 50 characters"
echo ""
read -p "Enter subject: " subject

# Validate subject length
if [ ${#subject} -gt 50 ]; then
    echo "Warning: Subject is ${#subject} characters (recommended max: 50)"
    read -p "Continue anyway? (y/n): " continue
    if [ "$continue" != "y" ]; then
        exit 1
    fi
fi

# Get optional body
echo ""
read -p "Enter body (optional, press Enter to skip): " body

# Get optional footer
echo ""
read -p "Enter footer (e.g., 'Closes #123', press Enter to skip): " footer

# Build commit message
commit_message="$type_scope: $subject"

if [ -n "$body" ]; then
    commit_message="$commit_message

$body"
fi

if [ -n "$footer" ]; then
    commit_message="$commit_message

$footer"
fi

# Show preview
echo ""
echo "Commit message preview:"
echo "======================="
echo "$commit_message"
echo "======================="

# Confirm
read -p "Commit with this message? (y/n): " confirm
if [ "$confirm" = "y" ]; then
    git add -A
    git commit -m "$commit_message"
    echo ""
    echo "Committed successfully!"
    echo ""
    echo "To push to GitHub:"
    echo "git push origin main"
else
    echo "Commit cancelled."
fi