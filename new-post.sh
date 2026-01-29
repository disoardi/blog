#!/bin/bash
# Helper script to create new blog posts with correct naming convention
# Usage: ./new-post.sh "Titolo del Post" [versione]

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if title is provided
if [ -z "$1" ]; then
    echo -e "${YELLOW}Usage: $0 \"Titolo del Post\" [versione]${NC}"
    echo "Example: $0 \"Il mio nuovo articolo\" 01.0"
    exit 1
fi

TITLE="$1"
VERSION="${2:-01.0}"  # Default version v01.0

# Generate date in yyyyMMdd format
DATE=$(date +%Y%m%d)

# Convert title to slug (lowercase, replace spaces with hyphens, remove special chars)
SLUG=$(echo "$TITLE" | iconv -t ascii//TRANSLIT | sed -E 's/[^a-zA-Z0-9]+/-/g' | sed -E 's/^-+|-+$//g' | tr A-Z a-z)

# Generate filename following convention: yyyyMMdd_titolo_vXX.Y.md
FILENAME="${DATE}_${SLUG}_v${VERSION}.md"
FILEPATH="content/posts/${FILENAME}"

# Check if file already exists
if [ -f "$FILEPATH" ]; then
    echo -e "${YELLOW}⚠️  File already exists: $FILEPATH${NC}"
    read -p "Do you want to overwrite it? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
fi

# Create the post using Hugo
hugo new "posts/${FILENAME}"

echo -e "${GREEN}✅ New post created successfully!${NC}"
echo -e "${BLUE}📝 File: $FILEPATH${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Edit the post: $FILEPATH"
echo "2. Add categories and tags"
echo "3. Write your content"
echo "4. Add an image to: static/img/${DATE}_${SLUG}_header.jpg"
echo "5. When ready, set draft: false"
echo ""
echo -e "${BLUE}🚀 Live preview: hugo server -D${NC}"
