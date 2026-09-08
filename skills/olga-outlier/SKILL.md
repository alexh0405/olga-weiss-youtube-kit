---
name: olga-outlier
description: >
  Findet YouTube-Outlier — Videos, die deutlich mehr Views bekommen haben als der Median aller
  gefundenen Videos in einem Zeitfenster (Standard: letzte 90 Tage) — fest zugeschnitten auf den
  Kanal von Olga Weiss (@OlgaWeissCoaching). Nutzt die YouTube Data API v3 (falls ein Key vorhanden
  ist) oder yt-dlp als Fallback (kein Key nötig).

  Zwei Modi:
  - **Olga-Recherche-Modus** (Standard): durchsucht die festen Referenzkanäle (eigener Kanal +
    Nischen-/Reichweiten-Peers, siehe `olga/reference-channels/channels.json`), extrahiert
    Keywords aus deren Top-Videos, findet verwandte Videos, die YouTube daneben vorschlägt, und
    führt die Outlier-Analyse auf dem kombinierten Datensatz aus. Braucht kein Argument.
  - **Keyword-Modus**: globale Stichwortsuche für ein einzelnes Thema außerhalb der festen
    Referenzkanäle.

  Trigger: "Finde Outlier für meine Nische", "was performt gerade gut im Bereich Technik-VA/KI",
  "YouTube-Recherche für Olga", "welche Videos schlagen gerade aus der Reihe", oder jede Frage nach
  über- oder unterdurchschnittlich performenden Videos in Olgas Themenfeld.
---

# YouTube Outlier Finder — Olga Weiss

Dieser Skill durchsucht YouTube nach Videos, die deutlich stärker performen als der Median —
verdeckte Perlen oder viraler Content in Olgas Nische (Technik/Tools/Prozesse, Schwerpunkt KI
im Arbeitsalltag von Dienstleisterinnen).

> **Pfad-Hinweis:** Alle Befehle gehen davon aus, dass dieser Skill unter
> `~/.claude/skills/olga-outlier/` installiert ist (inkl. mitkopiertem `brand/`-Ordner, siehe
> INSTALL.md im Repo). Der `SKILLDIR` lässt sich am Anfang einmal setzen:
> ```bash
> SKILLDIR="$HOME/.claude/skills/olga-outlier"   # ggf. anpassen
> ```

## Step 0 — Argumente parsen & Modus erkennen

Argumente kommen als String wie: `"claude workflow --days 60 --multiplier 2 --keyword-only"`

Parsen:
- Erstes/erste Nicht-Flag-Token(s) = optionales Keyword (mehrere Wörter, bis zum ersten `--`)
- `--days N` → Zeitfenster rückwärts (Standard: 90)
- `--multiplier X` → Outlier-Schwelle als Vielfaches des Medians (Standard: 1.5)
- `--top N` → maximale Anzahl gezeigter Outlier (Standard: 30)
- `--keyword-only` → erzwingt globalen Keyword-Modus statt Olga-Recherche-Modus

**Modus-Erkennung:**
- Standard (kein `--keyword-only`) UND ein gültiger `YOUTUBE_API_KEY` (>=30 Zeichen) ist gesetzt
  → **Olga-Recherche-Modus** (Step 1B) — läuft auch ganz ohne Keyword, dann gegen alle
  konfigurierten Referenzkanäle
- `--keyword-only` gesetzt UND ein Keyword vorhanden → **Keyword-Modus** (Step 1A)
- `--keyword-only` ohne Keyword → nachfragen: "Welches Keyword soll ich global durchsuchen?"
- **Kein gültiger `YOUTUBE_API_KEY` UND kein `--keyword-only`** → `research_pipeline.py` braucht
  zwingend einen echten API-Key (kein yt-dlp-Fallback in diesem Skript, anders als in Step 1A).
  Ohne Key automatisch auf **Keyword-Modus** (Step 1A, yt-dlp-Fallback) ausweichen, mit einem
  Hinweis: "Ohne YOUTUBE_API_KEY läuft die Referenzkanal-Recherche nicht — ich durchsuche
  stattdessen global über yt-dlp. Für die zielgenauere Referenzkanal-Recherche einen Key unter
  https://console.cloud.google.com/apis/credentials anlegen und als YOUTUBE_API_KEY setzen."

## Step 1A — Keyword-Modus (globale Suche)

### Fetch-Methode bestimmen

```bash
python3 - <<'EOF'
import os, shutil, sys

key = os.environ.get("YOUTUBE_API_KEY", "").strip()
ytdlp = shutil.which("yt-dlp") is not None
api_valid = len(key) >= 30

if key and not api_valid:
    print(f"API_ERROR: Key zu kurz ({len(key)} Zeichen, erwartet >=30).", file=sys.stderr)

print(f"API_VALID={api_valid}")
print(f"YTDLP={ytdlp}")
EOF
```

