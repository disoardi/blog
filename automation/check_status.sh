#!/bin/bash
# Quick status check for Home Assistant Release Monitor

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "📊 Home Assistant Release Monitor - Status Check"
echo "=================================================="
echo ""

# Check if system is configured
echo "🔧 Configuration:"
if [ -f "config.yaml" ]; then
    TARGET_VERSION=$(grep "target_version:" config.yaml | cut -d'"' -f2)
    echo "  Target version: $TARGET_VERSION"
else
    echo "  ❌ config.yaml not found"
fi

if [ -f ".env" ]; then
    if grep -q "your_api_key_here" .env; then
        echo "  ⚠️  API key not configured"
    else
        echo "  ✅ API key configured"
    fi
else
    echo "  ❌ .env file not found"
fi

echo ""

# Check state
echo "📝 Monitor State:"
if [ -f "temp/monitor_state.json" ]; then
    echo "  State file exists:"
    cat temp/monitor_state.json | python3 -m json.tool 2>/dev/null || cat temp/monitor_state.json
else
    echo "  No state file (first run pending)"
fi

echo ""

# Check recent logs
echo "📋 Recent Activity:"
if [ -f "logs/ha_monitor.log" ]; then
    echo "  Last 5 log entries:"
    tail -5 logs/ha_monitor.log | sed 's/^/    /'
else
    echo "  No log file yet"
fi

echo ""

# Check cron
echo "⏰ Cron Job:"
CRON_ENTRY=$(crontab -l 2>/dev/null | grep "ha_release_monitor")
if [ -n "$CRON_ENTRY" ]; then
    echo "  ✅ Cron job configured:"
    echo "     $CRON_ENTRY"
else
    echo "  ❌ No cron job found"
    echo "     Run: crontab -e"
fi

echo ""

# Check git status
echo "🔄 Git Status:"
cd ..
if git rev-parse --git-dir > /dev/null 2>&1; then
    BRANCH=$(git branch --show-current)
    echo "  Branch: $BRANCH"

    UNCOMMITTED=$(git status --porcelain | wc -l)
    if [ "$UNCOMMITTED" -gt 0 ]; then
        echo "  ⚠️  $UNCOMMITTED uncommitted changes"
    else
        echo "  ✅ Working directory clean"
    fi

    UNPUSHED=$(git log origin/$BRANCH..$BRANCH --oneline 2>/dev/null | wc -l)
    if [ "$UNPUSHED" -gt 0 ]; then
        echo "  ⚠️  $UNPUSHED unpushed commits"
    else
        echo "  ✅ All commits pushed"
    fi
else
    echo "  ❌ Not a git repository"
fi

echo ""
echo "=================================================="
