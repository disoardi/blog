#!/bin/bash
# cross-link-checker.sh
# Suggerisce articoli esistenti che potrebbero linkare al nuovo contenuto
#
# Usage: ./cross-link-checker.sh path/to/new-article.md

set -euo pipefail

NEW_ARTICLE="${1:-}"

if [[ -z "$NEW_ARTICLE" ]]; then
    echo "Usage: $0 <path-to-article.md>"
    echo "Example: $0 Post/20260214_minio-maintenance-mode_v01.0.md"
    exit 1
fi

if [[ ! -f "$NEW_ARTICLE" ]]; then
    echo "Error: File not found: $NEW_ARTICLE"
    exit 1
fi

echo "🔍 Analizzando: $NEW_ARTICLE"
echo ""

# Extract tags from front matter (requires yq or fallback to grep)
if command -v yq &> /dev/null; then
    TAGS=$(yq '.tags[]' "$NEW_ARTICLE" 2>/dev/null || true)
else
    # Fallback: extract tags manually from YAML front matter
    TAGS=$(awk '/^tags:/{flag=1; next} /^[a-z]/{flag=0} flag && /- /{gsub(/^[[:space:]]*-[[:space:]]*/, ""); print}' "$NEW_ARTICLE")
fi

if [[ -z "$TAGS" ]]; then
    echo "⚠️  Nessun tag trovato nel front matter"
    echo "   Aggiungi tag per migliorare la ricerca cross-link"
    exit 0
fi

echo "📌 Tag estratti:"
echo "$TAGS" | sed 's/^/   - /'
echo ""

# Build regex pattern from tags (case-insensitive)
PATTERN=$(echo "$TAGS" | tr '\n' '|' | sed 's/|$//')

if [[ -z "$PATTERN" ]]; then
    echo "⚠️  Pattern vuoto, impossibile continuare"
    exit 0
fi

echo "🔎 Cercando articoli correlati in Post/ e content/..."
echo ""

# Find related articles
RELATED=$(grep -r -l -i -E "$PATTERN" Post/ content/ --include="*.md" 2>/dev/null | grep -v "$NEW_ARTICLE" | sort -u || true)

if [[ -z "$RELATED" ]]; then
    echo "✅ Nessun articolo correlato trovato"
    echo "   Il nuovo articolo introduce topic completamente nuovo"
else
    echo "🔗 Articoli che potrebbero linkare al nuovo contenuto:"
    echo ""

    while IFS= read -r article; do
        # Extract title from front matter
        TITLE=$(awk '/^title:/{gsub(/^title:[[:space:]]*"|"$/, ""); print; exit}' "$article")

        # Extract matching lines for preview
        MATCHES=$(grep -i -E "$PATTERN" "$article" | head -3 | sed 's/^/      /')

        echo "  📄 $article"
        if [[ -n "$TITLE" ]]; then
            echo "     Titolo: $TITLE"
        fi
        echo "     Menzioni:"
        echo "$MATCHES"
        echo ""
    done <<< "$RELATED"

    COUNT=$(echo "$RELATED" | wc -l | tr -d ' ')
    echo "💡 Totale: $COUNT articol$([ "$COUNT" -eq 1 ] && echo "o" || echo "i") da considerare per cross-linking"
    echo ""
    echo "   Prossimi step:"
    echo "   1. Review articoli suggeriti"
    echo "   2. Aggiungi link dove rilevante"
    echo "   3. Aggiungi 'lastmod: $(date +%Y-%m-%d)' al front matter"
fi
