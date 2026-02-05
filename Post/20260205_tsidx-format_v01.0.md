---
title: "TSIDX: Il Formato che Rende Splunk Veloce (e Costoso)"
date: 2026-02-05
author: Davide Isoardi
categories: [Deep Dive, Search]
tags: [splunk, tsidx, inverted-index, search-engine, indexing, performance]
description: "Deep-dive tecnico sul formato TSIDX di Splunk: lexicon, posting lists, bloom filters, bucket lifecycle e come tutto questo impatta performance e storage cost"
complexity: advanced
prerequisites:
  - title: "Inverted Index: Fondamenti"
    url: "/blog/deep-dive/inverted-index/"
    required: false
  - title: "OpenSearch vs Splunk vs Elasticsearch vs Solr"
    url: "/blog/posts/20260205_search-engines-comparison_v01.0/"
    required: false
reading_time: "18-22 min"
cover:
  image: "/blog/img/20260205_tsidx-format_header.jpg"
  alt: "TSIDX format deep dive"
  caption: "Anatomia del formato TSIDX di Splunk"
---

## 📋 Requisiti

**Livello**: Advanced
**Tempo lettura stimato**: 18-22 minuti

**Prerequisiti obbligatori**:
- Familiarità con concetti di indexing e search engine
- Comprensione base di strutture dati (hash tables, array)

**Prerequisiti consigliati**:
- Conoscenza di base di Splunk o altri log analytics platform
- Familiarità con concetti di inverted index

---

**Riassunto**: Il formato TSIDX (Time-Series Index) è il cuore dell'architettura di Splunk, quello che permette query sub-second su petabyte di log ma che al tempo stesso fa lievitare i costi di storage. Analizziamo come funziona internamente: lexicon, posting lists, bloom filters, bucket lifecycle, e perché capire questo formato è fondamentale per ottimizzare deployment Splunk in produzione.

**TL;DR**: TSIDX è il formato proprietario di Splunk per indicizzare eventi time-series. Ogni bucket contiene TSIDX files (lexicon + posting lists che mappano termini → posizioni eventi) + bloom filters (filtri probabilistici per skip bucket inutili) + rawdata compressi. Storage ratio tipico: rawdata 15% dei dati originali, TSIDX 35% (totale ~50% overhead rispetto a storage grezzo). Bucket lifecycle: hot (scrittura attiva) → warm (read-only + bloom filter) → cold (archiviazione) → frozen (eliminazione o archive esterno). Ottimizzazioni: tuning segmentation rules riduce lexicon cardinality (esempio reale: -77% lexicon entries, -49% TSIDX size). Trade-off critico: più TSIDX = query veloci ma storage cost alti. Capire TSIDX spiega perché Splunk è potente ma costoso.

---

## Perché Dovrebbe Interessarti il TSIDX

Se hai mai usato Splunk, probabilmente hai notato due cose: è dannatamente veloce nel cercare tra miliardi di eventi, e costa una fortuna in licensing e storage. Entrambe le cose sono dovute al formato TSIDX.

La maggior parte degli articoli su Splunk ti dice "usa TSIDX reduction" o "ottimizza il tuo tsidxWritingLevel" senza spiegarti *cosa diavolo* sia un TSIDX file. Ed è un problema, perché se non capisci come Splunk indicizza i tuoi dati, finisci con cluster sovradimensionati che costano il triplo del necessario.

Questo articolo scava nei dettagli tecnici del formato TSIDX. Non è documentazione ufficiale Splunk (quella è volutamente vaga), ma è basato su anni di esperienza in produzione, reverse engineering parziale, e le poche presentazioni tecniche che Splunk ha rilasciato alle conferenze.

## TSIDX in 60 Secondi

Prima di entrare nei dettagli, il TL;DR tecnico:

**TSIDX** = Time-Series Index file. È un inverted index ottimizzato per time-series data dove ogni term (parola, numero, pattern) nel tuo log è mappato a una lista di eventi che lo contengono.

Un bucket Splunk contiene:
- **Rawdata files**: eventi compressi (zlib), circa 15% della dimensione originale
- **TSIDX files**: lexicon + posting lists, circa 35% della dimensione originale
- **Bloom filter**: struttura probabilistica per skip rapido, pochi MB
- **Metadata**: hosts.data, sources.data, sourcetypes.data

