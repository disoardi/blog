# 📋 Changelog - Sistema Semplificato

## 🔄 Cambiamenti Principali

### ❌ Rimosso (Automazione Completa)
- Build Hugo automatica
- Commit e push Git automatico
- Auto-incremento versione target
- Gestione git_manager.py

### ✅ Mantenuto (Workflow Semi-Automatico)
- Monitoring release Home Assistant
- Download contenuto release
- Generazione articolo con Claude Code CLI
- Salvataggio in Post/

### 🎯 Nuovo Workflow

**Prima (Automazione Completa)**:
```
Monitor → Download → Genera → Hugo Build → Git Commit → Git Push → Auto-incremento
```

**Ora (Semi-Automatico)**:
```
Monitor → Download → Genera → STOP

Tu: Rivedi → Hugo → Git → Push
```

## 📝 Cosa Fare Ora

### Test Veloce

```bash
cd /Users/disoardi/Progetti/blog/automation

# Pulisci
rm -f temp/*.json
rm -f ../Post/20260130_home-assistant-20262_v01.0.md

# Esegui
poetry run python ha_release_monitor.py
```

**Output Atteso**:
```
✅ Article generated successfully!
📄 Location: /Users/disoardi/Progetti/blog/Post/[filename].md

Next steps:
1. Review the article
2. Make any edits if needed
3. Build with Hugo: hugo
4. Commit and push manually when ready
```

### Verifica Articolo Generato

```bash
# Leggi l'articolo
cat ../Post/*home-assistant-*.md | head -50

# Dovrebbe contenere un vero articolo, non:
# - "How can I help"
# - "I'm ready to"
# - "Posso aiutarti"
```

### Pubblica Manualmente

```bash
cd /Users/disoardi/Progetti/blog

# 1. Rivedi articolo
nano Post/[nome-articolo].md

# 2. Build Hugo
hugo

# 3. Commit
git add Post/[nome-articolo].md public/
git commit -m "Nuovo articolo: Home Assistant 2026.2"

# 4. Push
git push origin main
```

## 🗑️ File da Archiviare/Ignorare

Questi file non servono più ma sono lasciati per reference:
- `git_manager.py`
- `setup.sh`
- `install_cron.sh`
- `README.md` (vecchio)
- `DEPLOYMENT_SUMMARY.md` (vecchio)
- `QUICKSTART.md` (vecchio)
- `TEST_INSTRUCTIONS.md` (vecchio)

**Nuovo file da usare**: `README_SIMPLE.md`

## 💡 Vantaggi

✅ **Più Semplice** - Meno codice, meno complessità
✅ **Più Controllo** - Rivedi prima di pubblicare
✅ **Più Sicuro** - Nessun push automatico
✅ **Più Flessibile** - Modifica articolo come vuoi
✅ **Meno Rischi** - Niente build/commit che possono fallire

## 🔧 Configurazione Pulita

Il nuovo `config.yaml` è più semplice:

```yaml
blog:
  root_path: /Users/disoardi/Progetti/blog
  post_dir: Post
  img_dir: img

monitoring:
  target_version: '2026.2'
  ha_blog_url: https://www.home-assistant.io/blog/categories/core/
  check_interval_hours: 6
  state_file: automation/temp/monitor_state.json

claude:
  model: claude-sonnet-4-5-20250929
  max_tokens: 8000
  temperature: 0.7

logging:
  level: INFO
  log_dir: automation/logs
```

Rimosso:
- ~~git.auto_push~~
- ~~git.branch~~

## 📖 Per Maggiori Info

Leggi: `README_SIMPLE.md`
