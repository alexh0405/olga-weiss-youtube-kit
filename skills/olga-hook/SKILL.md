---
name: olga-hook
description: Erstellt Hook-Vorschläge für neue Olga-Weiss-Videos (@OlgaWeissCoaching) in ihrer Sprache und baut aus ihren eigenen Videos eine Hook-Datenbank mit Goldstandards. Verbindet die Transkripte, die Olga schon hat, mit den YouTube-Studio-Zahlen (Klickrate und Wiedergabedauer), damit erkennbar wird, welche ihrer Hooks wirklich funktioniert haben. Modus A - Hook generieren ("Hook für Olga", "Hook-Vorschläge für mein Video", "Schreib mir 3 Hooks zu [Thema]", oder eine Outline/ein Thema liefern und nach dem Einstieg fragen). Modus B - Datenbank füllen oder aktualisieren ("Hook-Datenbank füllen", "meine Videos in den Hook-Generator", "Goldstandards aus meinen Videos", "neue Studio-Zahlen", "Datenbank aktualisieren"). Kein API-Key nötig.
---

# Olga Weiss — Hook-Generator

Schreibt Hook-Vorschläge, die nach Olga klingen und auf Einstiegen aufsetzen, die in ihrem eigenen Kanal
nachweislich funktioniert haben. Die Hook-Datenbank baut sie aus den Transkripten, die sie ohnehin
hat, plus den Zahlen aus YouTube Studio.

Kanal: `@OlgaWeissCoaching` · Channel-ID `UC3BPfoLoiJaVshDvSUH7p9Q`

## Zuerst lesen (jedes Mal)

1. `brand/olga_brand_voice.json` — Tonalität, Wortfelder, Verbote, Signaturphrasen, 7 Hook-Typen, 4C-Rahmen.
2. `brand/olga_channel.md` — Zielgruppe, innere Gedanken, Anti-Patterns, Zielkorridore.
3. `references/hook-theory.md` — Typ-Definitionen, 4C-Struktur, CTR/Retention-Diagnose.
4. Vor jedem Hook-Output: `hard_rules.md` des Schwester-Skills `olga-script`
   (`~/.claude/skills/olga-script/references/hard_rules.md`). Sie hat Vorrang vor allem hier. Fehlt die
   Datei, sag es Olga, statt ohne sie zu prüfen.

## Datenordner

Alles, was Olga aufbaut, liegt in `~/Documents/olga-hook/` (oder dort, wohin `OLGA_HOOK_DATA` zeigt).
Der Ordner bleibt bei Skill-Updates erhalten.

| Datei | Inhalt | Wer schreibt |
|---|---|---|
| `hooks.json` | Master-Datenbank: Zahlen, Hook-Text, Einordnung je Video | `scripts/hook_db.py` |
| `hook-datenbank.md` | lesbare Fassung, Ranglisten, Muster | wird aus `hooks.json` neu erzeugt, nie von Hand ändern |
| `goldstandard-hooks.md` | Index der von Olga freigegebenen Hooks (Datum + Titel) | Claude, nur nach Olgas Freigabe |
| `videos/<JJJJ-MM-TT>-<slug>/hook.md` | je freigegebener Hook mit vollem Sprechtext | Claude, nur nach Olgas Freigabe |

Skript: `python3 ~/.claude/skills/olga-hook/scripts/hook_db.py` (nur Standardbibliothek, Python 3.9+).
Auf Windows `python` statt `python3`.

## Modus B — Datenbank füllen oder aktualisieren

Trigger: siehe Beschreibung. Auch ganz am Anfang, wenn `hooks.json` noch nicht existiert. Existiert sie
nicht und Olga wünscht einen Hook, führe zuerst diesen Modus aus.

**Warum Transkript UND Zahlen:** Das Transkript liefert den wörtlichen Hook und Olgas Sprache. Ob er
funktioniert hat, sagen nur die Zahlen. Ohne Zahlen wäre jeder Hook gleich viel wert.

**Was Olga bereitstellt:**
1. **Transkripte** aller Videos in einem Ordner (`.txt`, `.md`, `.srt`, `.vtt`), ein Video pro Datei.
   Der Dateiname sollte die Video-ID oder den Videotitel enthalten. Zeitstempel sind nicht nötig.
