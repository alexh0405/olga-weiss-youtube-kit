# Olga Weiss — YouTube-Kit

Vier Claude-Code-Skills für den YouTube-Kanal **Olga Weiss** (@OlgaWeissCoaching) —
Outlier-Recherche, Skript-Erstellung, Video-Beschreibungen und Hook-Generator. Alle vier sind fest auf
den Kanal, die Zielgruppe und die Brand Voice zugeschnitten. Du musst nichts konfigurieren
oder ausfüllen — Thema, Link oder Transkript liefern reicht.

---

## Was kann ich damit erreichen?

1. **`olga-outlier`** — findet YouTube-Videos, die deutlich mehr Views bekommen als der Median:
   entweder gezielt über deine festen Referenzkanäle (Nische + Reichweiten-Vorbilder) oder über
   ein freies Stichwort. Zeigt dir, welches Thema/welche Verpackung gerade zieht.
2. **`olga-script`** — schreibt YouTube-Skripte und Content Outlines in deiner Brand Voice.
   Block für Block mit Freigabe nach jedem Schritt, inkl. Hook-Varianten, WWH-Struktur und
   einem festen Qualitäts-Check gegen ChatGPT-typische Formulierungen.
3. **`olga-description`** — transkribiert ein Video und schreibt dir die fertige YouTube-
   Beschreibung mit Timestamps, deinem CTA-Katalog und korrekten `https://`-Links.

4. **`olga-hook`** — schreibt Hook-Vorschläge in deiner Sprache und baut aus deinen eigenen Videos
   eine Hook-Datenbank mit Goldstandards. Du gibst deine Transkripte und die Zahlen aus YouTube Studio
   (Klickrate, Wiedergabedauer) hinein, so sieht der Generator, welche deiner Hooks wirklich
   funktioniert haben. Kein API-Key nötig.

Alle vier nutzen ein gemeinsames Kanal-Profil (`brand/`) — deine Positionierung, Zielgruppe,
Tonalität und CTA-Links sind an einer Stelle gepflegt.

---

## ⚡ Installation in 10 Sekunden (der einfachste Weg)

Öffne **Claude Code**, füge diese Zeile ein und schick sie ab:

```
Installier mir diesen Skill: https://github.com/alexh0405/olga-weiss-youtube-kit
```

Claude liest die `INSTALL.md` aus diesem Repo und installiert alle vier Skills automatisch nach
`~/.claude/skills/`. Danach Claude Code einmal neu starten — fertig.

> Falls Claude nachfragt: einfach bestätigen. Die Skills sind schreibgeschützt und sicher.

---

## Alternative: manuelle Installation

Siehe [INSTALL.md](INSTALL.md) für die Schritt-für-Schritt-Anleitung per Terminal.

---

## Beispielprompts

**Outlier-Recherche** (läuft ohne Argument gegen deine Referenzkanäle):
> "Finde Outlier für meine Nische der letzten 90 Tage"

**Skript schreiben:**
> "Schreib mir ein Skript über Claude-Cowork einrichten"

**Hook-Datenbank füllen** (einmal, mit deinen Transkripten und `Tabellendaten.csv` aus YouTube Studio):
> "Füll meine Hook-Datenbank. Die Transkripte liegen in [Ordner], die Studio-Zahlen in [Datei]."

**Hooks schreiben:**
> "Schreib mir 3 Hooks für ein Video über [Thema]"

**Beschreibung erstellen:**
> "Mach mir eine Beschreibung für https://youtube.com/watch?v=..."

---

## Umgebungsvariablen (beide optional)

| Variable | Pflicht? | Zweck |
|----------|----------|-------|
| `YOUTUBE_API_KEY` | Empfohlen | Für die Referenzkanal-Recherche (Standardmodus von `olga-outlier`) zwingend nötig — kein yt-dlp-Fallback dort. Ohne Key weicht `olga-outlier` automatisch auf globale Stichwortsuche über yt-dlp aus; `olga-script` verweist ohne Key generisch statt auf einen echten Videotitel. |
| `OPENAI_API_KEY` | Optional | Nur für `olga-description`, nur wenn ein Video keine YouTube-Untertitel hat (Whisper-Fallback). |

Setze die Variablen über die `.env` im Repo **oder** dauerhaft in deiner Shell (`~/.zshrc` / `~/.bashrc`):

```bash
export YOUTUBE_API_KEY="AIza...dein-key..."
```

---

## Repo-Struktur

```
olga-weiss-youtube-kit/
├── brand/                      Kanal-Profil, Brand Voice, Referenzkanäle (kanonische Quelle)
├── skills/
│   ├── olga-outlier/           Outlier-Recherche (eigene Kopie von brand/ inklusive)
│   ├── olga-script/            Skript & Outline (eigene Kopie von brand/ inklusive)
│   ├── olga-description/       Beschreibung & Timestamps (eigene Kopie von brand/ inklusive)
│   └── olga-hook/              Hook-Generator + Hook-Datenbank (eigene Kopie von brand/ inklusive)
├── .env.example
└── LICENSE
```

Jeder Skill trägt seine eigene Kopie von `brand/` in sich, damit er unabhängig funktioniert,
egal wohin er installiert wird. Wird die Positionierung oder Brand Voice aktualisiert: die
Dateien in `brand/` UND die Kopien in den vier `skills/*/brand/`-Ordnern anpassen.

---

## Lizenz

MIT — siehe [LICENSE](LICENSE).
