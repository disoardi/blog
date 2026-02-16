#!/bin/bash
# download-header-image.sh
# Helper per scaricare immagini header da Unsplash con naming corretto
#
# Usage: ./download-header-image.sh <unsplash-url> <article-date> <article-slug>

set -euo pipefail

UNSPLASH_URL="${1:-}"
ARTICLE_DATE="${2:-}"
ARTICLE_SLUG="${3:-}"

if [[ -z "$UNSPLASH_URL" ]] || [[ -z "$ARTICLE_DATE" ]] || [[ -z "$ARTICLE_SLUG" ]]; then
    echo "Usage: $0 <unsplash-url> <article-date> <article-slug>"
    echo ""
    echo "Example:"
    echo "  $0 'https://images.unsplash.com/photo-XXXXX?w=1200&q=80' 20260214 minio-maintenance-mode"
    echo ""
    echo "  Scarica l'immagine e salva in static/img/ con naming convention:"
    echo "  static/img/<date>_<slug>_header.jpg"
    echo ""
    echo "💡 Come trovare URL Unsplash:"
    echo "   1. Vai su unsplash.com e cerca tema articolo"
    echo "   2. Seleziona immagine → Right-click → Copy Image Address"
    echo "   3. Usa URL formato: https://images.unsplash.com/photo-XXXXX?w=1200&q=80"
    exit 1
fi

# Validate date format (yyyyMMdd)
if [[ ! "$ARTICLE_DATE" =~ ^[0-9]{8}$ ]]; then
    echo "❌ Error: Date format deve essere yyyyMMdd (es. 20260214)"
    exit 1
fi

# Build output filename
OUTPUT_FILE="static/img/${ARTICLE_DATE}_${ARTICLE_SLUG}_header.jpg"

echo "📥 Scaricando immagine header da Unsplash..."
echo ""
echo "   URL:    $UNSPLASH_URL"
echo "   Output: $OUTPUT_FILE"
echo ""

# Check if file already exists
if [[ -f "$OUTPUT_FILE" ]]; then
    echo "⚠️  Warning: File già esistente: $OUTPUT_FILE"
    read -p "   Vuoi sovrascriverlo? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Operazione annullata"
        exit 0
    fi
fi

# Download image
if curl -L "$UNSPLASH_URL" -o "$OUTPUT_FILE"; then
    FILE_SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
    echo ""
    echo "✅ Immagine scaricata con successo!"
    echo ""
    echo "   📂 Path:  $OUTPUT_FILE"
    echo "   📊 Size:  $FILE_SIZE"
    echo ""
    echo "📝 Front matter da aggiungere all'articolo:"
    echo ""
    echo "---"
    echo "cover:"
    echo "  image: img/${ARTICLE_DATE}_${ARTICLE_SLUG}_header.jpg"
    echo "  alt: \"[Descrivi l'immagine]\""
    echo "  relative: false"
    echo "---"
    echo ""
    echo "💡 Next steps:"
    echo "   - Aggiungi cover al front matter dell'articolo"
    echo "   - Commit: git add static/img/ Post/ content/posts/"
else
    echo ""
    echo "❌ Error: Download fallito"
    echo "   Verifica che l'URL sia corretto e accessibile"
    exit 1
fi
