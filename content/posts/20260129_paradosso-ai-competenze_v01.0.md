---
title: "L'AI e il Paradosso delle Competenze: Chi Guiderà le Macchine di Domani?"
date: 2026-01-29
author: Davide Isoardi
categories: [AI, Tecnologia, Riflessioni]
tags: [intelligenza-artificiale, AI-generativa, competenze, sviluppo-software, sysadmin, open-source]
description: "Riflessioni di un sistemista senior sull'uso quotidiano dell'AI: tra produttività estrema e il rischio concreto di perdere le competenze fondamentali che ci permettono di guidare la tecnologia."
cover:
  image: /img/20260129_ai-paradosso-competenze_header.jpg
  alt: "AI e il Paradosso delle Competenze"
  relative: false
draft: false
---

**Riassunto**: Da sistemista senior, uso l'AI ogni giorno con risultati straordinari. Ma c'è un paradosso: se l'AI sostituisce junior e middle, chi diventerà il senior di domani? Come si formeranno le competenze necessarie per guidare l'AI del futuro?

**TL;DR**: L'AI generativa sta rivoluzionando il lavoro dei developer e dei sistemisti, con i senior che ne beneficiano più dei junior. Ma questo crea un rischio concreto: se le nuove generazioni non acquisiscono le competenze fondamentali perché "tanto c'è l'AI", chi sarà in grado di guidare (e correggere) l'AI di domani? Le assunzioni junior sono già crollate del 50%. Serve un nuovo modello di apprendistato che usi l'AI arricchendo le persone, non impoverendole — prima che diventiamo tutti dipendenti da un'intelligenza esterna che pensa al posto nostro.

---

È qualche mese ormai che uso l'AI generativa praticamente tutti i santi giorni. Claude, ChatGPT, GitHub Copilot — sono diventati parte del mio flusso di lavoro tanto quanto `grep` e `awk`. E devo essere onesto: è un salto in avanti enorme. Non parliamo di un semplice "miglioramento incrementale" tipo quando passai da vim a neovim con tutti i plugin fighi. No, questa roba qui è proprio un cambio di paradigma.

Ma c'è qualcosa che mi tiene sveglio la notte, e non è la solita domanda esistenziale da nerd tipo "Picard o Kirk?" (ovviamente Picard, ma questa è un'altra storia). È una questione che riguarda il futuro del nostro lavoro, e forse anche il mio.

## Il Privilegio dell'Esperienza

Vedete, io mi sento privilegiato. Sono senior da un bel po' — più di quanto mi piaccia ammettere quando vedo il mio certificato di laurea che prende polvere. Lavoro nel centro di eccellenza Hadoop della mia azienda, scrivo documentazione architetturale di dettaglio, quella roba che poi serve davvero per implementare i sistemi. E sono sempre stato quello "portato" per queste cose, quel tipo che al Linux Day di Torino (ci vado praticamente tutti gli anni dal 2012, se non ricordo male) è quello che ti spiega come funziona systemd mentre gli altri ancora bestemmiano contro di esso.

Quindi quando chiedo all'AI di fare qualcosa, so esattamente cosa chiederle. Conosco il contesto, capisco le implicazioni, vedo i pattern. È come avere un equipaggio della Enterprise che esegue i tuoi ordini alla perfezione — senza pause caffè, senza malumori, senza bisogno di spiegare tre volte lo stesso concetto durante lo standup meeting.

E qui viene il punto: usare l'AI è davvero come avere un team di 10 middle developer super competenti, inarrestabili, che seguono le tue istruzioni al millesimo. I dati che ho trovato lo confermano: secondo [una ricerca su GitHub Copilot](https://arxiv.org/abs/2302.06590), gli sviluppatori completano i task il 55% più velocemente. E guardate questa statistica interessante che ho scovato: [un terzo degli sviluppatori con oltre 10 anni di esperienza genera oltre il 50% del codice con strumenti AI](https://www.tomshw.it/business/i-senior-developer-abbracciano-il-coding-moderno-2025-08-29), contro solo il 13% dei programmatori con meno di 2 anni di carriera.

Sapete cosa significa? Che noi senior stiamo sfruttando l'AI molto più dei junior. E questo, paradossalmente, è sia fantastico che terrificante.

## Il Grande Vuoto in Arrivo

Ora, diciamoci la verità: preferisco lavorare con l'AI che con un team di persone reali. L'ho detto. So che sembra cinico, ma dopo anni passati in riunioni infinite dove si discute per mezz'ora su come nominare una variabile, oppure a rispondere per la quinta volta alla stessa domanda su come funziona HDFS, be'... Claude non mi chiede mai "ma sei sicuro?" quando gli spiego per la terza volta lo stesso concetto.

