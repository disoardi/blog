# Home Assistant Release Monitor & Article Generator

Sistema automatizzato per monitorare le nuove release di Home Assistant e generare automaticamente articoli per il blog.

## 📋 Panoramica

Questo sistema:
1. Monitora periodicamente il blog ufficiale di Home Assistant
2. Rileva quando viene pubblicata la versione target (es. 2026.02)
3. Scarica e analizza il contenuto della release
4. Genera automaticamente un articolo utilizzando Claude API
5. Fa commit e push automatico del nuovo articolo su Git

## 🚀 Setup Iniziale

### 1. Requisiti

- Python 3.8 o superiore
- Git configurato nel repository del blog
- **Claude Code CLI installato e configurato** (comando `claude` disponibile)

### 2. Installazione Dipendenze

Se usi **Poetry** (raccomandato, come da linee guida):

```bash
cd /path/to/your/blog/automation
poetry init  # se non hai già un pyproject.toml
poetry add requests beautifulsoup4 PyYAML lxml
poetry install
```

Oppure con **pip** + virtualenv:

```bash
cd /path/to/your/blog/automation
python3 -m venv venv
source venv/bin/activate  # su Linux/Mac
# oppure: venv\Scripts\activate  # su Windows
pip install -r requirements.txt
```

### 3. Verifica Claude Code CLI

Il sistema usa **Claude Code CLI** invece delle API dirette. Verifica che sia installato:

```bash
claude --version
```

Dovresti vedere qualcosa come: `2.1.20 (Claude Code)`

Se non è installato, segui le istruzioni su: https://docs.anthropic.com/claude/docs/claude-code

**Vantaggi di usare Claude Code CLI:**
- ✅ Nessuna API key da gestire separatamente
- ✅ Usa la tua autenticazione Claude esistente
- ✅ Più semplice da configurare e mantenere
- ✅ Nessun costo aggiuntivo rispetto all'uso normale di Claude

### 4. Configurazione del Sistema

**IMPORTANTE**: Prima di tutto, crea il tuo file di configurazione locale:

```bash
cp config.yaml.example config.yaml
```

Poi modifica `config.yaml` con le tue impostazioni:

```yaml
blog:
  root_path: "/path/to/your/blog"  # Aggiorna con il path reale

monitoring:
  target_version: "2026.02"  # Cambia se vuoi monitorare una versione diversa
  check_interval_hours: 6  # Frequenza di controllo

git:
  auto_push: true  # false se vuoi solo commit locale
  branch: "main"  # o "master"
```

**📝 Nota sulla Privacy**: Il file `config.yaml` contiene percorsi locali e non deve essere committato su Git. È già incluso in `.gitignore` per proteggerlo. Usa sempre `config.yaml.example` come template per condividere la configurazione.

### 5. Test Manuale

Prima di attivare l'automazione, testa il sistema:

```bash
# Test di connessione e configurazione
poetry run python ha_release_monitor.py

# Oppure con venv:
source venv/bin/activate
python ha_release_monitor.py
```

Se vuoi testare la generazione su una release esistente:

```bash
poetry run python article_generator.py \
  "https://www.home-assistant.io/blog/2025/01/..." \
  "2025.01"
```

## ⚙️ Configurazione Automazione con Cron

### Setup Cron Job

Per eseguire il monitor ogni 6 ore:

```bash
# Apri il crontab editor
crontab -e
```

Aggiungi questa riga (adatta i path):

```cron
# Home Assistant Release Monitor - Esegui ogni 6 ore
0 */6 * * * cd /path/to/blog/automation && /path/to/poetry run python ha_release_monitor.py >> logs/cron.log 2>&1
```

Oppure se usi virtualenv:

```cron
0 */6 * * * cd /path/to/blog/automation && ./venv/bin/python ha_release_monitor.py >> logs/cron.log 2>&1
```

### Esempi di Scheduling Alternativo

```cron
# Ogni 3 ore
0 */3 * * * cd /path/to/blog/automation && poetry run python ha_release_monitor.py

# Una volta al giorno alle 10:00
0 10 * * * cd /path/to/blog/automation && poetry run python ha_release_monitor.py

# Due volte al giorno (mattina e sera)
0 9,21 * * * cd /path/to/blog/automation && poetry run python ha_release_monitor.py
```

### Verifica Cron Job Attivo

```bash
# Lista i cron job attivi
crontab -l

# Monitora i log
tail -f automation/logs/cron.log
```

## 📂 Struttura File

