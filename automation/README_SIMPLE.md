# 📝 Home Assistant Article Generator - Workflow Semplificato

Sistema semi-automatizzato per generare articoli sulle release di Home Assistant.

## 🎯 Come Funziona

1. **Script monitora** il blog di Home Assistant
2. **Rileva** quando esce una nuova versione
3. **Scarica** il contenuto della release
4. **Genera** un articolo usando Claude Code CLI
5. **Si ferma** - tu rivedi e pubblichi manualmente

## 🚀 Setup Iniziale

### 1. Installa Dipendenze

```bash
cd /Users/disoardi/Progetti/blog/automation

# Con Poetry (raccomandato)
poetry install

# Oppure con pip
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Verifica Claude Code CLI

```bash
claude --version
```

Deve essere installato: https://docs.anthropic.com/claude/docs/claude-code

### 3. Configura Path Blog

Modifica `config.yaml`:

```yaml
blog:
  root_path: "/Users/disoardi/Progetti/blog"  # Il tuo path
```

## 📖 Utilizzo

### Esecuzione Manuale

Quando sai che è uscita una nuova release:

```bash
cd /Users/disoardi/Progetti/blog/automation

# 1. Aggiorna la versione target in config.yaml
nano config.yaml
# Imposta: target_version: "2026.2"

# 2. Pulisci stato precedente (se vuoi rigenerare)
rm -f temp/monitor_state.json temp/release_data.json

# 3. Esegui
poetry run python ha_release_monitor.py
```

**Output**:
```
✅ Article generated successfully!
📄 Location: /Users/disoardi/Progetti/blog/Post/20260130_home-assistant-20262_v01.0.md

Next steps:
1. Review the article: [path]
2. Make any edits if needed
3. Build with Hugo: hugo
4. Commit and push manually when ready
```

### Esecuzione Automatica (Cron - Opzionale)

Se vuoi che lo script controlli periodicamente:

```bash
# Apri crontab
crontab -e

# Aggiungi (esegue ogni 6 ore)
0 */6 * * * cd /Users/disoardi/Progetti/blog/automation && poetry run python ha_release_monitor.py >> logs/cron.log 2>&1
```

Lo script:
- ✅ Controlla se c'è la nuova release
- ✅ Genera l'articolo se la trova
- ✅ Non rigenera se l'ha già fatto
- ⏸️  Si ferma - tu decidi quando pubblicare

## 📋 Workflow Completo

```
1. Script trova release 2026.2
   ↓
2. Scarica contenuto da home-assistant.io
   ↓
3. Genera articolo con Claude Code CLI
   (seguendo le linee guida in Claude.md)
   ↓
4. Salva in Post/yyyyMMdd_home-assistant-20262_v01.0.md
   ↓
5. TU prendi il controllo:
   ├─ Rivedi articolo
   ├─ Fai modifiche se necessarie
   ├─ hugo (build)
   ├─ git add Post/articolo.md public/
   ├─ git commit -m "..."
   └─ git push
```

## 🔧 Struttura File

```
automation/
├── ha_release_monitor.py    # Script principale
├── article_generator.py      # Generazione articolo con Claude CLI
├── config.yaml               # Configurazione
├── requirements.txt          # Dipendenze Python
├── logs/                     # Log esecuzione
└── temp/                     # File temporanei
    ├── monitor_state.json    # Stato (versioni già processate)
    └── release_data.json     # Dati release scaricati
```

## 🎨 Personalizzazione Stile

Lo script usa le linee guida in `../Claude.md` (sezione "Linee Guida per Claude - writer degli articoli").

Gli articoli riflettono:
- ✅ Tono colloquiale e personale
- ✅ Prospettiva: nerd old-school, FOSS, self-hosting
- ✅ Passioni: Star Trek, D&D, giochi da tavolo
- ✅ Focus: integrazioni, automazioni, performance

## 🔍 Monitoraggio

### Visualizza Log

```bash
# Log completo
cat logs/ha_monitor.log

# Ultimi check
tail -20 logs/ha_monitor.log

# Solo errori
grep ERROR logs/ha_monitor.log
```

### Stato Corrente

```bash
# Vedi quale versione è stata processata
cat temp/monitor_state.json | python -m json.tool
```

## 🔄 Per la Prossima Versione

```bash
# 1. Aggiorna config.yaml
nano config.yaml
# Cambia: target_version: "2026.3"

# 2. Pulisci stato
rm temp/monitor_state.json

# 3. Esegui
poetry run python ha_release_monitor.py
```

## ⚠️ Troubleshooting

### "Claude CLI returned conversational response"

Claude sta rispondendo in modo conversazionale invece di generare l'articolo.

**Soluzione**: Assicurati che Claude Code CLI sia aggiornato:
```bash
claude --version
```

### "Target version X not yet released"

La versione non è ancora sul sito Home Assistant.

**Verifica manualmente**: https://www.home-assistant.io/blog/categories/core/

### "Module not found"

```bash
# Reinstalla dipendenze
poetry install
# oppure
pip install -r requirements.txt
```

## 📚 File Deprecati

Questi file erano per l'automazione completa (ora rimossa):
- `git_manager.py` - Gestione git automatica
- `setup.sh` - Setup automazione completa
- `install_cron.sh` - Installazione cron automatico
- `README.md` (vecchio) - Documentazione automazione completa

Ora usi solo:
- `ha_release_monitor.py` - Monitor + generazione
- `article_generator.py` - Generatore articoli
- `config.yaml` - Configurazione
- Questo README

## 🎉 Vantaggi Workflow Semi-Automatico

✅ **Controllo Totale** - Rivedi ogni articolo prima di pubblicare
✅ **Flessibilità** - Modifica l'articolo come preferisci
✅ **Sicurezza** - Nessun push automatico indesiderato
✅ **Semplicità** - Meno componenti, meno cose che possono rompersi
✅ **Stile Coerente** - Claude segue le tue linee guida in Claude.md

---

**Domande?** Controlla i log in `logs/ha_monitor.log`
