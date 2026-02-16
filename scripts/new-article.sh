#!/bin/bash
# new-article.sh
# Genera template per nuovo articolo + prompt draft
#
# Usage: ./new-article.sh [slug]

set -euo pipefail

DATE=$(date +%Y%m%d)
DATE_FORMATTED=$(date +%Y-%m-%d)

SLUG="${1:-}"

# Interactive mode if no slug provided
if [[ -z "$SLUG" ]]; then
    echo "🆕 Creazione nuovo articolo"
    echo ""
    read -p "📝 Slug articolo (es. minio-maintenance-mode): " SLUG

    if [[ -z "$SLUG" ]]; then
        echo "❌ Error: Slug obbligatorio"
        exit 1
    fi
fi

read -p "📰 Titolo articolo: " TITLE

if [[ -z "$TITLE" ]]; then
    echo "❌ Error: Titolo obbligatorio"
    exit 1
fi

read -p "📚 Categoria (Infrastructure, Self-Hosting, AI, etc.): " CATEGORY
read -p "🏷️  Tag (separati da virgola): " TAGS_INPUT

# Parse tags
IFS=',' read -ra TAGS_ARRAY <<< "$TAGS_INPUT"
TAGS_YAML=""
for tag in "${TAGS_ARRAY[@]}"; do
    tag=$(echo "$tag" | xargs) # trim whitespace
    TAGS_YAML="${TAGS_YAML}  - $tag\n"
done

# File paths
PROMPT_FILE="prompts/drafts/${DATE}_${SLUG}_draft.md"
ARTICLE_FILE="Post/${DATE}_${SLUG}_v01.0.md"

echo ""
echo "🚀 Generando file..."
echo ""
echo "   Prompt:   $PROMPT_FILE"
echo "   Articolo: $ARTICLE_FILE"
echo ""

# Create prompt draft
cat > "$PROMPT_FILE" <<EOF
# Prompt: $TITLE

## 🎯 Contesto e Obiettivo

[Descrivi il contesto e l'obiettivo dell'articolo]

Scrivi un articolo tecnico che analizza/esplora/compara [topic principale].

**Focus articolo:**
- [Punto chiave 1]
- [Punto chiave 2]
- [Punto chiave 3]

**Tone:** [Pragmatico/Tecnico/Divulgativo]

---

## 👥 Target Audience

**Lettore primario:**
- [Descrivi il lettore principale]

**Cosa il lettore SA:**
- [Prerequisiti assunti]

**Cosa il lettore VUOLE:**
- [Obiettivi del lettore]

---

## 📐 Struttura dell'Articolo

### 1. Introduzione (300-400 parole)
[Descrivi cosa includere]

### 2. [Sezione principale 1] (600-800 parole)
[Outline contenuto]

### 3. [Sezione principale 2] (600-800 parole)
[Outline contenuto]

### 4. [Approfondimenti pratici] (800-1000 parole)
[Esempi, codice, guide]

---

## 📝 Linee Guida per la Scrittura

### Tone & Style
- **DO**: [Best practices specifiche per questo articolo]
- **DON'T**: [Cosa evitare]

### Fonti da Consultare
- [Link documenta ufficiale]
- [Repository GitHub rilevanti]
- [Articoli di riferimento]

---

## ⚠️ Checklist Finale

- [ ] Titolo chiaro e SEO-friendly
- [ ] TL;DR completo e accurato
- [ ] Esempi concreti e verificabili
- [ ] Link a fonti ufficiali
- [ ] Codice testato (se presente)
- [ ] Cross-link ad articoli correlati
- [ ] Immagine header appropriata
- [ ] No sezione "Conclusione"
EOF

# Create article template
cat > "$ARTICLE_FILE" <<EOF
---
title: "$TITLE"
date: $DATE_FORMATTED
author: Davide Isoardi
categories: [$CATEGORY]
tags:
$(echo -e "$TAGS_YAML")
description: "[Descrizione SEO-friendly breve]"
---

**Riassunto**: [1-2 frasi riassunto per preview]

**TL;DR** - [Paragrafo esteso che riassume articolo: problema, contesto, soluzione/analisi, takeaway chiave]

---

## [Sezione 1]

[Contenuto introduttivo...]

## [Sezione 2]

[Contenuto principale...]

## [Sezione 3]

[Approfondimenti...]

---

**Fonti**:
- [Link fonte 1]
- [Link fonte 2]
EOF

echo "✅ File generati con successo!"
echo ""
echo "📂 File creati:"
echo "   - $PROMPT_FILE"
echo "   - $ARTICLE_FILE"
echo ""
echo "💡 Next steps:"
echo "   1. Compila il prompt in prompts/drafts/ con dettagli"
echo "   2. Usa Claude per generare contenuto basato su prompt"
echo "   3. Review e iterate in Post/"
echo "   4. Quando pronto:"
echo "      - Sposta in content/posts/ per Hugo"
echo "      - Migra prompt: ./scripts/migrate-prompt.sh ${DATE}_${SLUG}_draft.md $ARTICLE_FILE"
echo "   5. Cross-link: ./scripts/cross-link-checker.sh $ARTICLE_FILE"
echo ""
echo "🔗 Quick edit:"
echo "   code $PROMPT_FILE $ARTICLE_FILE"