```
automation/
├── ha_release_monitor.py   # Script principale di monitoring
├── article_generator.py     # Modulo generazione articoli con Claude
├── git_manager.py           # Gestione commit e push automatici
├── config.yaml              # Configurazione sistema
├── requirements.txt         # Dipendenze Python
├── .env                     # API keys (non committare!)
├── .env.example             # Template per .env
├── README.md                # Questa documentazione
├── setup.sh                 # Script di setup automatico (opzionale)
├── logs/                    # Log di esecuzione
│   ├── ha_monitor.log
│   └── cron.log
└── temp/                    # File temporanei
    ├── monitor_state.json   # Stato del monitoring
    └── release_data.json    # Dati release scaricati
```

## 🔍 Come Funziona

### 1. Monitoring
- Lo script `ha_release_monitor.py` viene eseguito periodicamente
- Controlla https://www.home-assistant.io/blog/categories/core/
- Cerca la versione target nel titolo degli articoli

### 2. Rilevamento Release
- Quando trova la versione target, scarica il contenuto completo
- Salva le informazioni in `temp/release_data.json`
- Aggiorna lo stato in `temp/monitor_state.json`

### 3. Generazione Articolo
- Chiama l'API di Claude con il contenuto della release
- Usa le linee guida definite in `Claude.md`
- Genera l'articolo con focus su:
  - Integrazioni nuove
  - Automazioni e scripting
  - Performance e architettura

### 4. Pubblicazione
- Salva l'articolo in `Post/` con naming convention: `yyyyMMdd_home-assistant-202602_v01.0.md`
- Fa commit con messaggio descrittivo
- Push automatico (se abilitato)

## 🛠️ Manutenzione

### Monitorare i Log

```bash
# Log generale
tail -f automation/logs/ha_monitor.log

# Log cron
tail -f automation/logs/cron.log

# Filtra solo errori
grep ERROR automation/logs/ha_monitor.log
```

### Reset Stato (Rigenerare Articolo)

Se vuoi rigenerare l'articolo per la stessa versione:

```bash
rm automation/temp/monitor_state.json
```

### Aggiornamento Automatico della Versione Target ✨

**NOVITÀ**: Il sistema ora aggiorna automaticamente la versione target!

Quando rileva e processa con successo una release (es. 2026.02):
1. ✅ Genera l'articolo
2. ✅ Fa commit e push
3. ✅ **Calcola automaticamente la versione successiva** (2026.03)
4. ✅ **Aggiorna `config.yaml` automaticamente**
5. ✅ **Resetta lo stato per la nuova versione**
6. ✅ È pronto per monitorare la prossima release!

**Non devi fare nulla!** Il sistema si auto-configura per la versione successiva.

#### Aggiornamento Manuale (opzionale)

Se per qualche motivo vuoi forzare una versione specifica, puoi ancora farlo manualmente:

```yaml
monitoring:
  target_version: "2026.05"  # Salta qualche versione
```

E resetta lo stato:

```bash
rm automation/temp/monitor_state.json
```

### Cambiare Modello Claude

Per articoli più elaborati, usa Opus invece di Sonnet:

```yaml
claude:
  model: "claude-opus-4-5-20251101"  # Più costoso ma migliore qualità
```

## 🐛 Troubleshooting

### Problema: "ANTHROPIC_API_KEY not set"
**Soluzione**: Verifica che il file `.env` esista e contenga la chiave API.

```bash
cat .env
# Dovrebbe mostrare: ANTHROPIC_API_KEY=sk-ant-...
```

### Problema: Cron job non si esegue
**Soluzione**: Verifica i percorsi assoluti nel crontab

```bash
# Test manuale con gli stessi comandi del cron
cd /path/to/blog/automation && poetry run python ha_release_monitor.py
```

### Problema: Git push fallisce
**Soluzione**: Verifica le credenziali git

```bash
cd /path/to/blog
git config --list | grep user
git remote -v

# Test push manuale
git push origin main
```

### Problema: Articolo non generato
**Soluzione**: Controlla i log e verifica la risposta API

```bash
grep ERROR automation/logs/ha_monitor.log
tail -50 automation/logs/ha_monitor.log
```

## 📝 Note di Sicurezza

- ⚠️ **NON committare mai il file `.env`** (già in `.gitignore`)
- Le API key sono sensibili, tienile segrete
- Limita i permessi del file `.env`: `chmod 600 .env`
- Monitora l'uso della API su https://console.anthropic.com/

## 🎯 Prossimi Sviluppi

Possibili miglioramenti futuri:

- [ ] Notifiche Telegram/email quando viene rilevata una nuova release
- [ ] Supporto per multiple versioni da monitorare
- [ ] Download automatico di immagini dall'annuncio originale
- [ ] Integrazione con MkDocs per preview automatica
- [ ] Dashboard web per monitorare lo stato
- [ ] Backup automatico degli articoli generati

## 📧 Supporto

Per problemi o domande, consulta i log o contatta Davide Isoardi.

---

**Generato con ❤️ e Claude Sonnet 4.5**