2. **`Tabellendaten.csv`** aus YouTube Studio: Analytics → Erweiterter Modus → Zeitraum **Gesamt** →
   Tab **Videos** → oben rechts *Aktuelle Daten exportieren → CSV*. Aus dem Download reicht
   `Tabellendaten.csv`. Benötigte Spalten: Videos (ID), Videotitel, Veröffentlichungszeitpunkt, Dauer,
   Durchschnittliche Wiedergabedauer, Aufrufe, Impressionen, Klickrate. Fehlt eine, nennt das Skript den
   Spaltennamen. Dann in Studio die Spalte einblenden und neu exportieren.

**Ablauf:**
1. Pfade klären (max. 2 Rückfragen). Olga kann die Dateien in den Chat ziehen oder den Ordnerpfad nennen.
2. Bestätigen: „Ich lese deine Transkripte und die Studio-Zahlen lokal ein. Nichts wird hochgeladen, es
   kostet nichts."
3. Ausführen:
   ```bash
   python3 ~/.claude/skills/olga-hook/scripts/hook_db.py build \
     --studio "<Pfad zu Tabellendaten.csv oder Ordner>" --transcripts "<Ordner mit Transkripten>"
   ```
   Schwellen (Vorschlag, per Argument änderbar): `--min-impressions 1000`, `--min-views 100`,
   `--min-age-days 28`, `--min-duration 180` (kürzere Videos gelten als Shorts), `--hook-seconds 60`,
   `--hook-words 160`.
4. **Bericht an Olga, vollständig und ehrlich:** Zeilen in der Tabelle, ausgeschlossene Videos mit den
   Gründen, zugeordnete Transkripte, jede Zeile ohne Partner (Zahlen ohne Transkript, Transkript ohne
   Zuordnung). Zuordnungen nie raten. Bei Unklarheit frag Olga, welches Transkript zu welchem Video
   gehört, und benenne die Datei um oder lass sie umbenennen.
5. **Kleine Stichprobe offen sagen.** Olgas Kanal ist klein. Bleiben nach den Filtern wenige Videos
   übrig, nenne die Zahl und schlage vor, `--min-impressions` zu senken (z. B. 300), mit dem Hinweis, dass
   die Klickrate dann stärker schwankt. Unter 15 Videos: Ranglisten sind Tendenzen, keine Belege. Das
   Skript gibt die Warnung selbst aus.
6. **Einordnen (`tag`).** Lies aus `hooks.json` die `hook_text`-Felder der Videos ohne `tags`, in Gruppen
   zu je 8–10. Ordne jedes Video ein nach den Definitionen in `references/hook-theory.md`:
   - `hook_type` — einer von Olgas 7 Typen
   - `first_liner_type` — einer der 10 First-Liner-Typen
   - `beats` — nur Bausteine des 4C-Rahmens, die im Text wirklich vorkommen, in Reihenfolge
   - `tension_pattern` — ein dominantes Muster
   - `language` — `signature_phrases`, `verbs`, `anchors`: nur wörtliche Zitate aus dem Hook-Text
   - `note` — optional, z. B. „kein Click-Confirmation, steigt mit Werbung ein"

   Nichts ergänzen, was nicht dasteht. Schreibe die Einordnung als JSON `{"<video_id>": {…}}` in eine
   Wegwerf-Datei und übernimm sie mit:
   ```bash
   python3 ~/.claude/skills/olga-hook/scripts/hook_db.py tag --file "<Wegwerf-Datei>"
   ```
   Meldet das Skript unbekannte Typen oder Beats, korrigiere und wiederhole. Ein erneutes `build` behält
   die Einordnung, solange sich der Hook-Text nicht ändert.
7. **Goldstandard-Vorschlag.** Nenne die Videos mit Muster `doppel_champion` (Klickrate UND Retention im
   oberen Bereich) als Kandidaten, jeweils mit einem Satz, warum der Hook trägt. In `goldstandard-hooks.md`
   kommt nichts, bevor Olga einen Kandidaten ausdrücklich freigibt (Persistenz, siehe unten).
8. **Abschlussbericht, kurz:** wie viele Videos in der Datenbank, Verteilung der Hook-Typen bei
   Doppel-Champions gegenüber dem Rest, welcher Typ überwiegt und wie belastbar das bei dieser Größe ist,
   die 3 Videos mit dem größten Abstand zwischen Klickrate und Retention. Nächster Schritt: nach 4–6 neuen
   Videos einen frischen Studio-Export machen und `build` wiederholen.

