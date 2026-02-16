# Prompts Directory

Questa directory contiene i prompt utilizzati per la generazione degli articoli del blog.

## Struttura

```
prompts/
├── published/      # Prompt di articoli già pubblicati
├── drafts/         # Prompt in lavorazione (work in progress)
├── templates/      # Template riutilizzabili per tipologie di articoli
└── archive/        # Prompt vecchi/deprecati/scartati
```

## Naming Convention

### Prompt Pubblicati (`published/`)
**Formato**: `yyyyMMdd_slug-articolo_prompt.md`

Esempio:
- Prompt: `20260214_minio-maintenance-mode_prompt.md`
- Corrisponde all'articolo: `Post/20260214_minio-maintenance-mode_v01.0.md`

### Prompt Draft (`drafts/`)
**Formato**: `yyyyMMdd_slug-idea_draft.md`

Esempio:
- `20260215_kubernetes-storage_draft.md`

Mantiene la data di creazione dell'idea. Il suffix `_draft` indica work-in-progress.

### Template (`templates/`)
**Formato**: `tipo-template.md`

Esempio:
- `deep-dive-template.md` - Template per articoli deep-dive tecnici
- `comparison-template.md` - Template per comparazioni tecnologiche
- `news-analysis-template.md` - Template per analisi news/release

Template generici, senza data, riutilizzabili per categorie di articoli.

## Workflow

1. **Nuova idea** → Crea in `drafts/` con suffix `_draft.md`
2. **Articolo scritto e pubblicato** → Sposta prompt in `published/` rimuovendo `_draft`
3. **Idea scartata/obsoleta** → Sposta in `archive/`

## Best Practices

- **Mantieni corrispondenza**: Il nome del prompt dovrebbe matchare l'articolo pubblicato
- **Data consistency**: Usa la stessa data dell'articolo (yyyyMMdd)
- **Documentation**: Ogni prompt dovrebbe essere self-contained con contesto sufficiente
- **Version tracking**: Git history dei prompt permette di vedere evoluzione idee

## Esempio Lifecycle

```
# 1. Nuova idea
drafts/20260220_ai-privacy-concerns_draft.md

# 2. Articolo scritto
Post/20260220_ai-privacy-concerns_v01.0.md

# 3. Prompt migrato
published/20260220_ai-privacy-concerns_prompt.md
```

---

**Note**: I prompt sono documentazione preziosa per capire il processo di creazione degli articoli e possono essere riutilizzati/adattati per contenuti futuri.