**Entscheidungslogik (in Reihenfolge):**
- `API_VALID=True` → **Methode A** (YouTube Data API)
- `API_VALID=False` und `YTDLP=True` → **Methode B** (yt-dlp)
- Beides nicht verfügbar → stoppen, Setup-Hinweis geben (siehe README)

### YouTube durchsuchen

**Methode A — YouTube Data API:**

```bash
python3 "$SKILLDIR/scripts/fetch_youtube.py" \
  --query "KEYWORD" \
  --days DAYS \
  --api-key "$YOUTUBE_API_KEY" \
  --order relevance \
  --output /tmp/youtube_raw.json
```

**Methode B — yt-dlp (Fallback):**

```bash
python3 "$SKILLDIR/scripts/fetch_youtube_ytdlp.py" \
  --query "KEYWORD" \
  --days DAYS \
  --count 50 \
  --timeout 120 \
  --output /tmp/youtube_raw.json
```

Schlägt Methode A fehl, ohne Rückfrage auf Methode B wechseln.

### Outlier berechnen

```bash
python3 "$SKILLDIR/scripts/analyze_outliers.py" \
  --input /tmp/youtube_raw.json \
  --multiplier MULTIPLIER \
  --top TOP \
  --metric combined \
  --output /tmp/youtube_outliers.json
```

Weiter mit **Step 2 — Bericht schreiben**.

## Step 1B — Olga-Recherche-Modus (Standard, Referenzkanal-Pipeline)

Bevorzugter Modus, **braucht aber zwingend einen gültigen `YOUTUBE_API_KEY`** —
`research_pipeline.py` hat anders als Step 1A keinen yt-dlp-Fallback (siehe Step 0). Durchsucht
die festen Referenzkanäle in
`$SKILLDIR/olga/reference-channels/channels.json`, extrahiert Keywords aus deren Top-Videos,
findet was YouTube daneben vorschlägt, und führt die Outlier-Analyse auf dem kombinierten
Datensatz aus. Ist ein Keyword angegeben, geht es zusätzlich als Suchbegriff in die Related-
Videos-Suche ein — ohne Keyword läuft die Pipeline rein über die Referenzkanäle.

**Kompletten Pipeline-Lauf:**

```bash
python3 "$SKILLDIR/scripts/research_pipeline.py" \
  --keyword "KEYWORD_ODER_LEER" \
  --client-dir "$SKILLDIR/olga" \
  --api-key "$YOUTUBE_API_KEY" \
  --days DAYS \
  --multiplier MULTIPLIER \
  --max-channels 10 \
  --top-per-channel 3 \
  --max-seeds 3
```

**Quota-Budget: ~321 Units pro Lauf → ~31 Läufe/Tag** (10k Tageslimit).

**Was die Pipeline intern macht (4 Schritte):**

1. **Kanal-Priorisierung + Upload-Scan** — Sortiert die Referenzkanäle nach `priority`-Feld
   (dann `subscribers`). Scannt nur die Top N Kanäle (`--max-channels`, Standard 10). Nutzt
   `playlistItems.list` (1 Unit) statt `search.list` (100 Units) für die letzten Uploads, filtert
   nach Keyword-Treffer im Titel (oder nimmt alle, wenn kein Keyword). Sammelt Top 3 je Kanal.
   Stoppt sofort bei API-Quota-Erschöpfung (403).
2. **Keyword-Extraktion** — Analysiert die Titel der Top-30-Videos, extrahiert wiederkehrende
   Bigramme/Trigramme (Rauschwörter DE + EN gefiltert). Das sind die Phrasen, um die der
   Algorithmus gerade clustert.
3. **Related Videos** — Nimmt die Top-10-Seed-Videos, leitet Suchanfragen aus deren Titeln ab
   (erste 5 sinntragende Wörter). Sucht YouTube pro Anfrage, um zu sehen, was der Algorithmus
   neben diesen Top-Performern vorschlägt. Dedupliziert gegen bekannte IDs.
4. **Outlier-Analyse** — Kombiniert Kanal-Videos + Related Videos, berechnet Median-Views und
   Median-Velocity (Views/Tag), markiert alles über multiplier×Median als Outlier. Rankt nach
   kombiniertem Durchschnitt aus Views-Rang + Velocity-Rang.