### Wie die Zahlen zu lesen sind

Klickrate (CTR) misst die Verpackung: Titel und Thumbnail. Retention misst, ob das ganze Video hielt,
was der Klick versprach. Beide werden getrennt geführt und **nie zu einem Score verrechnet**.

Retention wird als Ø Wiedergabedauer geteilt durch Videolänge berechnet. Die Studio-Spalte „Bis zum Ende
angesehen (%)" ist eine andere Kennzahl und wird nicht verwendet.

**Grenzen, die Olga genannt werden müssen:** (1) Retention ist ein Wert fürs ganze Video, nicht für die
ersten Sekunden. Es gibt in diesen Exporten keine Daten dazu, an welcher Sekunde jemand aus dem Hook
aussteigt. (2) Die Klickrate misst vor allem Titel und Thumbnail, nicht den Hook. Deshalb sind
Doppel-Champions das stärkste Signal, alles andere ist schwächer. Ein genaueres Hook-Signal hat Olga
selbst: In Studio zeigt die Zuschauerbindung pro Video, wie viele nach 30 Sekunden noch dabei sind (falls
sichtbar). Nennt sie dir den Wert, führe ihn in `note` und gewichte ihn beim Hook-Urteil höher als die
Video-Retention.

Muster (Grenzen: Perzentil ≥ 0,70 hoch, ≤ 0,40 niedrig; Olgas Korridor CTR > 4 %, Retention > 25 %):

| Muster | Bedeutung | Konsequenz für den nächsten Hook |
|---|---|---|
| `doppel_champion` | Verpackung und Halt tragen | Typ und Beat-Struktur bevorzugt als Vorbild |
| `halt_ohne_klick` | Video stark, zu wenig gesehen | Hook als Vorbild nutzbar, Schwäche liegt in Titel/Thumbnail |
| `klick_ohne_halt` | Verpackung versprach mehr, als das Video hielt | Typ nicht verwerfen, Sprache nicht als Vorbild nehmen, im Output kennzeichnen |
| `schwach` | weder Klick noch Halt | als Vorbild meiden |
| `mittel` | Mittelfeld | nur Zusatz-Anker |

## Modus A — Hook generieren

**Input klären (max. 2 Rückfragen, nur wenn nicht ableitbar):**
1. Thema und Kernaussage: Welche Zuschauerin, welches Problem, welche These?
2. Optional: Titel oder Thumbnail-Idee (der Hook muss das Titelversprechen einlösen), Outline, gewünschter Typ.

**Voraussetzung:** `hooks.json` existiert. Sonst zuerst Modus B anbieten. Ist der Stand älter als 60 Tage
oder gibt es 4+ neue Videos, schlage einen frischen Studio-Export vor.

**Ablauf:**
1. **Datenbank laden:** `hooks.json` und `goldstandard-hooks.md` aus dem Datenordner.
2. **Typ-Match, 2–3 Typen ranken:** Welche `hook_type`/`first_liner_type` haben bei thematisch ähnlichen
   Videos die besten Perzentile? Doppel-Champions bevorzugen, wenn das Thema passt. Nenne bei dünner
   Datenlage (unter 15 Videos oder weniger als 3 Videos je Typ) offen, dass es eine Tendenz ist.