Ma ecco dove si crea il problema, un problema grosso come un buco nero. Le assunzioni di sviluppatori junior sono già calate drasticamente. Ho letto che [le assunzioni di neolaureati nel tech sono crollate del 50% rispetto ai livelli pre-pandemia](https://www.agendadigitale.eu/mercati-digitali/intelligenza-artificiale-minaccia-costante-per-i-giovani-lavoratori/), con le Big Tech che hanno ridotto del 25% l'ingresso di neolaureati tra il 2023 e il 2024.

Pensateci un attimo. Se noi senior ci troviamo così bene con l'AI che sostituisce i middle e i junior... chi diventerà il senior di domani? Come cresceranno le competenze necessarie per guidare efficacemente l'AI del futuro?

È come se in Star Trek avessero eliminato tutti i ranghi intermedi tra cadetto e capitano. Come diavolo fai a diventare un buon capitano se non hai mai fatto il timoniere, il capo ingegnere, il primo ufficiale? Non puoi saltare quella roba lì. Quelle esperienze sono fondamentali, anche — forse soprattutto — quelle negative, quelle dove combini casini clamorosi.

## Il Sistemista che Non Sapeva più i Comandi

Vi racconto una cosa che mi fa paura, da sistemista. Io già me lo immagino il futuro dei sistemi operativi: AI integrata ovunque. Non dovrai più sapere le regex, la sintassi contorta di `awk`, i flag esoterici di `sed`. Interrogherai il sistema in linguaggio naturale — "Ehi, trova tutti i file di log modificati nell'ultima ora che contengono errori di autenticazione" — e il sistema te li servirà su un piatto d'argento.

Bellissimo, no? Efficientissimo.

Ma io adesso so usare la console. So che `grep -rn "pattern"` cerca ricorsivamente, so che `sed 's/foo/bar/g'` sostituisce tutte le occorrenze, so leggere una regex come `/^[A-Z]{3}\d{4}$/` e capire immediatamente cosa cerca. Però se uso queste cose di meno... be', le sintassi le dimenticherò. È inevitabile. Il cervello fa pulizia di quello che non usi, è fisiologia.

E chi invece nascerà sistemista in un mondo con l'AI già integrata? Uno che non dovrà mai imparare i comandi base perché "tanto c'è l'AI che lo fa"?

Il giorno che l'AI sbaglierà — e credetemi, sbaglierà, l'ho vista [generare codice con il 13.6% di errori in meno per riga rispetto al codice scritto senza AI](https://www.quantumrun.com/consulting/github-copilot-statistics/), il che è ottimo ma significa che gli errori ci sono ancora — come farà quel sistemista ad accorgersene? Come farà a correggere in autonomia?

È come se improvvisamente tutti i meccanici del mondo smettessero di capire come funziona un motore a combustione perché "tanto adesso ci sono solo auto elettriche con diagnostica AI". Poi un giorno l'AI diagnostica sbaglia, dice che è la batteria quando invece è il controller, e il meccanico sta lì a grattarsi la testa perché non ha mai imparato a debuggare realmente il sistema.

## Quando l'AI Istruirà l'AI (e Noi Staremo a Guardare)

C'è uno scenario che mi gira per la testa, un po' distopico ma neanche troppo. Immaginate fra dieci, quindici anni. I senior attuali come me saranno probabilmente in pensione o quasi (spero di ritirarmi a coltivare pomodori e a hostare servizi in self-hosting nella mia cantina, ma vabbè). I middle attuali saranno diventati senior, ma avranno fatto la maggior parte del loro percorso con l'AI al fianco — o meglio, con l'AI che faceva gran parte del lavoro.

E i junior? Quali junior? Quelli che dovevano esserci non ci sono mai stati, perché tanto "l'AI fa quel lavoro meglio e costa meno".

Quindi avremo una generazione di senior che in realtà non hanno mai fatto davvero tutto il percorso completo. Senior che sono bravissimi a dire all'AI cosa fare, ma che forse non sanno più fare a mano le cose fondamentali. E quando questi senior dovranno guidare l'AI del 2040, che sarà probabilmente ancora più potente e complessa... ce la faranno?

O forse — ed ecco la parte davvero inquietante — avremo bisogno di un'AI senior che istruisce le AI middle e junior? Un sistema che insegna ad altri sistemi, con noi umani sempre più defilati, sempre più dipendenti?

Non fraintendetemi, non sono un apocalittico tecnologico. Non sono uno di quelli che pensa "l'AI ci ruberà il lavoro tutti quanti". Faccio parte dell'ILS (Italian Linux Society), sono un sostenitore del software libero, della Pirateria intesa come libertà di espressione e condivisione delle idee in un mondo che sempre più tende al controllo (non quella del "scarico Windows craccato", eh). Credo nella tecnologia come strumento di libertà — come la Federazione dei Pianeti Uniti in Star Trek, non come l'Impero Galattico (che poi, diciamocelo, Star Wars è fantasy mascherato da sci-fi, ma questa è un'altra guerra da combattere in un altro articolo). Ma proprio perché ci credo, mi preoccupo quando vedo che potrebbe diventare una catena invece che una chiave.

## Numeri che Non Mentono (e che Fanno Riflettere)

Guardiamo alcuni dati concreti. [Oltre il 97% degli sviluppatori di quattro paesi diversi hanno dichiarato di usare strumenti di AI coding al lavoro](https://www.itpro.com/software/development/junior-developer-ai-tools-coding-skills). È praticamente universale. E [GitHub Copilot ha raggiunto 20 milioni di utenti nel luglio 2025](https://www.quantumrun.com/consulting/github-copilot-statistics/), con un aumento di 5 milioni in soli tre mesi.

L'AI contribuisce ora al [46% di tutto il codice scritto dagli utenti attivi](https://www.index.dev/blog/ai-pair-programming-statistics). Quasi la metà. E per gli sviluppatori Java, si arriva al 61%.

Ma ecco il dato che davvero dovrebbe farci fermare a pensare: c'è chi nota che i junior developer stanno sviluppando una ["overreliance on AI tools"](https://www.itpro.com/software/development/junior-developer-ai-tools-coding-skills), spedendo codice più velocemente ma senza saperlo spiegare, senza capire i casi limite, senza quella comprensione profonda che viene solo dall'aver sbattuto la testa contro il muro cinquanta volte prima di capire come funziona davvero quella cosa.

Come dice qualcuno nell'articolo: "We're trading deep understanding for quick fixes" — stiamo scambiando la comprensione profonda con soluzioni rapide. E questo è esattamente il punto.

## L'Open Source Come Palestra (Che Nessuno Usa Più?)

Una delle cose bellissime dell'open source — e parlo da uno che ha passato serate intere a leggere il codice di progetti come [systemd](https://github.com/systemd/systemd), [Apache Hadoop](https://github.com/apache/hadoop), o [Kubernetes](https://github.com/kubernetes/kubernetes) — è che puoi imparare dai migliori. Leggi il codice, vedi come hanno risolto problemi complessi, cerchi di capire le decisioni architetturali.

Ma se l'AI scrive il codice per te, e tu non hai più bisogno di "sporcarti le mani"... quando mai troverai il tempo, la motivazione, il bisogno di andare a leggere quel codice? Quando mai imparerai quelle tecniche, quei pattern, quella saggezza accumulata in decenni di sviluppo?

È un po' come imparare a cucinare. Puoi usare il Bimby (o il Thermomix, per i non italiani) e fare piatti fantastici seguendo le ricette. Ma se non hai mai imparato come funziona una riduzione, come si fa un soffritto perfetto, come si capisce quando la pasta è al dente senza guardare l'orologio... be', il giorno che il Bimby si rompe, rimani a pane e salame.

## Serve un Nuovo Modello di Apprendistato

Allora, cosa facciamo? Rinunciamo all'AI e torniamo a scrivere tutto a mano come nel 2015? Ovviamente no. Sarebbe stupido quanto negare che le automobili siano migliori dei cavalli.

Ma dobbiamo — e uso "dobbiamo" perché credo sia davvero una necessità — trovare un modo per usare l'AI arricchendo le persone, non impoverendole. Non so esattamente come, ma alcune idee cominciano a formarsi.

Per esempio, possiamo pensare a un modello in cui i junior usano l'AI, sì, ma con vincoli. Magari per il primo anno devono scrivere tutto il codice "core" a mano, senza assistenza. Devono fare gli errori, devono debuggare le cose oscure, devono passare tre ore a capire perché quel dannatissimo script bash non funziona (spoiler: quasi sempre è un problema di quoting o di spazi nei nomi dei file).

E poi, gradualmente, gli dai accesso agli strumenti AI, ma sempre con una comprensione profonda di cosa stanno facendo. Un po' come nella formazione dei piloti: prima impari a volare con gli strumenti manuali, poi ti danno il pilota automatico. Ma sai sempre cosa sta facendo la macchina e puoi prendere i comandi in qualsiasi momento.

O magari — e questo lo dico da uno che partecipa attivamente agli eventi della community — dobbiamo reinventare il concetto stesso di comunità tech. Fare in modo che il Linux Day, gli hackathon, i meetup diventino luoghi dove si trasmette non solo "come usare l'AI" ma "come pensare come un sistemista/developer/architetto". Quel tipo di conoscenza tacita, quasi artigianale, che non sta nei tutorial ma nelle storie, negli aneddoti, nei "quella volta che ho distrutto il sistema di produzione alle 3 di notte e ho imparato questa lezione".

## L'AI è uno Strumento, Non un Sostituto (Ma Lo Sarà?)

Quando chatto con altri sistemisti e developer della mia età, molti dicono "ma dai, l'AI è solo uno strumento, come lo era git, come lo erano gli IDE, come lo era Stack Overflow". E in parte hanno ragione. Ogni generazione di tecnologi ha avuto i suoi strumenti che facevano storcere il naso ai veterani.

Ricordo quando alcuni vecchi Unix sysadmin dicevano che systemd era "troppo complicato" e "nascondeva troppo". Eppure oggi systemd è lo standard, e funziona benissimo. Io l'ho abbracciato, l'ho studiato a fondo, e ora lo uso quotidianamente.

Ma l'AI è diversa. È diversa perché non è solo un'astrazione su qualcosa che già sai fare. È un sostituto quasi completo del processo di creazione. Quando usi git, stai ancora pensando tu al codice, git gestisce solo le versioni. Quando usi un IDE, sei ancora tu che scrivi, l'IDE ti aiuta con l'autocomplete e il refactoring.

Quando usi l'AI, puoi letteralmente dire "fammi un'API REST in Python con FastAPI che gestisce autenticazione JWT e CRUD per utenti e prodotti" e quella te la tira fuori. Completa. Funzionante. Con i test (a volte).

Dov'è il confine tra "strumento che ti aiuta" e "sostituto che pensa al posto tuo"? E soprattutto, come facciamo a non attraversarlo senza accorgercene?

## Una Dipendenza Diversa da Tutte le Altre

C'è un'altra questione, più sottile ma forse ancora più importante. La dipendenza.

Siamo sempre stati dipendenti dagli strumenti, certo. Io sono dipendente dalla mia console, dal mio setup di vim (anzi, neovim con tutti i plugin che si ostina a caricare anche quando gli dico di no), dalle mie ansible playbook. Se mi levi quelli, rallento. Ma non sono bloccato. Posso usare nano (con disgusto), posso scrivere gli script bash a mano, posso configurare i sistemi manualmente.

Ma se divento dipendente dall'AI per cose basilari? Se dimentico come funziona il pattern matching in awk perché tanto "lo chiedo all'AI"? Se non ricordo più la differenza tra un inner join e un left join perché "tanto l'AI sa quale usare"?

Quella non è una dipendenza da uno strumento. È una dipendenza da un'intelligenza esterna che pensa al posto mio. E questo mi spaventa, perché significa che sto esternalizzando non solo l'esecuzione, ma anche la comprensione.

È la differenza tra usare una calcolatrice per fare 5.847 × 3.291 (ragionevole, noioso farlo a mano) e usarla per fare 5 + 3 perché hai dimenticato come si sommano i numeri.

## Le Griglie, i Board Games e il Self-Hosting Come Antidoto

Forse la soluzione — o almeno parte di essa — sta nel mantenere viva una parte della nostra vita tech che sia "inutilmente" complessa. Che richieda di sporcarsi le mani senza motivo economico.

Io, per esempio, faccio self-hosting di un sacco di roba a casa. Ho un piccolo cluster che ospita Nextcloud, Jellyfin, un'istanza di Gitea, un server Minecraft per quando vengono gli amici con le famiglie (e i bambini ci lasciano in pace per due ore beate). Non ne ho strettamente bisogno — ci sono servizi cloud per tutto questo. Ma lo faccio perché mi piace, perché imparo, perché quando qualcosa si rompe alle 11 di sera devo capire cos'è e sistemarlo.

E questo mi tiene allenato. Mi tiene quello strato di conoscenza profonda che altrimenti, usando solo l'AI al lavoro, comincerei a perdere.

Allo stesso modo, preferisco ancora una bella grigliata con famiglia e altre famiglie nerd come me che andare a fare le cose "di moda". I board games sono diventati un appuntamento fisso — 7 Wonders, Carcassonne, Castelli di Borgogna, Magica Adunanza, Pulsare, Battlestar Galactica. Quella roba lì. German style quando possibile, perché richiedono strategia, non solo fortuna. D&D sarebbe il massimo, ma ora che sono padre di famiglia organizzare una sessione è praticamente impossibile, quindi mi accontento di qualche partita occasionale quando gli astri (e i bambini) si allineano favorevolmente. Non perché sono asociale (be', non solo per quello), ma perché sono attività che mantengono acceso il cervello in modi diversi, creativi, non ottimizzati.

E forse questo è parte della risposta: mantenere spazi — sia nella vita professionale che in quella personale — dove l'efficienza non è l'obiettivo, dove il percorso è importante quanto la destinazione, dove sbagliare e imparare dall'errore è parte integrante del processo.

## Il Futuro che Vogliamo Costruire

Questa rivoluzione tecnologica è pervasiva, questo è chiaro. E cambierà il modo di lavorare di noi tecnici in modi che probabilmente neanche riusciamo a immaginare del tutto. Tra dieci anni forse rideremo di questo articolo, come oggi ridiamo degli articoli degli anni 2000 che dicevano che Google ci avrebbe reso tutti stupidi perché non avremmo più dovuto ricordare niente.

O forse no. Forse tra dieci anni avremo davvero una generazione di "senior" che in realtà non sanno fare nulla senza l'AI, che sono prigionieri delle loro interfacce a linguaggio naturale, incapaci di capire quando la macchina sta sbagliando perché non hanno mai imparato a fare quella cosa nel modo "difficile".

La domanda, in fondo, non è "l'AI è buona o cattiva?" — è una domanda stupida, come chiedere se i martelli sono buoni o cattivi. La domanda giusta è: "Come vogliamo usare l'AI? Come ci assicuriamo che ci renda più capaci, non meno? Come trasmettiamo le competenze essenziali alle nuove generazioni in un mondo dove quelle competenze sembrano superflue?"

Non ho risposte definitive. Sarei un bugiardo se pretendessi di averle. Ma credo che iniziare a porsi queste domande — adesso, mentre siamo ancora agli inizi di questa rivoluzione — sia fondamentale. Perché tra dieci anni potrebbe essere troppo tardi.

E io vorrei che le persone che verranno dopo di me, i futuri senior del 2040 e del 2050, siano davvero competenti, non solo bravi a dare ordini a un'AI. Che sappiano ancora debuggare un kernel panic, leggere un core dump, ottimizzare una query complessa, scrivere un parser a mano quando serve.

Che siano, insomma, quello che la USS Enterprise aveva di meglio: un equipaggio che sapeva come funzionava la nave anche quando il computer di bordo faceva le bizze. Perché credetemi, il computer farà le bizze. Sempre.

E quando succederà, sarà meglio che qualcuno sappia ancora come si fa a "bypassare il condotto energetico primario e ricalibcare i deflettori manualmente". Anche se è solo una metafora per dire "aprire un terminale e fixare la cosa senza chiedere a Claude".

---

**Fonti e approfondimenti:**

- [The Impact of AI on Developer Productivity: Evidence from GitHub Copilot](https://arxiv.org/abs/2302.06590)
- [GitHub Copilot Statistics 2026](https://www.quantumrun.com/consulting/github-copilot-statistics/)
- [AI coding assistants wave goodbye to junior developers - CIO](https://www.cio.com/article/3509174/ai-coding-assistants-wave-goodbye-to-junior-developers.html)
- [Sorpresa! Gli sviluppatori esperti usano l'AI più dei junior - Tom's Hardware](https://www.tomshw.it/business/i-senior-developer-abbracciano-il-coding-moderno-2025-08-29)
- [Intelligenza artificiale, minaccia costante per i giovani lavoratori - Agenda Digitale](https://www.agendadigitale.eu/mercati-digitali/intelligenza-artificiale-minaccia-costante-per-i-giovani-lavoratori/)
- [Junior Developers lack coding skills because of AI tools - IT Pro](https://www.itpro.com/software/development/junior-developer-ai-tools-coding-skills)
- [Top 100 AI Pair Programming Statistics 2026](https://www.index.dev/blog/ai-pair-programming-statistics)

**Repository Open Source citati:**
- [systemd](https://github.com/systemd/systemd) - System and Service Manager per Linux
- [Apache Hadoop](https://github.com/apache/hadoop) - Framework per distributed storage e processing
- [Kubernetes](https://github.com/kubernetes/kubernetes) - Container orchestration system
