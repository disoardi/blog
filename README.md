# 🚀 Davide Isoardi - Tech Blog

Blog personale costruito con [Hugo](https://gohugo.io/) e il tema [PaperMod](https://github.com/adityatelange/hugo-PaperMod), con un tocco di Star Trek.

## 🖖 Benvenuto a bordo

Questo è il repository del mio blog tecnologico dove esploro innovazione, open source, big data e riflessioni sulla tecnologia.

**Live site**: [disoardi.github.io/blog](https://disoardi.github.io/blog/)

> 🚧 Dominio personalizzato `isoardi.info` sarà configurato successivamente.

## 📦 Stack Tecnologico

- **Generator**: Hugo (extended) v0.155.0
- **Theme**: PaperMod (git submodule)
- **Hosting**: GitHub Pages
- **CI/CD**: GitHub Actions
- **Style**: Custom LCARS-inspired CSS
- **Language**: Italiano

## 🛠️ Setup Locale

### Prerequisiti

- Hugo extended (installato via Homebrew su macOS)
- Git

### Installazione

```bash
# Clone del repository con submodule
git clone --recursive https://github.com/disoardi/blog.git
cd blog

# Se hai già clonato senza --recursive
git submodule update --init --recursive
```

### Server di Sviluppo

```bash
# Avvia il server locale (include bozze)
hugo server -D

# Senza bozze
hugo server

# Il sito sarà disponibile su http://localhost:1313/
```

### Build Produzione

```bash
# Build del sito statico
hugo --gc --minify

# Output in ./public/
```

## ✍️ Creare Nuovi Articoli

### Metodo Rapido (Script Helper)

```bash
# Crea nuovo post con naming convention corretta
./new-post.sh "Titolo del Mio Articolo" 01.0

# Genera: content/posts/yyyyMMdd_titolo-del-mio-articolo_v01.0.md
```

### Metodo Manuale

```bash
hugo new posts/20260129_mio-articolo_v01.0.md
```

### Convenzioni di Naming

Formato: `yyyyMMdd_titolo_vXX.Y.md`

Esempio: `20260129_paradosso-ai-competenze_v01.0.md`

- `yyyyMMdd`: Data di creazione
- `titolo`: Titolo in kebab-case
- `vXX.Y`: Versione (es. v01.0, v01.1, v02.0)

### Front Matter Template

```yaml
---
title: "Titolo dell'Articolo"
date: 2026-01-29
author: Davide Isoardi
categories: [Categoria1, Categoria2]
tags: [tag1, tag2, tag3]
description: "Descrizione breve per SEO"
cover:
  image: /img/20260129_titolo_header.jpg
  alt: "Alt text per l'immagine"
  relative: false
draft: false
---

**Riassunto**: [1-2 frasi]

**TL;DR**: [Riassunto esteso]

---

Contenuto dell'articolo...
```

## 📁 Struttura Directory

```
blog/
├── .github/
│   └── workflows/
│       └── deploy.yml        # GitHub Actions per deploy
├── archetypes/
│   └── post.md              # Template per nuovi post
├── assets/
│   └── css/
│       └── extended/
│           └── trek-theme.css # Stili Star Trek personalizzati
├── content/
│   ├── posts/               # Articoli del blog
│   └── about.md             # Pagina About
├── static/
│   └── img/                 # Immagini (copiate da /img/)
├── themes/
│   └── PaperMod/            # Tema (git submodule)
├── hugo.toml                # Configurazione Hugo
├── new-post.sh              # Script helper per nuovi post
└── README.md
```

## 🎨 Customizzazioni

### Tema Star Trek

Il tema include customizzazioni CSS ispirate al sistema LCARS di Star Trek:

- Colori accent arancione (#FF9966) e blu (#9999FF)
- Bordi e transizioni LCARS-style
- Effetti hover sui link e bottoni
- Styling delle citazioni e del codice

File: `assets/css/extended/trek-theme.css`

### Modificare gli Stili

Per personalizzare ulteriormente, modifica o aggiungi CSS in:

```bash
assets/css/extended/
```

Hugo automaticamente concatenerà questi file con gli stili del tema.

## 🚀 Deploy e Pubblicazione

### GitHub Pages (Automatico)

Il deploy avviene automaticamente tramite GitHub Actions:

1. **Push su `main`** → Trigger automatico
2. **Build con Hugo** → Genera sito statico
3. **Deploy su GitHub Pages** → Pubblicazione

Workflow: `.github/workflows/deploy.yml`

### Configurare GitHub Pages

1. Vai su `Settings` → `Pages` nel repository
2. Source: **GitHub Actions**
3. Il sito sarà disponibile su `https://disoardi.github.io/blog/`

### Dominio Personalizzato

Per usare `isoardi.info`:

1. Aggiungi `CNAME` file in `static/`:
   ```bash
   echo "isoardi.info" > static/CNAME
   ```
2. Configura DNS:
   - `A record` → GitHub Pages IPs
   - O `CNAME` → `disoardi.github.io`

## 📝 Workflow di Scrittura

1. **Brainstorming** con Claude per idee articoli
2. **Creare nuovo post**:
   ```bash
   ./new-post.sh "Titolo Articolo"
   ```
3. **Scrivere contenuto** in Markdown (con Claude)
4. **Aggiungere immagine header** in `static/img/`
5. **Preview locale**:
   ```bash
   hugo server -D
   ```
6. **Rivedere e iterare** il contenuto
7. **Pubblicare**: set `draft: false` e commit
8. **Deploy automatico** via GitHub Actions

## 🔧 Comandi Utili

```bash
# Server sviluppo con draft
hugo server -D

# Server senza draft
hugo server

# Build production
hugo --gc --minify

# Nuovo post
./new-post.sh "Titolo" 01.0

# Check Hugo version
hugo version

# Update tema PaperMod
git submodule update --remote --merge
```

## 📚 Categorie Principali

- **Big Data & Hadoop** - HDFS, Spark, ecosistema Hadoop
- **Open Source** - Software libero, ILS, Linux Day
- **AI & Machine Learning** - Riflessioni su AI e competenze
- **Self-Hosting** - Progetti homelab
- **Riflessioni Tech** - Pensieri e analisi tecnologiche
- **Sci-Fi & Tech Culture** - Star Trek e paralleli tecnologici

## 🤝 Contributi

Questo è un blog personale, ma se trovi typo o errori, sentiti libero di aprire una issue o PR!

## 📄 Licenza

Contenuto: © 2026 Davide Isoardi
Codice del sito: MIT (vedi tema PaperMod per dettagli)

## 🔗 Links

- **Blog**: [disoardi.github.io/blog](https://disoardi.github.io/blog/)
- **GitHub**: [@disoardi](https://github.com/disoardi)
- **Hugo Docs**: [gohugo.io](https://gohugo.io/)
- **PaperMod Docs**: [adityatelange.github.io/hugo-PaperMod](https://adityatelange.github.io/hugo-PaperMod/)

---

*"Resistance is futile... but learning is essential."* 🖖
