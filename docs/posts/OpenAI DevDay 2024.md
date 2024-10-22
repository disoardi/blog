---
Created time: 2024-10-03
Last update: 2024-10-03
Status: Done
tags:
  - AI
  - openai
  - generativeAI
date: 2024-10-02
authors:
  - abacus
pgType: blog
---
Si sono appena conclusi gli OpenAI DevDay ed hanno annunciato:  

- RealTime API
- Vision Fine-Tuning
- Prompt Caching
- Distillation
## RealTime API
[Documentation](https://platform.openai.com/docs/guides/realtime)  
Tramite web socket è possibile creare esperienze più immediate con l'AI generativa. Si tratta quindi di API a bassa latenza che si interfacciano con i modelli anche multi-modali (text e image generation per esempio).  
E' simile alla funzionalità all'Advance Voic Mode di ChatGPT e attualmente supporta le sei voci preimpostate.  
Tale funzionalità è stata implementate anche nella modalità chat (con GPT-4o) al quale quindi puoi passare testo e/o audio e chiedere una risposta in testo e/o audio.  

Per comprendere l'importanza di questa novità in precedenza per creare un'esperienza vocale di interazione l'applicazione doveva:  

1. trascivere l'audio con un modello dedicato tipo Whisper  
2. passare il testo ad un modello di inferenza o reasoning  
3. infine usare un modello text-to-speech per creare la risposta audio  

Oltre ad essere un processo lungo questo porta a snaturare e perdere l'emotività trasmessa nel tono dell'audio. Con le Chat Completions API questo processo è stato "nascosto" ma in sostanza il lavoro svolto, con i suoi difetti, rimaneva lo stesso.  
Under the hood le RT API aprono un socket persistente con il modello tramite il quale è possibile streammare audio direttamente in input e in output.  
Inoltre è presente il function calling, rendendolo di fatto un agente in quanto l'AI può integrarsi con servizi, chiamare funzioni, scrivere mail, cercare sul web...  

## Vision Fine-Tuning
[Documentation](https://platform.openai.com/docs/guides/fine-tuning/vision)
Il fine tuning dei modelli che possono generare immagini (come GPT-4o) avveniva indicando testualmente come mentre ora è possibile integrare con immagini questo processo:  
``` JSON
{
  "messages": [
    { "role": "system", "content": "You are an assistant that identifies uncommon cheeses." },
    { "role": "user", "content": "What is this cheese?" },
    { "role": "user", "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://upload.wikimedia.org/wikipedia/commons/3/36/Danbo_Cheese.jpg"
          }
        }
      ] 
    },
    { "role": "assistant", "content": "Danbo" }
  ]
}
```

Questo aumenta sensibilmente l'accuratezza anche con pochi esempi utilizzati per il fine-tuning.  
Questo approccio è molto interessante anche per l'ambito RPA e portano a esempio una specializzazione di un agente ad utilizzare una interfaccia grafica per compiere azioni come se fosse un operatore. Per fare questo è stata usata questa nuova possibilità di fine-tuning.  
## Prompt Caching
[Documentation](https://platform.openai.com/docs/guides/prompt-caching)  
In pratica se diversi utenti fanno lo stesso prompt/domanda il modello usa la cache senza invocare nuovamente il modello, riducendo i costi. In pratica fa quello per cui è stato sviluppato GPTCache (ne avevo parlato già [qui](https://github.dxc.com/pages/disoardi/LLM-architecture-reference/LLM%20Functional%20Architecture/#llm-cache) e [qui](https://github.dxc.com/pages/disoardi/LLM-architecture-reference/Technologies/)).  
## Model Distilation
[Documentation](https://platform.openai.com/docs/guides/distillation)  
La distillazione è una tecnica che consiste nel prendere un modello molto grande ma ridurlo di dimensioni. Tecnicamente si prende un modello più piccolo e lo si addestra sull'output del modello più grande.  
Questo approccio è ora disponibile tramite API.