3. **Drei Varianten, jede mit einem anderen First-Liner-Typ** (kein Typ doppelt). Stärkster dokumentierter
   Einstieg des Kanals ist der Fall-Einstieg („Letzte Woche saß eine Kundin vor genau diesem Problem…").
   Pflichtstruktur je Hook nach dem 4C-Rahmen: Click Confirmation (echter innerer Gedanke der Zielgruppe
   aus `olga_channel.md`, sofort bestätigt) → Common Belief → Contrarian Take → Proof + Plan (3 Schritte,
   je 4–10 Wörter). Umfang: 120–160 Wörter, First-Liner ≤ 30 Sekunden, Intro ≤ 60 Sekunden. Sprach-Inventar
   (Wendungen, Verben, Anker) aus dem thematisch nächsten eigenen Video der Datenbank, plus höchstens 1
   Signaturphrase.
4. **Quality Gate vor der Ausgabe:** `hard_rules.md` durchgehen. Dazu: Spiegelung echt? Kein
   Einkommensversprechen, keine Euro-Zahl, kein Hype? Keine Fremdsprache aus Vorlagen („Let's dive in")?
   Keine Gedankenstriche, „…"-Anführungszeichen, Du-Anrede? Kein Abo-CTA direkt nach dem Hook? Zahlen,
   Tools, Ergebnisse nur, wenn Olga sie geliefert hat. Sonst `[Platzhalter in eckigen Klammern]`, nichts
   erfinden. **2-Sätze-Test:** Würde Olga diese ersten zwei Sätze so sagen?
5. **Ausgabe:**
   ```
   ## Hook-Vorschläge: [Thema]

   ### Variante 1: [Hook-Typ] · [First-Liner-Typ]
   **Vorbild:** [Titel](https://youtube.com/watch?v=ID) · Klickrate-Perzentil 0,xx · Retention-Perzentil 0,xx
   (Muster: Doppel-Champion / Halt ohne Klick / …)
   **Warum dieser Typ:** ein Satz

   **CLICK CONFIRMATION (0–10 s)** …
   **COMMON BELIEF → CONTRARIAN TAKE (10–35 s)** …
   **PROOF + PLAN (35–60 s)**
   1. … 2. … 3. …
   ```
   3 Varianten, nach erwarteter Stärke sortiert, jede mit anderem Vorbild. Trägt ein Vorbild das Muster
   `klick_ohne_halt`, kennzeichne es. Am Ende ein Satz: „Welche willst du testen?" Dann warten. Kein
   weiterer Schritt ohne Olgas Wahl.

## Persistenz — nur nach Olgas ausdrücklicher Freigabe

Ein vorgeschlagener Hook ist noch kein Goldstandard. Erst wenn Olga einen Hook freigibt:

1. **Video-Notiz** `videos/<JJJJ-MM-TT>-<slug>/hook.md` im Datenordner. Slug aus dem vollen Videotitel
   bilden. Inhalt: Datum, Titel, Hook-Typ, First-Liner-Typ, Vorbild mit Perzentilen, freigegebener
   Sprechtext, Beat-Tabelle, Open Loops, verworfene Varianten.
2. **Index-Zeile** oben unter `## Freigegebene Hooks` in `goldstandard-hooks.md` (neueste zuerst):
   `- **JJJJ-MM-TT** — [Video-Titel](videos/<JJJJ-MM-TT>-<slug>/hook.md)` und in der Folgezeile der
   Hook-Ansatz in einem Satz.

Den vollen Hook-Text **nicht** in die Index-Datei schreiben und **nicht** nummerieren. Eine frühere Index-Datei
in dieser Skill-Familie wurde 87 KB groß, ihre Nummern waren nicht mehr zu retten.
Beim Speichern nur melden: „Als Goldstandard gespeichert."

Dieselbe Freigabe gilt für Doppel-Champions aus Modus B: Kandidaten erst nach Olgas Ja eintragen, dann mit
dem tatsächlichen Hook-Text aus `hooks.json`, nicht aus dem Gedächtnis.

## Harte Regeln

1. Deutsch, Du-Anrede, ruhig, kein Hype. Tech-Begriffe werden sofort übersetzt (siehe Brand Voice).
2. Nichts erfinden: keine Zahlen, Ergebnisse, Kundengeschichten. Fehlt es, `[Platzhalter]`.
3. Sprach-Inventar nur aus Olgas eigenen Videos. Keine Wendungen aus fremden Kanälen.
4. Kein Einkommensversprechen, keine Euro-Zahl im Hook. Kein „Tech-Allrounderin".
5. Bei zwei gleich plausiblen Typen gewinnt der mit den besseren Perzentilen. Nie nach rohen Aufrufen allein.
6. Ranglisten für Klickrate und Retention bleiben getrennt.
7. Keine Datei ungefragt überschreiben. `hook-datenbank.md` ist die einzige Ausnahme, sie wird erzeugt.

## Nicht Teil dieses Skills

- Vollständige Skripte und Outlines: `olga-script` (der Hook kann dorthin als Input gehen).
- Outlier-Recherche in fremden Kanälen: `olga-outlier`.
- Absprung-Analyse auf die Sekunde: dafür gibt es in den Exporten keine Datenquelle.
- Automatischer Studio-Abruf: Die CSV muss Olga manuell exportieren.
