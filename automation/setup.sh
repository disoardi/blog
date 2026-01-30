#!/bin/bash
# Setup script for Home Assistant Release Monitor

set -e  # Exit on error

echo "🚀 Home Assistant Release Monitor - Setup"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "📁 Working directory: $SCRIPT_DIR"
echo ""

# Check Python version
echo "🐍 Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✓${NC} Python 3 found: $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Poetry is available
echo ""
echo "📦 Checking for Poetry..."
if command -v poetry &> /dev/null; then
    echo -e "${GREEN}✓${NC} Poetry found"
    USE_POETRY=true

    # Initialize poetry if needed
    if [ ! -f "pyproject.toml" ]; then
        echo "Initializing Poetry project..."
        poetry init --no-interaction --name ha-release-monitor
    fi

    # Install dependencies
    echo "Installing dependencies with Poetry..."
    poetry add requests beautifulsoup4 PyYAML anthropic python-dotenv lxml

else
    echo -e "${YELLOW}⚠${NC} Poetry not found, using pip + venv"
    USE_POETRY=false

    # Create virtual environment
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi

    # Activate venv and install dependencies
    echo "Installing dependencies with pip..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# Setup .env file
echo ""
echo "🔑 Setting up environment variables..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠${NC} Created .env file from template"
    echo -e "${YELLOW}⚠${NC} Please edit .env and add your ANTHROPIC_API_KEY"
    echo ""
    read -p "Do you have your Anthropic API key ready? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter your Anthropic API key: " API_KEY
        sed -i.bak "s/your_api_key_here/$API_KEY/" .env
        rm .env.bak 2>/dev/null || true
        echo -e "${GREEN}✓${NC} API key configured"
    else
        echo -e "${YELLOW}⚠${NC} Remember to add your API key to .env before running!"
        echo "Get your key at: https://console.anthropic.com/"
    fi
else
    echo -e "${GREEN}✓${NC} .env file already exists"
fi

# Create necessary directories
echo ""
echo "📂 Creating directories..."
mkdir -p logs
mkdir -p temp
echo -e "${GREEN}✓${NC} Directories created"

# Check git configuration
echo ""
echo "🔧 Checking git configuration..."
if git rev-parse --git-dir > /dev/null 2>&1; then
    CURRENT_BRANCH=$(git branch --show-current)
    echo -e "${GREEN}✓${NC} Git repository detected (branch: $CURRENT_BRANCH)"

    # Update config.yaml with correct branch
    if [ -f "config.yaml" ]; then
        sed -i.bak "s/branch: \"main\"/branch: \"$CURRENT_BRANCH\"/" config.yaml
        rm config.yaml.bak 2>/dev/null || true
    fi
else
    echo -e "${YELLOW}⚠${NC} Not in a git repository. Some features may not work."
fi

# Update config.yaml with correct path
echo ""
echo "📝 Updating config.yaml..."
BLOG_ROOT=$(cd .. && pwd)
if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sed -i.bak "s|root_path: \".*\"|root_path: \"$BLOG_ROOT\"|" config.yaml
    rm config.yaml.bak 2>/dev/null || true
else
    echo -e "${YELLOW}⚠${NC} Please manually update 'root_path' in config.yaml to: $BLOG_ROOT"
fi

# Test run
echo ""
echo "🧪 Running basic configuration test..."
if [ "$USE_POETRY" = true ]; then
    poetry run python -c "import yaml; print('YAML: OK'); import requests; print('Requests: OK'); import anthropic; print('Anthropic: OK')"
else
    source venv/bin/activate
    python -c "import yaml; print('YAML: OK'); import requests; print('Requests: OK'); import anthropic; print('Anthropic: OK')"
fi

echo ""
echo -e "${GREEN}✓${NC} All dependencies imported successfully"

# Setup instructions
echo ""
echo "=========================================="
echo -e "${GREEN}✅ Setup completed!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Verify your .env file contains your API key:"
echo "   cat .env"
echo ""
echo "2. Test the monitor manually:"
if [ "$USE_POETRY" = true ]; then
    echo "   poetry run python ha_release_monitor.py"
else
    echo "   source venv/bin/activate && python ha_release_monitor.py"
fi
echo ""
echo "3. Setup cron job for automation:"
echo "   crontab -e"
echo ""
echo "   Add this line (update paths):"
if [ "$USE_POETRY" = true ]; then
    echo "   0 */6 * * * cd $SCRIPT_DIR && $(which poetry) run python ha_release_monitor.py >> logs/cron.log 2>&1"
else
    echo "   0 */6 * * * cd $SCRIPT_DIR && $SCRIPT_DIR/venv/bin/python ha_release_monitor.py >> logs/cron.log 2>&1"
fi
echo ""
echo "📚 For more information, read README.md"
echo ""
