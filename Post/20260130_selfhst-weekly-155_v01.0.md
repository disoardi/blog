---
title: "Self-Host Weekly #155: Le Novità che Contano per Chi si Auto-Ospita"
date: 2026-01-30
author: Davide Isoardi
categories: [Self-Hosting, Open Source]
tags: [self-hosting, homelab, backup, calibre, rackula, repoflow, zerobyte, openclaw, fosdem]
description: "Analisi delle novità più interessanti dalla Self-Host Weekly #155: da OpenClaw che rivoluziona l'AI self-hosted, a Calibre-Web Automated 4.0 con le Magic Shelves, fino a Zerobyte per backup intelligenti"
cover:
  image: img/20260130_selfhst-weekly-155_header.jpg
  alt: "Self-Hosting e Homelab"
  relative: false
---

**Riassunto**: Questa settimana nel mondo self-hosting troviamo OpenClaw che porta l'AI a casa nostra con oltre 100k stelle su GitHub, Calibre-Web Automated 4.0 con funzionalità quasi magiche per gestire gli ebook, e una serie di tool che semplificano la vita a noi homelabber.

**TL;DR**: Self-Host Weekly #155 porta novità sostanziose: OpenClaw emerge come soluzione AI self-hosted seria (ex Clawdbot, 100k+ stelle GitHub), Calibre-Web Automated 4.0 introduce Magic Shelves e gestione duplicati automatica, Rackula diventa lo standard per visualizzare rack fisici, RepoFlow gestisce pacchetti software di ogni tipo, Zerobyte semplifica i backup con Restic. FOSDEM 2026 è alle porte ma quest'anno passo - anche perché al Delirium Café potrebbero esserci troppi fan di nano.

---

## La Newsletter che Non Ti Aspetti di Leggere

