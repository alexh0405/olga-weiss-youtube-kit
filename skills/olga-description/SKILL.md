---
name: olga-description
description: "Transkribiert YouTube-Videos von Olga Weiss (@OlgaWeissCoaching) und erstellt individuelle Beschreibungen mit Timestamps — fest in ihrem Kanal-Stil und mit ihrem CTA-Katalog. Trigger, wenn jemand ein YouTube-Video transkribieren will, eine Beschreibung/Description erstellen oder schreiben will, Timestamps für ein Video generieren will, wichtige Momente aus einem Video extrahieren will, oder wenn einfach eine YouTube-URL geteilt wird mit der Bitte um eine Beschreibung, Timestamps, oder 'kannst du das transkribieren' / 'mach mir eine Beschreibung für mein Video'."
---

# YouTube Description Generator — Olga Weiss

Dieser Skill transkribiert YouTube-Videos (über Auto-Captions oder Whisper) und erstellt
individuelle Beschreibungen mit Timestamps — fest im Stil von Olga Weiss (@OlgaWeissCoaching).
Es gibt kein Kanalprofil zum Nachschlagen: Kanal, Tonalität und CTA-Katalog sind fest in
`brand/olga_channel.md` hinterlegt.

## Workflow

### Schritt 1: Eingaben sammeln

Fragen (oder aus dem Kontext ableiten):
- **YouTube-URL** (Pflicht)
- **Sprache**: Ausgabesprache (DE, EN, oder beides). Standard: Sprache des Videos.
- **Besondere Wünsche**: was betont oder anders strukturiert werden soll.
- **War das Thumbnail dieses Videos KI-generiert oder KI-bearbeitet und zeigt es Olga?**
  (steuert den KI-Transparenzhinweis in Schritt 5b — im Zweifel fragen, nicht annehmen)

### Schritt 2: Transkript extrahieren

```bash
python <skill_dir>/scripts/get_transcript.py "<youtube_url>" --lang <lang> --output /tmp/transcript.json
```

- `<skill_dir>` ist der Ordner, der diese SKILL.md enthält
- `--lang`: `de` für deutschsprachig zuerst, `en` für englisch zuerst
- Das Skript versucht zuerst YouTube-Auto-Captions (kostenlos, schnell), fällt sonst auf die
  OpenAI-Whisper-API zurück

**Falls yt-dlp nicht installiert ist:**
```bash
pip install yt-dlp
```

**Falls der Whisper-Fallback gebraucht wird und openai nicht installiert ist:**
```bash
pip install openai
# OPENAI_API_KEY muss gesetzt sein
```

Output `/tmp/transcript.json` lesen. Enthält:
```json
{
  "title": "Video title",
  "source": "captions" | "whisper",
  "segments": [
    {"start": 0.0, "end": 12.5, "text": "...", "timestamp": "0:12"}
  ]
}
```

### Schritt 3: Transkript analysieren

Alle Segmente lesen, um die Struktur des Videos zu verstehen:
- Was sind die Hauptthemen/Abschnitte?
- Wo passieren Themenwechsel? (werden zu Timestamp-Markern)
- Was ist die Kernbotschaft / das Nutzenversprechen?
- Was sind wichtige Momente, Tipps oder Highlights?
- **Leitfrage im Hinterkopf:** Wie verdient man mit dem im Video Gezeigten Geld / löst es das
  konkrete Problem der Zuschauerin?

Ziel: 5–12 Timestamp-Einträge je nach Videolänge:
- Videos <10 Min: 4–7 Timestamps
- Videos 10–30 Min: 7–12 Timestamps
- Videos >30 Min: 10–15 Timestamps

Timestamps an natürlichen Brüchen wählen (Themenwechsel, neue Abschnitte, Q&A-Start etc.).

### Schritt 4: Kanal-Profil laden

`brand/olga_channel.md` lesen für:
- Ton & Stil (ruhig, bodenständig, klartextlich, Du-Anrede)
- Zielgruppe und innere Gedanken (für die Eröffnungszeilen)
- Festen CTA-Block und Beschreibungs-Timeline
- Content-Pillar-Einordnung des Videos

### Schritt 5: Beschreibung generieren

Vollständige Video-Beschreibung nach Olgas Stil und Struktur schreiben.

**Immer enthalten:**
- Eine mitreißende Eröffnung, die die Zuschauerin abholt (kein Clickbait, kein Hype —
  siehe `banned_words_or_patterns` in `brand/olga_brand_voice.json`)
- Eine Zusammenfassung dessen, was das Video abdeckt (was lernt/bekommt die Zuschauerin?)
- Eine Timestamps-Sektion mit exakten Zeiten aus dem Transkript
- **Den Audit-Link an erster Stelle** im CTA-Block (siehe `brand/olga_channel.md`,
  Abschnitt "Fester CTA-Block"), mit `?utm_source=youtube&utm_medium=description`
