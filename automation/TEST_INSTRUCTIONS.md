# 🧪 Istruzioni per Test sul Computer Reale

**Nota**: Nell'ambiente VM di Cowork c'è un blocco di rete che impedisce di accedere a home-assistant.io.
Sul tuo computer reale questo problema non ci sarà.

## ✅ Test Rapido (Consigliato)

### 1. Test Manuale del Sistema

```bash
cd /path/to/blog/automation

# Test con dati simulati (funziona anche offline)
python3 test_with_mock_data.py
```

Questo dovrebbe mostrare:
- ✅ Version Increment: PASSED
- ✅ Article Generation: PASSED

### 2. Test con Release Reale

```bash
# Assicurati che config.yaml abbia target_version: "2026.01"
grep target_version config.yaml

# Esegui il monitor una volta
python3 ha_release_monitor.py
```

**Cosa dovrebbe succedere**:
1. Script scarica la release notes di Home Assistant 2026.01
2. Genera un articolo usando Claude Code CLI
3. Salva l'articolo in `../Post/20260129_home-assistant-202601_v01.0.md`
4. Fa git commit e push automatico
5. **Auto-aggiorna config.yaml a versione 2026.02**
6. Sistema pronto per monitorare 2026.02!

### 3. Verifica Risultati

```bash
# Controlla che l'articolo sia stato creato
ls -lh ../Post/*home-assistant*.md

# Verifica il commit git
cd ..
git log -1

# Verifica che la versione sia stata aggiornata
grep target_version automation/config.yaml
# Dovrebbe mostrare: target_version: "2026.02"

# Controlla lo stato salvato
cat automation/temp/monitor_state.json
```

## 🔧 Installazione Cron Job

Una volta verificato che tutto funziona:

```bash
cd /path/to/blog/automation

# Installa il cron job automaticamente
./install_cron.sh
```

Lo script:
- ✅ Rileva automaticamente se usi Poetry o venv
- ✅ Configura il cron job con path assoluti
- ✅ Imposta esecuzione ogni 6 ore
- ✅ Configura logging automatico

### Verifica Cron Job Installato

```bash
# Visualizza il cron job
crontab -l | grep ha_release

# Monitora i log
tail -f automation/logs/cron.log

# Test immediato (forzato)
cd /path/to/blog/automation && python3 ha_release_monitor.py
```

## 📊 Scenario di Test Completo

### Test 1: Release 2026.01 (già uscita)

```bash
# 1. Imposta target su 2026.01
nano automation/config.yaml
# Cambia: target_version: "2026.01"

# 2. Pulisci lo stato
rm -f automation/temp/monitor_state.json

# 3. Esegui
cd automation
python3 ha_release_monitor.py

# 4. Verifica risultati
ls ../Post/*202601*.md
grep target_version config.yaml  # Dovrebbe dire 2026.02 ora
```

### Test 2: Attesa Prossima Release

```bash
# Il sistema ora è configurato su 2026.02
# Quando uscirà 2026.02 (febbraio 2026):
# 1. Cron job eseguirà automaticamente
# 2. Genererà l'articolo
# 3. Auto-aggiornerà a 2026.03
# 4. Continuerà all'infinito!
```

## 🔍 Monitoraggio

### Log del Monitor

```bash
# Visualizza log completo
cat automation/logs/ha_monitor.log

# Solo ultimi check
tail -20 automation/logs/ha_monitor.log

# Filtra errori
grep ERROR automation/logs/ha_monitor.log

# Monitoraggio real-time
tail -f automation/logs/ha_monitor.log
```

### Log Cron

```bash
# Visualizza esecuzioni cron
cat automation/logs/cron.log

# Ultime esecuzioni
tail -50 automation/logs/cron.log

# Monitoraggio real-time
tail -f automation/logs/cron.log
```

### Stato Sistema

```bash
# Visualizza stato corrente
cat automation/temp/monitor_state.json | python3 -m json.tool

# Esempio output:
# {
#   "last_checked_version": "2026.02",
#   "article_generated": false,
#   "previous_version": "2026.01",
#   "previous_article_path": "../Post/...",
#   "previous_generation_date": "2026-01-29T...",
#   "auto_incremented": true
# }
```

## ⚠️ Troubleshooting

### Problema: "Claude CLI not available"

```bash
# Verifica installazione
claude --version

# Se non installato:
# https://docs.anthropic.com/claude/docs/claude-code
```

### Problema: "Module not found"

```bash
# Reinstalla dipendenze
cd automation
poetry install

# Oppure con pip
pip install -r requirements.txt
```

### Problema: "Permission denied" per config.yaml

```bash
# Verifica permessi
ls -l automation/config.yaml

# Se necessario
chmod 644 automation/config.yaml
```

### Problema: Git push fallisce

```bash
# Verifica credenziali git
cd /path/to/blog
git config --list | grep user

# Test push manuale
git push origin main
```

### Problema: Cron non si esegue

```bash
# Verifica che cron sia attivo
sudo systemctl status cron  # Linux
# oppure
sudo launchctl list | grep cron  # macOS

# Usa path assoluti nel crontab
crontab -e
# Esempio:
# 0 */6 * * * /usr/bin/python3 /full/path/to/automation/ha_release_monitor.py
```

## 🎯 Checklist Test Completo

Prima di considerare il sistema pronto per produzione:

- [ ] Test con dati simulati passa
- [ ] Test con release reale (2026.01) passa
- [ ] Articolo generato correttamente
- [ ] Git commit & push funziona
- [ ] Versione auto-aggiornata a 2026.02
- [ ] Stato salvato correttamente
- [ ] Cron job installato
- [ ] Log accessibili e leggibili
- [ ] Test manuale del cron (con esecuzione forzata)

## 🚀 Quando Tutto Funziona

Una volta completati i test:

1. ✅ **Lascia il cron job attivo**
2. ✅ **Il sistema farà tutto da solo**
3. ✅ **Ogni release sarà automaticamente documentata**
4. ✅ **La versione si auto-aggiorna**
5. ✅ **Non serve più intervento manuale!**

### Monitoraggio Periodico (Opzionale)

```bash
# Una volta a settimana/mese, controlla:

# 1. Stato sistema
grep target_version automation/config.yaml
cat automation/temp/monitor_state.json

# 2. Articoli generati
ls -lt Post/*home-assistant*.md | head -5

# 3. Log recenti
tail -50 automation/logs/cron.log

# 4. Commit recenti
git log --grep="home-assistant" --oneline -5
```

## 📞 Hai Problemi?

1. Controlla `automation/logs/ha_monitor.log`
2. Esegui `python3 test_with_mock_data.py`
3. Verifica la configurazione in `config.yaml`
4. Consulta `README.md` per documentazione completa

---

**Buon testing! 🎉**

*Ricorda: il sistema è progettato per funzionare autonomamente. Una volta testato e attivato il cron, puoi dimenticartene!*
