#!/usr/bin/env python3
"""
Article Generator Module
Uses Claude Code CLI to generate blog articles about Home Assistant releases.
"""

import os
import logging
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class ArticleGenerator:
    """Generate blog articles using Claude Code CLI."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the article generator."""
        self.config = config
        self.blog_root = Path(config['blog']['root_path'])
        self.post_dir = self.blog_root / config['blog']['post_dir']
        self.img_dir = self.blog_root / config['blog']['img_dir']

        # Load guidelines
        guidelines_path = self.blog_root / "Claude.md"
        with open(guidelines_path, 'r') as f:
            self.guidelines = f.read()

        # Check if claude CLI is available
        if not self._check_claude_cli():
            raise RuntimeError("Claude Code CLI not available. Please install it first.")

    def _check_claude_cli(self) -> bool:
        """Check if claude CLI is available."""
        try:
            result = subprocess.run(
                ['claude', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def _build_prompt(self, release_data: Dict[str, Any]) -> str:
        """Build the prompt for Claude to generate the article."""

        version = release_data['version']
        title = release_data['title']
        url = release_data['url']
        content = release_data['content']

        prompt = f"""IMPORTANTE: Questo è un task automatizzato. Rispondi SOLO con il contenuto dell'articolo in markdown. NON fare domande, NON essere conversazionale, NON chiedere conferme.

TASK: Scrivi un articolo completo in italiano per il mio blog tecnologico sulla release di Home Assistant {version}.

OUTPUT RICHIESTO: Solo il contenuto dell'articolo in formato markdown, nient'altro.

# Informazioni sulla Release

**Titolo originale**: {title}
**URL**: {url}
**Versione**: {version}

**Contenuto dell'annuncio ufficiale**:
```
{content[:8000]}  # Limit content to avoid token limits
```

# LINEE GUIDA OBBLIGATORIE (dal file Claude.md - sezione "Linee Guida per Claude - writer degli articoli")

DEVI ASSOLUTAMENTE seguire queste linee guida per rispecchiare il mio stile e la mia personalità:

{self.guidelines}

ATTENZIONE: Queste linee guida sono FONDAMENTALI. L'articolo DEVE riflettere:
- Il mio carattere: nerd old-school, non quello figo moderno
- Passioni: fantascienza (Star Trek ❤️, non Star Wars), D&D, giochi da tavolo tedeschi
- Valori: FOSS, self-hosting, pirateria come libertà di espressione
- Background: leader centro eccellenza Hadoop, Italian Linux Society
- Contesto familiare: padre di famiglia che preferisce grigliate nerd alle cose di moda

# Requisiti Specifici per questo Articolo

1. **Focus principale**: Concentrati sulle novità più rilevanti, in particolare su:
   - Nuove integrazioni (device e servizi supportati)
   - Miglioramenti alle automazioni e scripting
   - Performance e ottimizzazioni architetturali

2. **Struttura**:
   - Inizia con un'introduzione coinvolgente in stile colloquiale
   - TL;DR: breve riassunto esecutivo
   - Analisi delle novità principali (5-10 punti chiave)
   - Valutazioni personali sulle implicazioni per la community self-hosting
   - NO sezione "Conclusione" (come da linee guida)

3. **Stile**:
   - Tono colloquiale e personale come se raccontassi a un amico
   - Considera la mia prospettiva: nerd, sostenitore del FOSS, hobbista self-hosting
   - Variare lunghezza delle frasi, usare espressioni informali
   - Evitare frasi AI tipiche ("in conclusione", "approfondire", "sfruttare", ecc.)
   - Inserire opinioni personali e valutazioni basate sull'esperienza

4. **Contenuto**:
   - Includi link diretti alle integrazioni GitHub se rilevanti
   - Se menzioni numeri o statistiche, devono essere REALI dal contenuto
   - NO dati inventati
   - Riferimenti a progetti open source quando possibile

5. **Formato**:
   - Output in Markdown
   - Rispetta la naming convention per le immagini se necessarie
   - Usa heading chiari ma non eccessivamente strutturati

6. **Metadata in testa**:
   - TL;DR breve
   - Riassunto esteso

Genera SOLO il contenuto dell'articolo in markdown, senza aggiungere commenti o note esterne al contenuto stesso.
"""

        return prompt

    def generate_article(self, release_data: Dict[str, Any]) -> Optional[Path]:
        """
        Generate an article using Claude Code CLI.
        Returns the path to the generated article file.
        """
        try:
            logger.info(f"Generating article for {release_data['version']}")

            # Build prompt
            prompt = self._build_prompt(release_data)

            logger.info("Calling Claude Code CLI via stdin (non-interactive mode)...")

            try:
                # Call Claude Code CLI via stdin instead of file
                # This should trigger a more direct, non-conversational response
                result = subprocess.run(
                    ['claude', 'chat'],  # Use 'chat' command which can accept stdin
                    input=prompt,
                    capture_output=True,
                    text=True,
                    timeout=300,  # 5 minutes timeout
                    cwd='/tmp'  # Use neutral directory to avoid workspace context
                )

                if result.returncode != 0:
                    logger.error(f"Claude CLI failed with code {result.returncode}")
                    logger.error(f"Error output: {result.stderr}")
                    return None

                # Extract article content from output
                article_content = result.stdout.strip()

                if not article_content:
                    logger.error("Claude CLI returned empty content")
                    return None

                # Check if response is still conversational (red flag phrases)
                conversational_indicators = [
                    "How can I help",
                    "What would you like",
                    "I'm ready to",
                    "Posso aiutarti",
                    "Cosa vorresti"
                ]

                if any(indicator.lower() in article_content.lower()[:200] for indicator in conversational_indicators):
                    logger.error("Claude CLI returned conversational response instead of article")
                    logger.error(f"Response preview: {article_content[:500]}")
                    logger.error("This indicates the prompt is not being interpreted as a task")
                    return None

                # Generate filename
                today = datetime.now()
                version_clean = release_data['version'].replace('.', '')
                filename = f"{today.strftime('%Y%m%d')}_home-assistant-{version_clean}_v01.0.md"
                article_path = self.post_dir / filename

                # Ensure directory exists
                self.post_dir.mkdir(parents=True, exist_ok=True)

                # Save article
                with open(article_path, 'w', encoding='utf-8') as f:
                    f.write(article_content)

                logger.info(f"Article saved to: {article_path}")
                return article_path

            finally:
                # Clean up temp prompt file
                try:
                    os.unlink(prompt_file_path)
                except:
                    pass

        except subprocess.TimeoutExpired:
            logger.error("Claude CLI timed out after 5 minutes")
            return None
        except Exception as e:
            logger.error(f"Error generating article: {e}", exc_info=True)
            return None

    def generate_article_manually(self, release_url: str, version: str) -> Optional[Path]:
        """
        Manually trigger article generation with a URL.
        Useful for testing or manual invocation.
        """
        # Fetch content
        import requests
        from bs4 import BeautifulSoup

        try:
            response = requests.get(release_url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            content = soup.find('article') or soup.find('div', class_='content')

            if not content:
                logger.error("Could not extract content from URL")
                return None

            release_data = {
                'version': version,
                'title': f'Home Assistant {version}',
                'url': release_url,
                'content': content.get_text(separator='\n', strip=True)
            }

            return self.generate_article(release_data)

        except Exception as e:
            logger.error(f"Error in manual generation: {e}", exc_info=True)
            return None


if __name__ == "__main__":
    # Allow manual testing
    import sys
    import yaml

    if len(sys.argv) < 3:
        print("Usage: python article_generator.py <release_url> <version>")
        print("Example: python article_generator.py https://www.home-assistant.io/blog/2026/02/... 2026.02")
        sys.exit(1)

    logging.basicConfig(level=logging.INFO)

    with open('automation/config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    generator = ArticleGenerator(config)
    article_path = generator.generate_article_manually(sys.argv[1], sys.argv[2])

    if article_path:
        print(f"Article generated: {article_path}")
    else:
        print("Article generation failed")
        sys.exit(1)
