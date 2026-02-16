## Automation Scripts per Blog Workflow

Questa directory contiene script helper per automatizzare task ripetitivi nel workflow di creazione e pubblicazione articoli.

## 📜 Script Disponibili

### 1. `new-article.sh` - Crea Nuovo Articolo

Genera template per nuovo articolo + prompt draft con naming convention corretta.

**Usage**:
```bash
./scripts/new-article.sh [slug]

# Interactive mode (no slug provided)
./scripts/new-article.sh

# Direct mode
./scripts/new-article.sh minio-maintenance-mode
```

**Output**:
- `prompts/drafts/yyyyMMdd_slug_draft.md` - Template prompt dettagliato
- `Post/yyyyMMdd_slug_v01.0.md` - Template articolo con front matter

**Workflow**:
1. Esegui script → Compila prompt con dettagli
2. Usa Claude per generare contenuto basato su prompt
3. Review e iterate articolo in `Post/`
4. Sposta in `content/posts/` quando pronto per pubblicazione

---

### 2. `cross-link-checker.sh` - Suggerisce Cross-Link

Analizza nuovo articolo e suggerisce articoli esistenti che potrebbero linkarlo.

**Usage**:
```bash
./scripts/cross-link-checker.sh path/to/new-article.md

# Example
./scripts/cross-link-checker.sh Post/20260214_minio-maintenance-mode_v01.0.md
```

**Come funziona**:
1. Estrae tag dal front matter del nuovo articolo
2. Grep keyword in articoli esistenti (`Post/` e `content/`)
3. Mostra preview di dove il topic viene menzionato
4. Suggerisce articoli da aggiornare per cross-linking

**Best Practice**:
- Esegui DOPO aver scritto nuovo articolo
- Review suggerimenti e aggiungi link dove rilevante
- Aggiungi `lastmod: YYYY-MM-DD` agli articoli aggiornati

**Requirements**:
- `yq` (optional, per parsing YAML - fallback a grep se non disponibile)

---

### 3. `migrate-prompt.sh` - Migra Prompt Draft → Published

Sposta prompt da `prompts/drafts/` a `prompts/published/` con naming convention corretta.

**Usage**:
```bash
./scripts/migrate-prompt.sh <draft-filename> <published-article-path>

# Example
./scripts/migrate-prompt.sh 20260214_minio_draft.md Post/20260214_minio-maintenance-mode_v01.0.md
```

**Come funziona**:
1. Estrae date e slug dall'articolo pubblicato
2. Rinomina prompt con naming convention: `yyyyMMdd_slug_prompt.md`
3. Sposta da `drafts/` a `published/`
4. Verifica consistency naming con articolo

**Quando usare**:
- Dopo pubblicazione articolo in `content/posts/`
- Prima del commit finale (per archiviare prompt con articolo)

---

### 4. `download-header-image.sh` - Scarica Immagine Header

Download immagine header da Unsplash con naming convention corretta.

**Usage**:
```bash
./scripts/download-header-image.sh <unsplash-url> <article-date> <article-slug>

# Example
./scripts/download-header-image.sh \
  'https://images.unsplash.com/photo-XXXXX?w=1200&q=80' \
  20260214 \
  minio-maintenance-mode
```

**Come trovare URL Unsplash**:
1. Vai su [unsplash.com](https://unsplash.com)
2. Cerca tema articolo (es. "data center", "server", etc.)
3. Seleziona immagine → Right-click → Copy Image Address
4. Usa URL formato: `https://images.unsplash.com/photo-XXXXX?w=1200&q=80`

**Output**:
- Scarica in: `static/img/yyyyMMdd_slug_header.jpg`
- Genera front matter da copy-paste nell'articolo

**Best Practice**:
- Usa immagini width=1200 per good quality
- q=80 è optimal trade-off quality/size
- Unsplash = free, no attribution required (ma nice to credit)

---

## 🔄 Workflow Completo

### Creazione Nuovo Articolo

```bash
# 1. Genera template articolo + prompt
./scripts/new-article.sh kubernetes-storage

# 2. Compila prompt con dettagli (usa editor)
code prompts/drafts/20260214_kubernetes-storage_draft.md

# 3. Claude genera contenuto basato su prompt
# (interazione con Claude Code)

# 4. Review articolo generato
code Post/20260214_kubernetes-storage_v01.0.md

# 5. Scarica immagine header
./scripts/download-header-image.sh \
  'https://images.unsplash.com/photo-XXXXX?w=1200&q=80' \
  20260214 \
  kubernetes-storage

# 6. Aggiungi cover al front matter (output script punto 5)

# 7. Copia articolo in Hugo content
cp Post/20260214_kubernetes-storage_v01.0.md content/posts/

# 8. Check cross-link opportunities
./scripts/cross-link-checker.sh Post/20260214_kubernetes-storage_v01.0.md

# 9. Update articoli correlati se necessario (manuale)

# 10. Migra prompt da draft a published
./scripts/migrate-prompt.sh \
  20260214_kubernetes-storage_draft.md \
  Post/20260214_kubernetes-storage_v01.0.md

# 11. Commit tutto
git add Post/ content/posts/ prompts/ static/img/
git commit -m "📝 Pubblica articolo Kubernetes storage"
git push
```

---

## 📦 Installazione Dipendenze (Opzionali)

### yq (YAML parser)

**macOS (Homebrew)**:
```bash
brew install yq
```

**Linux**:
```bash
# Download binary from GitHub releases
wget https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 -O /usr/local/bin/yq
chmod +x /usr/local/bin/yq
```

**Note**: `cross-link-checker.sh` funziona anche senza `yq` (fallback a grep), ma `yq` fornisce parsing YAML più robusto.

---

## 🐛 Troubleshooting

### Permessi Negati

```bash
# Rendi tutti gli script eseguibili
chmod +x scripts/*.sh
```

### Script Non Trova File

Assicurati di eseguire script dalla **root del repository**:

```bash
# ✅ Correct
./scripts/cross-link-checker.sh Post/article.md

# ❌ Wrong (da dentro scripts/)
cd scripts
./cross-link-checker.sh Post/article.md  # fails
```

### Grep Non Trova Articoli

- Verifica che articoli abbiano tag nel front matter
- Cross-link-checker usa tag per matching
- Se nessun tag presente, aggiungi manualmente

---

## 🚀 Future Enhancements

Possibili miglioramenti future:

- **Auto cross-link**: Script che suggerisce E applica automaticamente link (con review)
- **Image search**: Integrazione API Unsplash per search diretto da command line
- **Git hooks**: Pre-commit hook che verifica naming convention e metadata
- **Hugo preview**: Script che lancia Hugo server + apre browser
- **Prompt templates**: Template specializzati per tipo articolo (comparison, deep-dive, news)

---

## 📝 Contributing

Se aggiungi nuovi script:
1. Segui naming convention: `verb-noun.sh` (es. `check-links.sh`)
2. Includi usage help (run senza args → mostra help)
3. Usa `set -euo pipefail` per error handling robusto
4. Aggiungi documentazione in questo README
5. Testa su macOS e Linux se possibile

---

**Last Updated**: 2026-02-16
