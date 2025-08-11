#!/bin/bash
# Setup script for Claude Writing Assistant

echo "Setting up Claude Writing Assistant..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if Claude Code CLI is already installed
if command -v claude &> /dev/null; then
    echo "✓ Claude Code CLI is already installed"
else
    echo "Installing Claude Code CLI..."
    
    # Detect platform and install accordingly
    if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "msys" ]]; then
        # macOS, Linux, or WSL
        curl -fsSL claude.ai/install.sh | bash
    else
        echo "Please install Claude Code CLI manually:"
        echo "Visit: https://docs.anthropic.com/en/docs/claude-code/quickstart"
        exit 1
    fi
    
    # Verify installation
    if command -v claude &> /dev/null; then
        echo "✓ Claude Code CLI installed successfully"
    else
        echo "Error: Claude Code CLI installation failed. You may need to restart your shell."
        echo "Try running: source ~/.bashrc (or ~/.zshrc)"
        echo "Or install manually: https://docs.anthropic.com/en/docs/claude-code/quickstart"
        exit 1
    fi
fi

# Make Python script executable
chmod +x scripts/write.py

echo "✓ Setup complete!"
echo
echo "Usage:"
echo "  python3 scripts/write.py --list-collections"
echo "  python3 scripts/write.py inputs/example_story.txt"
echo
echo "See README.md for detailed instructions."