Ogni settimana [selfh.st](https://selfh.st/) pubblica una raccolta di novità dal mondo self-hosting che, diciamocelo, è una specie di droga per noi nerd che preferiamo avere il controllo sui nostri dati piuttosto che affidarli al cloud di turno. La [weekly #155](https://selfh.st/weekly/2026-01-30/) non fa eccezione e anzi, questa volta ci sono robe davvero interessanti.

Prima però una nota personale: FOSDEM 2026 è praticamente domani (1-2 febbraio a Bruxelles), ma quest'anno non ci sarò. Non fraintendetemi, è un evento fantastico per chi ama l'open source, ma diciamo che dopo aver scoperto che al Delirium Café potrebbero esserci troppi utenti di nano... beh, ho preferito evitare. Vim è l'unica via, punto.

## OpenClaw: Quando l'AI Diventa Self-Hosted (Sul Serio)

Se c'è una cosa che mi ha colpito in questa weekly, è OpenClaw. Prima si chiamava Clawdbot, poi Moltbot, ora finalmente OpenClaw - e a giudicare dalle **oltre 100.000 stelle su GitHub**, direi che non sono l'unico ad averlo notato.

Ma cos'è esattamente? È un agente AI che gira completamente in locale, sul tuo hardware. Niente cloud, niente API key da pagare a peso d'oro, niente preoccupazioni su chi legge i tuoi prompt. Lo installi, scegli il modello LLM che preferisci (è model-agnostic, quindi funziona con Ollama, LM Studio, o qualsiasi cosa tu abbia), e parte.

La parte bella è che si integra con tutto: WhatsApp, Telegram, Discord, Slack. Praticamente puoi avere il tuo assistente AI personale che risponde ovunque tu sia, ma che in realtà gira sul tuo server in cantina o sul Raspberry Pi sotto la TV. Questo per me è il vero spirito del self-hosting.

Ho dato un'occhiata al [repository su GitHub](https://github.com/openclaw/openclaw) e devo dire che il progetto sembra maturo. Certo, non è semplicissimo da configurare se non hai già familiarità con i modelli LLM locali, ma se hai già un setup con Ollama o simili, ci metti davvero poco.

## Calibre-Web Automated 4.0: La Magia delle Magic Shelves

Parliamoci chiaro: gestire una libreria di ebook può diventare un incubo. Duplicati ovunque, metadata incasinati, formati diversi dello stesso libro... insomma, un casino. Ed è qui che [Calibre-Web Automated v4.0.0](https://github.com/crocodilestick/Calibre-Web-Automated/releases/tag/v4.0.0) arriva come un cavaliere in armatura scintillante.

### Duplicati? Non Più un Problema

La funzionalità di **gestione automatica dei duplicati** è, onestamente, qualcosa che avrei voluto anni fa. Il sistema fa una scansione post-ingest (quindi dopo che hai importato i libri), normalizza i titoli in modo intelligente - eliminando articoli e caratteri speciali - e identifica i doppioni. Ma la cosa figata è che è language-aware, quindi non ti segnala come duplicato la traduzione italiana di un libro che hai anche in inglese.

E quando trova duplicati? Puoi scegliere se risolverli manualmente o lasciare che il sistema faccia tutto automaticamente: tiene il più recente, o il più vecchio, o quello con più formati... tu scegli la policy e lui esegue.

### Le Magic Shelves: Smart Playlist per Libri

Questa è la feature che mi ha fatto dire "wow". Le **Magic Shelves** sono collezioni dinamiche che si popolano automaticamente in base a criteri che definisci tu. Una specie di smart playlist ma per i libri.

Vuoi una shelf con tutti i libri di fantascienza pubblicati dopo il 2020 con rating superiore a 4 stelle? Fatto. Tutti i libri non letti della serie Foundation? Fatto. E si aggiorna in tempo reale man mano che aggiungi nuovi libri alla tua biblioteca.

Puoi filtrare per praticamente qualsiasi cosa: titolo, autore, serie, editore, lingua, tag, stato di lettura, rating, data di pubblicazione, identificatori. Con logica AND/OR, pattern regex, range di date... è potentissimo ma rimane sorprendentemente semplice da usare.

### Performance che Contano

Gli sviluppatori hanno fatto un lavoro certosino sull'ottimizzazione. La ricerca avanzata ora carica solo i dati necessari per la pagina corrente invece di tutto il database - su librerie grosse la differenza si sente eccome. E poi hanno convertito tutto in WebP riducendo il peso delle pagine del **97%**. Non male.

Un'altra cosa interessante: hanno sistemato i problemi con Amazon Send-to-Kindle per gli EPUB. Chi ha mai provato a mandare un EPUB modificato con Sigil al Kindle sa di cosa parlo: errori E999 a raffica. Ora dovrebbe andare molto meglio.

## Rackula: Visualizzare il Rack Senza Impazzire

[Rackula](https://github.com/RackulaLives/Rackula) è uno di quei tool che non sapevi di volere finché non li vedi. È un visualizzatore drag-and-drop per rack server che gira nel browser.

Se hai un homelab con più di tre server impilati, sai quanto può essere frustrante tenere traccia di cosa c'è dove, soprattutto quando devi pianificare aggiunte o spostamenti. Rackula risolve il problema: trascini le immagini dei dispositivi (compatibili con la devicetype-library di NetBox) nel rack virtuale, le posizioni correttamente, e ottieni una visualizzazione accurata in scala.

Puoi esportare in PNG, PDF o SVG, e condividere i tuoi layout tramite QR code o URL. La cosa interessante è che è stato recentemente rinominato da Rackarr a Rackula ed è stato aggiunto al TrueNAS Apps Market il 17 gennaio 2026.

Gira interamente nel browser, quindi è leggerissimo. Le configurazioni si salvano via URL univoci o file ZIP scaricabili. Se vuoi persistenza tra sessioni, puoi buildarlo con quella opzione attivata.

## RepoFlow: Un Repository per Governarli Tutti

Quante volte ti sei trovato a gestire Docker images, pacchetti NPM, moduli Python e artifact Maven sparsi tra repository diversi? [RepoFlow](https://www.repoflow.io) cerca di risolvere questo problema con un'interfaccia unificata.

È un package management platform che supporta Docker, NPM, PyPI, Maven, NuGet, Helm, RPM, Gems, Go, Cargo, Composer, Debian e formati universali. Tutto in un posto solo, con SSO e LDAP per l'autenticazione, scanning CVE per la sicurezza, e la possibilità di self-hosting completo.

I requisiti minimi sono abbastanza ragionevoli: 4 core CPU e almeno 3GB di RAM. E la cosa bella del self-hosting è che non hai limiti di storage, bandwidth o numero di pacchetti - sei limitato solo dall'hardware che ci metti.

Costa $79/mese per la versione cloud, ma c'è un tier gratuito con 10GB storage, 10GB bandwidth, 100 pacchetti e utenti illimitati. Oppure lo self-hosti e hai feature parity completa.

## Zerobyte: Backup con Restic ma Facile

Restic è fantastico per i backup, ma ammettiamolo: gestire tutto da linea di comando può diventare tedioso. [Zerobyte](https://github.com/nicotsx/zerobyte) è un wrapper con interfaccia web che rende tutto più semplice.

Crei repository, scheduli job, monitori snapshot tutto da browser invece di scrivere script bash e cronjob a mano. Supporta storage locale, S3-compatible, Google Cloud Storage, Azure Blob, e tramite rclone puoi backuppare su praticamente qualsiasi cloud: Google Drive, Dropbox, OneDrive, Backblaze B2, Wasabi...

Ma la parte che mi piace di più è il supporto per share di rete: NFS, SMB, WebDAV out of the box. Perfetto per chi ha un NAS e vuole backuppare altri server della rete senza dover montare manualmente le share su ogni macchina.

Si deploya facilmente con Docker/Docker Compose, ascolta sulla porta 4096 di default, e da poco supporta anche setup multi-utente - ogni utente ha i suoi volumi/repository/backup da gestire.

## Altre Chicche della Weekly

La newsletter copre anche altre robe interessanti che però, per questa volta, possiamo tranquillamente soprassedere. Devuan ha rilasciato una nuova versione, ma se non sei un fan di systemd probabilmente lo sai già. E Immich continua la sua evoluzione, ma ne abbiamo già parlato altre volte.

## Pensieri Finali (Che Non Sono una Conclusione)

Il mondo self-hosting è in fermento. Strumenti come OpenClaw dimostrano che possiamo avere AI potente senza dover vendere l'anima a provider cloud. Calibre-Web Automated 4.0 dimostra che l'open source può avere UX e feature che fanno invidia ai tool commerciali. E tool come Zerobyte e Rackula rendono la vita quotidiana del self-hoster molto più semplice.

Io continuo a tenere acceso il mio cluster k3s su Raspberry Pi 5 24/7, e progetti come questi mi convincono sempre di più che la strada giusta sia tenere il controllo dei propri dati. Certo, richiede più lavoro, più competenze, più manutenzione. Ma alla fine della fiera, i dati sono miei, il controllo è mio, e nessuno può decidere domani di cambiare le condizioni del servizio o di chiudere baracca.

E voi? Avete già provato qualcuno di questi tool? Il vostro homelab come sta messo? Io sto ancora valutando se dare una chance a OpenClaw sul Pi - potrebbe essere una figata avere un assistente AI che risponde su Telegram ma che in realtà gira nella mia rete locale.

---

**Sources:**
- [Self-Host Weekly #155](https://selfh.st/weekly/2026-01-30/)
- [OpenClaw GitHub Repository](https://github.com/openclaw/openclaw)
- [Calibre-Web Automated v4.0.0 Release](https://github.com/crocodilestick/Calibre-Web-Automated/releases/tag/v4.0.0)
- [Rackula GitHub Repository](https://github.com/RackulaLives/Rackula)
- [RepoFlow Official Website](https://www.repoflow.io)
- [Zerobyte GitHub Repository](https://github.com/nicotsx/zerobyte)
