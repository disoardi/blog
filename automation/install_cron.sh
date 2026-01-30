#!/bin/bash
# Script to install cron job for Home Assistant Release Monitor

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "🚀 Installazione Cron Job per Home Assistant Release Monitor"
echo ""

# Get the absolute path to this script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BLOG_DIR="$(dirname "$SCRIPT_DIR")"

echo "📁 Directory blog: $BLOG_DIR"
echo "📁 Directory automation: $SCRIPT_DIR"
echo ""

# Check if poetry is available
if command -v poetry &> /dev/null; then
    PYTHON_CMD="cd $SCRIPT_DIR && poetry run python"
    echo "✅ Poetry trovato - userò: poetry run python"
elif [ -f "$SCRIPT_DIR/venv/bin/python" ]; then
    PYTHON_CMD="$SCRIPT_DIR/venv/bin/python"
    echo "✅ Virtualenv trovato - userò: venv/bin/python"
else
    PYTHON_CMD="python3"
    echo "⚠️  Poetry/venv non trovati - userò: python3"
fi

echo ""

# Create the cron job command
CRON_COMMAND="0 */6 * * * cd $SCRIPT_DIR && $PYTHON_CMD ha_release_monitor.py >> logs/cron.log 2>&1"

echo "📝 Cron job che verrà installato:"
echo "   $CRON_COMMAND"
echo ""

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "ha_release_monitor.py"; then
    echo -e "${YELLOW}⚠️  Un cron job per ha_release_monitor.py esiste già!${NC}"
    echo ""
    echo "Cron job esistenti:"
    crontab -l | grep "ha_release_monitor.py"
    echo ""
    read -p "Vuoi sostituirlo? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Operazione annullata"
        exit 1
    fi

    # Remove old cron job
    crontab -l | grep -v "ha_release_monitor.py" | crontab -
    echo "🗑️  Vecchio cron job rimosso"
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_COMMAND") | crontab -

echo ""
echo -e "${GREEN}✅ Cron job installato con successo!${NC}"
echo ""
echo "📊 Verifica installazione:"
echo ""
crontab -l | grep "ha_release_monitor.py"
echo ""
echo "📖 Il cron job verrà eseguito:"
echo "   - Ogni 6 ore (00:00, 06:00, 12:00, 18:00)"
echo "   - Log salvati in: $SCRIPT_DIR/logs/cron.log"
echo ""
echo "🔍 Per monitorare i log in tempo reale:"
echo "   tail -f $SCRIPT_DIR/logs/cron.log"
echo ""
echo "📝 Per modificare il cron job:"
echo "   crontab -e"
echo ""
echo "🗑️  Per rimuovere il cron job:"
echo "   crontab -l | grep -v 'ha_release_monitor.py' | crontab -"
echo ""
echo -e "${GREEN}🎉 Setup completato!${NC}"
