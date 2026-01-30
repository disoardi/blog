# 🚀 Quickstart Guide

Guida rapida per attivare il sistema in 5 minuti.

## Setup Veloce

### 1. Esegui lo script di setup automatico

```bash
cd /path/to/blog/automation
./setup.sh
```

Lo script farà:
- ✅ Controllo dipendenze Python
- ✅ Installazione pacchetti (con Poetry o pip)
- ✅ Creazione file .env
- ✅ Configurazione directories
- ✅ Test iniziali

### 2. Configura la tua API Key

Quando richiesto durante il setup, inserisci la tua API key di Anthropic.

Oppure modificala manualmente:

```bash
nano .env
```

Sostituisci `your_api_key_here` con la tua chiave da https://console.anthropic.com/

### 3. Test Manuale

Prima di attivare l'automazione, testa il sistema:

```bash
# Con Poetry
poetry run python test_system.py

# Con venv
source venv/bin/activate
python test_system.py
```

Tutti i test dovrebbero passare ✅

### 4. Attiva il Cron Job

Apri il crontab:

```bash
crontab -e
```

Aggiungi questa riga (aggiorna i path):

```cron
# Check ogni 6 ore per nuove release di Home Assistant
0 */6 * * * cd /path/to/blog/automation && /path/to/poetry run python ha_release_monitor.py >> logs/cron.log 2>&1
```

Salva e esci.

### 5. Verifica lo Stato

```bash
./check_status.sh
```

Dovresti vedere:
- ✅ API key configurata
- ✅ Target version impostata
- ✅ Cron job attivo

## ✅ Fatto!

Il sistema ora:
- 🔍 Controlla automaticamente ogni 6 ore se è uscita la versione 2026.02
- 📝 Genera un articolo quando la trova
- 🚀 Fa commit e push automatico

## Monitoraggio

Controlla i log:

```bash
# Log monitor
tail -f automation/logs/ha_monitor.log

# Log cron
tail -f automation/logs/cron.log
```

## Prossima Release

Quando esce la versione successiva (es. 2026.03), aggiorna `config.yaml`:

```yaml
monitoring:
  target_version: "2026.03"
```

E resetta lo stato:

```bash
rm automation/temp/monitor_state.json
```

---

📚 **Per documentazione completa**: leggi [README.md](README.md)
