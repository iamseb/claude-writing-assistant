#!/bin/bash
# Setup script for Claude Writing Assistant

echo "Setting up Claude Writing Assistant..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is required but not installed."
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "Error: Node.js version 18+ is required. Current version: $(node -v)"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Install Claude Code CLI
echo "Installing Claude Code CLI..."
npm install

# Make Python script executable
chmod +x scripts/write.py

echo "✓ Setup complete!"
echo
echo "Usage:"
echo "  python scripts/write.py inputs/example_story.txt"
echo "  npm run example"
echo
echo "See README.md for detailed instructions."