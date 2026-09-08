# Installation für Claude Code

Kurzanleitung, um alle drei Skills in Claude Code einsatzbereit zu machen.

## Schnellweg

```bash
# 1. Repo holen
git clone https://github.com/alexh0405/olga-weiss-youtube-kit.git
cd olga-weiss-youtube-kit

# 2. Skills ins Claude-Code-Verzeichnis kopieren (jeder bringt sein eigenes brand/ mit)
mkdir -p ~/.claude/skills
cp -R skills/olga-outlier      ~/.claude/skills/olga-outlier
cp -R skills/olga-script       ~/.claude/skills/olga-script
cp -R skills/olga-description  ~/.claude/skills/olga-description

# 3. Konfiguration anlegen (beide Werte optional)
cp .env.example .env
# .env öffnen und YOUTUBE_API_KEY / OPENAI_API_KEY eintragen, falls gewünscht

# 4. Optionaler Fallback fuer olga-outlier und olga-description ohne API-Key
pip install yt-dlp
```

Danach Claude Code einmal neu starten. Dann z. B.:

> "Finde Outlier für meine Nische der letzten 90 Tage"

oder:

> "Schreib mir ein Skript über [dein Thema]"

oder:

> "Mach mir eine Beschreibung für [YouTube-Link]"

## Per Claude Code installieren lassen

Du kannst Claude Code auch direkt bitten:

> "Installier mir die Skills aus https://github.com/alexh0405/olga-weiss-youtube-kit —
>  klone das Repo und kopiere die drei Ordner aus `skills/` nach `~/.claude/skills/`."

## Umgebungsvariablen

| Variable | Pflicht? | Zweck |
|----------|----------|-------|
| `YOUTUBE_API_KEY` | Empfohlen | Für die Referenzkanal-Recherche (Standardmodus von `olga-outlier`) zwingend nötig — kein yt-dlp-Fallback dort. Ohne Key weicht `olga-outlier` automatisch auf globale Stichwortsuche über yt-dlp aus; `olga-script` verweist ohne Key generisch statt auf einen echten Videotitel. |
| `OPENAI_API_KEY` | Optional | Nur für `olga-description`, nur wenn ein Video keine YouTube-Untertitel hat (Whisper-Fallback). |

```bash
export YOUTUBE_API_KEY="AIza...dein-key..."
export OPENAI_API_KEY="sk-...dein-key..."
```

## Verifizieren

```bash
# olga-outlier: Trockenlauf über den yt-dlp-Fallback (braucht keinen Key)
python3 ~/.claude/skills/olga-outlier/scripts/fetch_youtube_ytdlp.py \
  --query "claude code" --days 90 --count 20 --output /tmp/raw.json
python3 ~/.claude/skills/olga-outlier/scripts/analyze_outliers.py \
  --input /tmp/raw.json --multiplier 1.5 --top 10 --output /tmp/out.json

# olga-script: Live-Kanal-Daten holen (braucht Key, sonst sauberer Fallback)
python3 ~/.claude/skills/olga-script/scripts/youtube_live.py --recent 5

# olga-description: Skript-Hilfe anzeigen
python3 ~/.claude/skills/olga-description/scripts/get_transcript.py --help
```

Wenn alle drei Befehle ohne Fehler durchlaufen, ist alles startklar.

## Deinstallation

```bash
rm -rf ~/.claude/skills/olga-outlier ~/.claude/skills/olga-script ~/.claude/skills/olga-description
```