**Shorts:** werden von `research_pipeline.py`/`analyze_outliers.py` automatisch ausgefiltert
(Titel mit #shorts oder Dauer < 90s) — das ist fest im Code, kein Schalter nötig. Passt zum
eigenen Kanalbefund: ein Long-Form-Aufruf ist 15,1× so viel wert wie ein Short-Aufruf.

**Output:** JSON-Datei unter `olga/reports/research-<keyword>-<date>.json` (bzw. `-alle-` wenn
kein Keyword angegeben war).

Danach die JSON lesen und weiter mit **Step 2**.

## Step 2 — Bericht schreiben

Output-JSON lesen und mit dem Write-Tool den Bericht erzeugen.

**Dateiname:** `youtube-outlier-{keyword-slug-oder-olga}-{YYYY-MM-DD}.md`
Speicherort: aktuelles Arbeitsverzeichnis (Keyword-Modus) bzw. `olga/reports/` (Olga-Modus).

**Berichtsformat** (exakt diese Struktur verwenden):

```markdown
# YouTube Outlier Report: {keyword oder "Olga Weiss — Nische"}

**Analysezeitraum:** Letzte {days} Tage
**Analysiert am:** {date}
**Videos analysiert:** {totalVideosAnalyzed}
**Median Views:** {median} ({median_formatted})
**Durchschnitt Views:** {average} ({average_formatted})
**Outlier-Schwelle:** {threshold} ({multiplier}x Median)
**Outlier gefunden:** {count}

---

## Outlier-Videos

### {rank}. {title}

- **Kanal:** {channelTitle}
- **Views:** {viewCount_formatted} | **Views/Tag:** {viewsPerDayFormatted} ({velocityMultiple} Median)
- **Outlier-Multiple:** {outlierMultiple}
- **Veroeffentlicht:** {publishedAt_formatted} ({daysSincePublish} Tage her)
- **Likes:** {likeCount} | **Kommentare:** {commentCount} | **Engagement:** {engagementRate}
- **Kanal-Abonnenten:** {subscriberCount} *(nur bei yt-dlp verfügbar)*
- **Link:** {url}

[... für jeden Outlier wiederholen ...]

---
*Generiert mit olga-outlier | {totalVideosAnalyzed} Videos analysiert*
```

**Im Olga-Recherche-Modus** zusätzlich nach dem Header:

```markdown
**Modus:** Olga-Recherche
**Referenzkanaele:** {channelsSearched}
**Videos aus Kanaelen:** {totalVideosFromChannels}
**Related Videos:** {totalRelatedVideos}

## Extrahierte Keywords
{Liste der wiederkehrenden Phrasen mit Anzahl}
```

Zahlen mit Tausendertrennzeichen (`1.234.567`). Datum als `DD.MM.YYYY`.

**Edge Cases:**
- Keine Outlier gefunden → Top 10 nach View-Zahl mit Hinweis zeigen
- Weniger als 5 Videos gefunden → auf kleine Stichprobe hinweisen

## Step 3 — Zusammenfassung

Nach dem Schreiben der Datei eine knappe Zusammenfassung ausgeben:

```
Analyse abgeschlossen!

Videos analysiert:  {total}
Median Views:       {median_formatted}
Outlier gefunden:   {count} ({multiplier}x Median-Schwelle)
Bericht gespeichert: {filepath}
```

Im Olga-Recherche-Modus zusätzlich:
```
Referenzkanaele:    {channelsSearched}
Videos aus Kanaelen: {fromChannels}
Related Videos:     {related}
Top-Keywords:       {5 wichtigste extrahierte Keywords, kommagetrennt}
```

## Metriken — was bedeutet was?

- **Median Views:** Der mittlere View-Wert aller gefundenen Videos. Robuster als der Durchschnitt,
  weil einzelne Mega-Videos ihn nicht verzerren.
- **Outlier-Multiple:** Wie oft über dem Median ein Video liegt (z.B. `3.2x`). Je höher, desto
  stärker schlägt das Video aus der Reihe.
- **Velocity (Views/Tag):** Views geteilt durch Tage seit Veröffentlichung. Findet, was GERADE
  Fahrt aufnimmt.
- **Combined-Metrik (Standard):** Durchschnitt aus Views-Rang und Velocity-Rang.
- **Shorts werden standardmäßig gefiltert** — folgt dem eigenen Kanalbefund (siehe oben).

## Referenzkanäle pflegen

`$SKILLDIR/olga/reference-channels/channels.json` ist fest hinterlegt (Stand 06.09.2026, siehe
`brand/referenzkanaele.json` für die kuratierte Kurzfassung mit Begründung). Neue Kanäle einfach
in die `channels`-Liste ergänzen — `priority` (1–10) steuert die Scan-Reihenfolge.