Quando fai una query tipo `index=web error status=500`, Splunk:
1. Usa bloom filters per eliminare bucket che sicuramente non contengono "error" o "500"
2. Legge TSIDX files dei bucket rimasti per trovare posting lists di "error" e "500"
3. Recupera eventi dal rawdata usando seek addresses nelle posting lists
4. Applica filtri addizionali e aggregazioni

Veloce perché evita di leggere rawdata inutili. Costoso perché TSIDX files occupano spazio significativo.

## Anatomia di un TSIDX File

Un TSIDX file ha due componenti principali: **lexicon** e **posting lists**.

### Il Lexicon: Dizionario dei Termini

Il lexicon è essenzialmente un dizionario ordinato di tutti i termini unici trovati negli eventi del bucket. Per "termini" intendo qualsiasi cosa l'indicizzatore abbia segmentato: parole, numeri, IP address, timestamp component, eccetera.

Esempio di lexicon entries per un log Apache:
```
200
404
500
GET
POST
/api/users
/login
apache
error
index.html
192.168.1.100
...
```

Ogni entry nel lexicon punta a una posting list. Il lexicon è ordinato alfabeticamente, il che permette ricerche binarie efficienti e ottimizza wildcard searches tipo `host=web*` (molto più veloci di `host=*web`).

### Posting Lists: Dove Stanno gli Eventi

Per ogni term nel lexicon, la posting list contiene:
- **Seek addresses**: offset esatti nel rawdata file dove trovare eventi che contengono quel term
- **Frequency info**: quante volte appare il term (utile per ranking)
- **Metadata addizionali**: timestamp range, field associations, eccetera

Esempio concettuale:
```
Term: "error"
Posting List: [
  {offset: 1024, timestamp: 1707134400, field: _raw},
  {offset: 5632, timestamp: 1707134401, field: message},
  {offset: 12048, timestamp: 1707134405, field: _raw},
  ...
]
```

Quando Splunk cerca "error", non scansiona gigabyte di log. Legge il lexicon, trova "error", legge la posting list, e salta direttamente agli offset nei rawdata files. Questo è il motivo per cui Splunk è velocissimo sulle keyword searches.

### Dimensioni Reali

Su un cluster di produzione che gestisco, questi sono i ratio tipici per log applicativi strutturati (JSON):

- **Dati pre-ingest**: 100 GB/giorno
- **Rawdata (compressi)**: ~15 GB (ratio 15%)
- **TSIDX files**: ~35 GB (ratio 35%)
- **Bloom filters + metadata**: ~0.5 GB
- **Totale storage**: ~50.5 GB

Quindi per ogni 100 GB di log, paghi ~50 GB di storage sul cluster. E questo è *dopo* compressione. Se i tuoi log sono ad alta cardinalità (tanti valori unici), il ratio TSIDX può salire al 50-60%.

## Segmentation: Come Splunk Costruisce il Lexicon

La segmentation è il processo che decide cosa va nel lexicon. Splunk usa regole definite in `segmenters.conf` per spezzare eventi in token.

### Segmenters di Default

Splunk ha segmenters built-in che trattano:
- **Major breakers**: spazi, newline, parentesi, virgole, eccetera → creano boundary netti
- **Minor breakers**: underscore, slash, dot → mantengono token più lunghi ma permettono anche sub-token

Esempio con log Apache:
```
192.168.1.100 - - [05/Feb/2026:10:15:30 +0000] "GET /api/users/42 HTTP/1.1" 200 1234
```

Segmentation produce (tra gli altri):
```
192.168.1.100
192
168
1
100
GET
/api/users/42
api
users
42
HTTP/1.1
200
1234
05
Feb
2026
10
15
30
...
```

Vedi il problema? Timestamp components tipo "10", "15", "30" diventano lexicon entries separate. Se hai 86400 secondi in un giorno e ogni secondo appare in molti eventi, il lexicon esplode.

### High-Cardinality Hell

