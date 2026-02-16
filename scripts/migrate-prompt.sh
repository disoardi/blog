#!/bin/bash
# migrate-prompt.sh
# Sposta prompt da drafts/ a published/ con naming corretto
#
# Usage: ./migrate-prompt.sh <draft-prompt> <published-article>

set -euo pipefail

DRAFT="${1:-}"
ARTICLE="${2:-}"

if [[ -z "$DRAFT" ]] || [[ -z "$ARTICLE" ]]; then
    echo "Usage: $0 <draft-prompt-name> <published-article-path>"
    echo ""
    echo "Example:"
    echo "  $0 20260214_minio_draft.md Post/20260214_minio-maintenance-mode_v01.0.md"
    echo ""
    echo "  Lo script estrarrà date e slug dall'articolo pubblicato per creare"
    echo "  il nome corretto del prompt in prompts/published/"
    exit 1
fi

DRAFT_PATH="prompts/drafts/$DRAFT"

if [[ ! -f "$DRAFT_PATH" ]]; then
    echo "❌ Error: Draft prompt not found: $DRAFT_PATH"
    exit 1
fi

if [[ ! -f "$ARTICLE" ]]; then
    echo "❌ Error: Published article not found: $ARTICLE"
    exit 1
fi

# Extract date and slug from article filename
ARTICLE_BASENAME=$(basename "$ARTICLE")

# Extract date (first 8 chars: yyyyMMdd)
DATE=$(echo "$ARTICLE_BASENAME" | cut -c1-8)

# Extract slug (everything between first _ and _vXX.Y.md)
SLUG=$(echo "$ARTICLE_BASENAME" | sed 's/^[0-9]*_//; s/_v[0-9.]*\.md$//')

# Build published prompt filename
PUBLISHED_NAME="${DATE}_${SLUG}_prompt.md"
PUBLISHED_PATH="prompts/published/$PUBLISHED_NAME"

echo "🚀 Migrando prompt da draft a published"
echo ""
echo "   Draft:     $DRAFT_PATH"
echo "   Articolo:  $ARTICLE"
echo "   Published: $PUBLISHED_PATH"
echo ""

# Check if published prompt already exists
if [[ -f "$PUBLISHED_PATH" ]]; then
    echo "⚠️  Warning: Il prompt published esiste già: $PUBLISHED_PATH"
    read -p "   Vuoi sovrascriverlo? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Operazione annullata"
        exit 0
    fi
fi

# Move the file
mv "$DRAFT_PATH" "$PUBLISHED_PATH"

echo "✅ Prompt migrato con successo!"
echo ""
echo "   📂 Nuovo path: $PUBLISHED_PATH"
echo ""
echo "   Naming convention rispettata:"
echo "      Date:  $DATE"
echo "      Slug:  $SLUG"
echo "      Match: $(basename "$ARTICLE" | sed 's/_v[0-9.]*\.md$//')"
echo ""
echo "💡 Next steps:"
echo "   - Verifica il contenuto del prompt"
echo "   - Commit: git add prompts/ && git commit -m '📝 Archivia prompt $SLUG'"