- **Alle Links vollständig mit `https://`** — YouTube macht sonst keinen klickbaren Link daraus
  (Domains ohne Protokoll-Präfix bleiben Plain Text)
- Passende Hashtags (2–5, thematisch, keine Hashtag-Stapelung)
- **Den KI-Transparenzhinweis-Block (Schritt 5b) — nur wenn zutreffend, siehe dort**

**Timestamp-Format:**
Immer `0:00` als Format für Zeiten unter 10 Minuten, `00:00` für den allerersten Eintrag.
YouTube aktiviert die Kapitel-/Timestamp-Funktion nur, wenn die Liste mit `0:00` beginnt.
`M:SS` bis 59:59, `H:MM:SS` über eine Stunde. Jeder Timestamp bekommt einen kurzen,
beschreibenden Titel (nicht den rohen Transkript-Text).

**Beispiel Timestamps-Sektion:**
```
⏱️ Timestamps
0:00 Intro
1:45 Das Problem
4:20 Lösung Teil 1
8:30 Live-Demo
12:15 Häufige Fehler
15:00 Fazit & nächste Schritte
```

WICHTIG: Die Timestamp-Liste MUSS immer mit `0:00` beginnen — sonst aktiviert YouTube die
Kapitel-Funktion nicht.

### Schritt 5b: KI-Transparenzhinweis (nur wenn zutreffend — vorher prüfen, nicht automatisch anhängen)

Olgas Thumbnails sind laut Design-Vorgabe **echte Fotos, kein KI-generiertes Abbild ihrer
Person** (siehe `brand/olga_channel.md`). Der folgende Block ist eine rechtliche
Kennzeichnungspflicht (EU AI Act, Art. 50 — Transparenzpflichten für KI-generierte/-manipulierte
Inhalte, die eine reale Person zeigen) und darf **nur** angehängt werden, wenn das Thumbnail
dieses konkreten Videos tatsächlich KI-generiert oder KI-bearbeitet ist und Olga (oder eine
andere reale Person) zeigt. Bei Unsicherheit in Schritt 1 nachfragen, nicht automatisch
annehmen — ein falscher Hinweis ist genauso falsch wie ein fehlender.

```
🤖 KI-Transparenzhinweis
Das Vorschaubild dieses Videos wurde mithilfe Künstlicher Intelligenz erstellt bzw. bildlich verändert. Die dort gezeigte Darstellung ist eine KI-generierte Nachbildung, keine reale Fotografie oder Videoaufnahme. Kennzeichnung gemäß Art. 50 der Verordnung (EU) 2024/1689 (KI-Verordnung).
```

- **Platzierung:** ganz am Ende der Beschreibung, nach Timestamps, CTA-Block, Links und Hashtags.
- **Nicht anhängen**, wenn das Thumbnail ein echtes Foto ist (Olgas Standard-Fall) — dann endet
  die Beschreibung mit den Hashtags.

### Schritt 6: Im Chat ausgeben

Die Beschreibung direkt im Chat ausgeben — keine Datei, kein Code-Block, keine dreifachen
Backticks, keine Markdown-Formatierung.

Einfach den rohen Beschreibungstext so schreiben, wie er auf YouTube erscheinen wird. Nicht
in einen Container packen.

Nach der Beschreibung, auf einer neuen Zeile, fragen: "Passt der Stil? Soll ich etwas anpassen?"

---

## Tipps für gute Beschreibungen

- Die **ersten 2–3 Zeilen** werden vor "Mehr anzeigen" angezeigt — die müssen zählen.
- **Timestamps verbessern die Retention** — Zuschauerinnen springen zu dem, was sie wollen; das ist okay.
- **Nicht zu wörtlich zusammenfassen** — die Beschreibung soll zum Schauen motivieren, nicht das Schauen ersetzen.
- **SEO**: das Hauptthema natürlich als Phrase im ersten Absatz einbauen, nicht erzwungen.
- Leitfrage im Hinterkopf behalten: "Wie verdient man damit Geld?" — auch die Beschreibung darf
  auf das Ergebnis zeigen, nicht nur auf das Tool.

---

## Troubleshooting

| Problem | Lösung |
|---|---|
| `yt-dlp: command not found` | `pip install yt-dlp` |
| Keine Captions gefunden | Skript fällt automatisch auf Whisper zurück |
| Whisper schlägt fehl: kein API-Key | `export OPENAI_API_KEY=sk-...` |
| Captions in falscher Sprache | `--lang en` oder `--lang de` explizit übergeben |
| Video sehr lang (>2h) | Whisper kann timeout — wenn möglich Captions nutzen |

## Referenzen (alle im Skill-Ordner, self-contained)
- `brand/olga_channel.md` — Kanal-Profil, Zielgruppe, fester CTA-Block, Beschreibungs-Timeline
- `brand/olga_brand_voice.json` — Ton, Wortfelder, Verbote
- `scripts/get_transcript.py` — Transkription (Captions oder Whisper-Fallback)