Un case study reale da [Duane Waddle](https://www.duanewaddle.com/splunk-bucket-lexicons-and-segmentation/):

**Scenario**: 782 MB di Cisco ASA firewall logs.

**Dopo indicizzazione standard**:
- Rawdata: 156 MB
- TSIDX files: 538 MB (!)
- Lexicon entries: 11.8 milioni
- Average occurrences per entry: 26 eventi

Analizzando con `walklex` (utility Splunk per ispezionare TSIDX), Duane scoprì che **quasi 60% delle entries apparivano una sola volta**. E 5.7 milioni di entries erano variazioni di timestamp.

**Dopo ottimizzazione** (custom segmentation rules):
- Lexicon entries: 2.7 milioni (-77%)
- TSIDX files: 277 MB (-49%)
- Average occurrences: 94 eventi per entry

Come? Filtrando timestamp components via `segmenters.conf` e facendo "/" un major segmenter.

La morale: se non ottimizzi segmentation per i tuoi dati specifici, sprechi storage su lexicon entries inutili.

## Bloom Filters: Il Turbo per le Query

I bloom filters sono la "magia nera" che rende Splunk ancora più veloce. Sono strutture dati probabilistiche che rispondono alla domanda: "questo bucket contiene il term X?" con due possibili risposte:
- **"Sicuramente NO"** → skip il bucket, non leggere nemmeno il TSIDX
- **"Forse SÌ"** → leggi il TSIDX per confermare

Nota: bloom filters possono dare **false positive** (dice "forse sì" ma in realtà è no), ma **MAI false negative** (se dice "no", è no al 100%).

### Come Funziona un Bloom Filter

Semplificando brutalmente: è un array di bit + multiple hash functions.

Quando indicizzi un term:
1. Hash il term con N hash functions diverse
2. Setta a 1 i bit nelle posizioni restituite dagli hash
3. Ripeti per ogni term nel bucket

Quando cerchi un term:
1. Hash il term con le stesse N hash functions
2. Controlla se *tutti* i bit nelle posizioni risultanti sono a 1
3. Se almeno uno è 0 → term sicuramente non presente
4. Se tutti sono 1 → term *forse* presente (devi verificare nel TSIDX)

I bloom filters in Splunk sono creati quando un bucket passa da hot a warm (lifecycle stage che vediamo tra poco).

### Dimensioni e Tuning

Splunk crea bloom filters con dimensioni basate su:
- Numero di unique terms nel bucket
- False positive rate target (di solito 1-5%)

Su bucket tipici, bloom filters sono 1-10 MB. Niente rispetto ai TSIDX (gigabyte), ma l'impact sulle performance è enorme.

Un esempio pratico: query su 1000 bucket, 900 non contengono i search terms. Con bloom filters:
- Splunk skip 900 bucket leggendo solo bloom filters (pochi MB)
- Legge TSIDX solo dei 100 bucket rimanenti
- Risparmio: evita di leggere ~900 * ~500MB = ~450 GB di TSIDX inutili

Ecco perché Splunk può rispondere in secondi su dataset enormi.

## Bucket Lifecycle: Hot, Warm, Cold, Frozen

Splunk organizza i dati in bucket, e ogni bucket ha un lifecycle definito. Capire questo è fondamentale per ottimizzare storage cost.

### Hot Buckets

**Stato**: scrittura attiva
**Location**: default in `$SPLUNK_HOME/var/lib/splunk/<index>/db/hot_*`
**Caratteristiche**:
- Ricevono eventi in tempo reale
- TSIDX files aggiornati continuamente
- **NO bloom filter ancora** (troppo costoso ricostruirlo ad ogni write)
- Storage: tipicamente SSD per performance

Un indexer può avere N hot bucket per indice (configurabile con `maxHotBuckets`). Quando un hot bucket raggiunge dimensione massima (`maxDataSize`) o age massima, viene "rolled" a warm.

### Warm Buckets

**Stato**: read-only
**Location**: `$SPLUNK_HOME/var/lib/splunk/<index>/db/db_*`
**Caratteristiche**:
- **Bloom filter creato** al momento del roll
- TSIDX files immutabili
- Searchable normalmente
- Storage: possono stare su HDD più economici

I warm bucket restano finché:
- Raggiunto limite di spazio totale per l'indice (`maxTotalDataSizeMB`)
- O raggiunto limite di età (`frozenTimePeriodInSecs`)

Poi vengono promossi a cold.

### Cold Buckets

**Stato**: read-only, archiviazione
**Location**: `$SPLUNK_HOME/var/lib/splunk/<index>/colddb/db_*`
**Caratteristiche**:
- Stessa struttura dei warm (rawdata + TSIDX + bloom filter)
- Searchable, ma con latency maggiore (storage tier più lento)
- Storage: tipicamente HDD economici o network storage

In deployment enterprise, cold bucket possono essere spostati su storage object (S3-compatible) per ulteriore riduzione costi.

### Frozen Buckets

**Stato**: eliminati o archiviati esternamente
**Caratteristiche**:
- Rimossi dal cluster Splunk
- Opzionalmente copiati in `coldToFrozenDir` per archive a lungo termine
- **Non searchable** da Splunk (a meno di re-import)

La retention policy è definita da `frozenTimePeriodInSecs` (default: 188697600 secondi = ~6 anni).

### Hot-Warm-Cold in Pratica

Esempio reale di una mia configurazione per indice applicativo:

```ini
[application_logs]
homePath = volume:hot/application_logs/db
coldPath = volume:cold/application_logs/colddb
thawedPath = $SPLUNK_DB/application_logs/thaweddb

maxHotBuckets = 10
maxDataSize = auto_high_volume
maxTotalDataSizeMB = 512000  # 500 GB totale per indice
frozenTimePeriodInSecs = 2592000  # 30 giorni

# Hot tier: SSD
# Warm tier: HDD
# Cold tier: S3-compatible via SmartStore
```

Con questa config:
- 7 giorni in hot (SSD veloce, ~100 GB)
- 21 giorni in warm (HDD, ~300 GB)
- 2 giorni in cold (S3, ~100 GB) prima di frozen
- Totale retention: 30 giorni

Cost breakdown (storage):
- Hot SSD: $0.10/GB/month → $10/month
- Warm HDD: $0.03/GB/month → $9/month
- Cold S3: $0.01/GB/month → $1/month
- **Totale**: ~$20/month solo storage (escluso licensing Splunk)

Moltiplicalo per 50 indici su un enterprise deployment e capisci perché tutti parlano di "Splunk TCO".

## TSIDX Reduction: Tecniche di Ottimizzazione

Splunk offre diverse tecniche per ridurre TSIDX size senza compromettere troppo la searchability.

### 1. TSIDX Reduction Policy

Setting: `tsidxReductionCheckPeriodInSec` in indexes.conf

Splunk può automaticamente "semplificare" TSIDX files di bucket vecchi rimuovendo:
- Posting lists per termini ad altissima frequenza (rumore)
- Metadata ridondanti

Trade-off: query su bucket ridotti sono più lente (Splunk deve fare più fallback su rawdata).

In pratica, questa feature è delicata. L'ho vista creare più problemi (query timeout) che benefici (saving storage marginale). Attivala solo se:
- Hai analizzato query patterns e sai che bucket vecchi sono raramente cercati
- Storage cost è *davvero* critico
- Hai capacity per latency maggiore su historical searches

### 2. Custom Segmentation Rules

Come abbiamo visto prima, tuning `segmenters.conf` può ridurre drasticamente lexicon size.

Strategia pratica:
1. Usa `walklex` per analizzare lexicon dei tuoi bucket
2. Identifica high-cardinality terms inutili (timestamp components, UUID, eccetera)
3. Crea regole custom per filtrarli o cambiarli a minor breakers

Esempio per filtrare timestamp seconds:
```ini
[<segmenter_name>]
MAJOR = <your_breakers>
FILTER = \d{2}:\d{2}:\d{2}  # regex per HH:MM:SS
```

Attenzione: filtrare troppo aggressivamente rende certi search patterns impossibili.

### 3. Indexed Fields Tuning

Non tutti i field devono essere indicizzati. In `fields.conf`:

```ini
[your_noisy_field]
INDEXED = false
```

Questo evita che field values entrino nel lexicon. Trade-off: non puoi più fare `your_noisy_field=value` come keyword search (devi usare `| search your_noisy_field=value` dopo aver recuperato eventi, molto più lento).

Usa `INDEXED=false` per:
- Field con valori ad altissima cardinalità che non cerchi mai come keyword
- Field calcolati a search time
- Field verbosi o JSON blob giganti

### 4. Enhanced TSIDX Compression (Splunk 8.1+)

Setting: `tsidxWritingLevel` in indexes.conf

```ini
[<index>]
tsidxWritingLevel = 4  # valori 1-4, default 3
```

Livelli:
- **1**: compatibilità legacy
- **2**: compression migliorata (default pre-8.1)
- **3**: default su Splunk 8.0+
- **4**: enhanced compression (8.1+), fino a 40% riduzione TSIDX size

Trade-off minimo: livello 4 ha overhead CPU leggermente maggiore all'indicizzazione, ma è trascurabile. **Raccomando sempre level 4 su deployment nuovi**.

## Performance Implications: Quando TSIDX Ti Salva (o Ti Frega)

### Query Veloci: Keyword Searches

TSIDX è ottimizzato per:
- **Simple keyword**: `error`, `status=500`, `host=web01`
- **Field-based filters**: `index=main sourcetype=access_combined`
- **Wildcard prefix**: `host=web*` (scansione lexicon ordinato)

Questi pattern sono sub-second anche su TB di dati perché Splunk:
1. Skip bucket via bloom filters (millisecondi)
2. Lookup nel lexicon (binary search, millisecondi)
3. Legge posting lists (MB, non GB)
4. Recupera eventi specifici da rawdata

### Query Lente: Pattern Matching Complesso

TSIDX *non aiuta* con:
- **Wildcard suffix/infix**: `host=*web`, `host=*web*` → forza full lexicon scan
- **Regex complesse**: `| regex _raw="complex.*pattern"` → forza rawdata extraction
- **Field extraction**: `| rex field=_raw "(?<my_field>...)"` → processing post-retrieval

Questi pattern forzano Splunk a:
1. Recuperare *molti più eventi* del necessario
2. Processare rawdata in memoria
3. Applicare filtri computazionalmente costosi

Esempio: `index=web | regex _raw="error.*database.*timeout"` su 1 TB di log può impiegare minuti. Alternativa più veloce: `index=web error database timeout | regex _raw="error.*database.*timeout"` (primo pass usa TSIDX, secondo affina).

### Memory Footprint Durante Search

Splunk carica posting lists in memoria durante query execution. Su lexicon entries ad altissima frequency (milioni di eventi), questo può esaurire RAM.

Esempio patologico: query `index=*` senza altri filtri su cluster con 100TB dati. Splunk tenta di:
1. Leggere TSIDX di tutti i bucket (GB)
2. Caricare posting lists per ogni term matchato (praticamente tutto)
3. OOM crash o query timeout

Best practice: **sempre** filtra per time range (`earliest=-24h`) e aggiungi keyword specifiche.

## Confronto: TSIDX vs Altri Formati

### TSIDX vs Elasticsearch Inverted Index

Elasticsearch usa anch'esso inverted index, ma con differenze:

**Similarità**:
- Lexicon (term dictionary in ES)
- Posting lists
- Compression

**Differenze**:
- **ES**: index structure in Lucene segment files, ottimizzato per search generiche e aggregazioni
- **TSIDX**: ottimizzato per time-series queries con time range primario
- **ES**: non ha bloom filters di default (usa bitset caching)
- **TSIDX**: bloom filters integrated per skip bucket-level
- **ES**: doc values per columnar aggregations (field-oriented)
- **TSIDX**: rawdata-oriented, field extraction a search time per molti campi

**Storage overhead**:
- ES: ~50-100% overhead (indice + doc values) rispetto a raw JSON
- Splunk: ~35% TSIDX + 15% rawdata = 50% totale, ma su dati pre-compression

Splunk è generalmente più efficiente su pure log analytics searches, ES è più flessibile per use case misti (search + aggregation + real-time analytics).

### TSIDX vs Columnar Formats (Parquet, ORC)

Columnar formats sono completamente diversi:

**TSIDX** (row-oriented su rawdata):
- Eventi stored integralmente in rawdata
- TSIDX punta a eventi completi
- Field extraction on-the-fly (tranne indexed fields)

**Columnar** (Parquet/ORC):
- Dati stored per column, non per row
- Compression migliore per column omogenee
- Aggregazioni su column specifiche velocissime
- Full row reconstruction più lento

Use case:
- **TSIDX**: log search, investigazione eventi, incident response
- **Columnar**: analytics batch, aggregazioni su dataset enormi, BI queries

Combinazioni ibride esistono: es. HDFS + Parquet per cold storage + Splunk per hot/warm queries.

## Quando TSIDX (e Splunk) Ha Senso

Dopo questa dissezione, quando dovresti usare Splunk nonostante i cost?

### Sweet Spot

- **SIEM e security analytics**: la velocità di TSIDX è critica per incident response. Paghi il premium perché "5 minuti invece di 30 minuti" per trovare un breach può valere milioni.
- **Operational troubleshooting**: quando un outage costa $100k/ora, query sub-second su mesi di log sono invaluable.
- **Compliance e audit**: retention lungo termine con search rapido su eventi storici, integrato con reporting.
- **SPL richness**: Splunk Processing Language è *estremamente* potente per correlation searches, statistical analysis, eccetera.

### Quando Considerare Alternative

- **Budget-constrained analytics**: se il primary use case è "analizza log per insights", non "troubleshooting real-time", considera Elasticsearch o OpenSearch (costo inferiore, licensing open).
- **Structured data analytics**: se i tuoi dati sono già strutturati (database query logs, transaction logs), columnar stores (ClickHouse, Druid) possono essere più efficienti.
- **Long-term archival**: per retention multi-year con rare searches, S3 + Athena o similari costano frazione di Splunk cold storage.

### Hybrid Approaches

Molti deployment enterprise usano:
- **Splunk**: hot data (7-30 giorni) per operational queries
- **S3/Data Lake**: cold data (>30 giorni) per compliance/archival
- **Presto/Athena**: query ad-hoc su cold data (lente ma economiche)

Questa architettura ottimizza TCO: paghi Splunk premium solo per hot tier dove la velocità conta, e usi storage economici per il resto.

## Takeaway Pratici

Se gestisci Splunk in produzione:

1. **Analizza i tuoi TSIDX ratio**: usa `| dbinspect index=<your_index>` per vedere rawdata size vs TSIDX size. Se ratio è >50%, hai optimization opportunities.

2. **Walklex sui bucket campione**: `splunk cmd walklex <bucket_path>` ti mostra lexicon composition. Cerca high-cardinality terms inutili.

3. **Tuna segmentation per i tuoi dati specifici**: non usare defaults ciecamente. Investi tempo in `segmenters.conf` custom.

4. **Enable tsidxWritingLevel=4** su indici nuovi (8.1+). Compression migliore a costo CPU trascurabile.

5. **Design retention tiers intelligentemente**: non tenere tutto in hot. Sposta warm/cold aggressivamente, usa SmartStore se su cloud.

6. **Educa gli utenti su query patterns**: wildcard suffix/infix e regex abuso uccidono performance. Keyword searches sono il tuo amico.

7. **Monitor bloom filter effectiveness**: se vedi query che leggono troppi bucket, bloom filters potrebbero essere undersized o false positive rate troppo alto (tuning in indexes.conf).

Se stai *valutando* Splunk:

- **Calcola TCO realisticamente**: licensing + storage + operational cost. Moltiplica storage raw per 2-3x per TSIDX overhead.
- **Benchmark sui tuoi dati**: Splunk performance varia enormemente con data characteristics. High-cardinality logs = TSIDX size esplosivo.
- **Confronta con alternative open**: OpenSearch + data prepper può coprire 70% degli use case Splunk a frazione del costo.

---

**Risorse e Approfondimenti**

- [Splunk Splexicon: TSIDX File](https://docs.splunk.com/Splexicon:Tsidxfile) - Definizione ufficiale
- [Splunk Splexicon: Bloom Filter](https://docs.splunk.com/Splexicon:Bloomfilter) - Bloom filter integration
- [Duane Waddle: Splunk Bucket Lexicons and Segmentation](https://www.duanewaddle.com/splunk-bucket-lexicons-and-segmentation/) - Case study ottimizzazione reale
- [XMLisse: How Splunk Search Works](https://xmlisse.wordpress.com/2020/05/20/splunkconf-how-search-works/) - Architettura search process
- [OpenSearch vs Splunk vs Elasticsearch vs Solr](/blog/posts/20260205_search-engines-comparison_v01.0/) - Comparazione platform (articolo correlato)
