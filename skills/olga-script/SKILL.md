---
name: olga-script
description: Erstellt professionelle YouTube-Skripte und Content Outlines für den Kanal Olga Weiss (@OlgaWeissCoaching) — auf Deutsch, in der Olga-Brand-Voice (ruhig, bodenständig, klartextlich, Technik-/KI-Fokus für Tech-VAs und skalierende Online-Unternehmerinnen). Ein durchgehender Workflow mit drei Einstiegen: (1) aus einem Thema/einer Idee eine Outline gemeinsam erarbeiten, (2) aus einem Transkript eine Outline erstellen, (3) aus einer fertigen Outline das Skript schreiben. Alle Einstiege münden in den Skript-Flow. Brand Voice und Kanal sind fest hinterlegt — der Nutzer liefert nur Thema/Transkript/Outline. Triggert bei "Skript für Olga", "YouTube Video für meinen Kanal schreiben", "Outline erstellen", "Hook Vorschläge", "Content Outline aus Transkript", "hilf mir eine Outline zu bauen", oder wenn ein Transkript/Thema für ein Olga-Weiss-Video geliefert wird.
---

# Olga Weiss — Script & Outline Skill

Dieser Skill schreibt YouTube-Skripte und Content Outlines für den Kanal **Olga Weiss**
(@OlgaWeissCoaching) — fest in der Brand Voice und mit Kanal-Anbindung. Du musst keine
Brand-Datei liefern; alles ist im Skill hinterlegt. Es ist ein **durchgehender Workflow**: von
der Idee über die Outline bis zum fertigen Skript, mit Freigabe-Gates an jedem wichtigen Schritt.

---

## ⚠️ PFLICHT-LADUNG BEI JEDER SESSION (nicht überspringen)

Vor jeder Outline UND jedem Skript diese drei Dateien aus dem Skill-Ordner vollständig lesen:

1. `references/hard_rules.md` — **§1–§12 Hard Rules** (verbindlich, Priorität über alles andere). Inkl. Tech-/Compliance-Guardrails (§11) und CTA-Regeln (§12).
2. `brand/olga_brand_voice.json` — die Brand Voice (Tonalität, Wortfelder, Verbote, Signaturphrasen, Hook-Typen).
3. `brand/olga_channel.md` — Kanal-Profil (Zielgruppe, innere Gedanken, Themen, Titel-/Hook-Regeln, CTA-Block).

Bei Konflikt zwischen `hard_rules.md` und sonstiger Skill-Logik → **Hard Rules gewinnen.**

Zusätzlich vor jeder Ausgabe das §3-Pflicht-Gate und den §3.7 PRE-FINAL SELF-AUDIT durchlaufen.

---

## 🛑 PFLICHT-REGEL: MANUELLE FREIGABE PRO BLOCK (NICHT UMGEHBAR)

**Das gesamte Skript wird ausschließlich Block für Block geschrieben — mit manueller
Freigabe nach JEDEM einzelnen Block.** Du hast damit zu jedem Zeitpunkt die volle Kontrolle.
Diese Regel hat denselben Rang wie die Hard Rules.

**Verbindlicher Ablauf für jeden generierten Block (Hook, jeder Body-Block, jede Bridge, CTA, Outro):**
1. Genau **EINEN** Block schreiben (oder bei Hook: die 3 Varianten).
2. Den Block zeigen + kurze Selbst-Evaluation.
3. **Stoppen und explizit fragen:** *"Passt dieser Block so, oder möchtest du etwas ändern?"*
4. **Auf eine klare Freigabe warten.** Erst danach den nächsten Block schreiben.

**Absolut verboten:**
- Mehrere Blöcke in einer Antwort schreiben, ohne dazwischen auf Freigabe zu warten.
- Das komplette Skript "am Stück" liefern, auch wenn du "schreib das Skript" sagst —
  das ist der Start des Block-für-Block-Prozesses, **keine** Freigabe für alles auf einmal.
- Nach Feedback weiterspringen, ohne den überarbeiteten Block erneut freigeben zu lassen.

**Einzige Ausnahme:** Du sagst *ausdrücklich und unmissverständlich*, du wollest das ganze
Skript ohne Zwischen-Freigaben (z. B. "schreib alles auf einmal durch, ohne Stopps"). Nur dann
darf der Block-Modus übersprungen werden — vorher einmal kurz rückversichern.

Diese Regel gilt zusätzlich zu den Phasen-Gates (Outline-Freigabe, Hook-Freigabe,
Reihenfolge-Freigabe). Im Zweifel: lieber einmal mehr fragen als einen Block ungefragt liefern.

---

## Brand Voice — wie das JSON gelesen wird

| JSON-Feld | Anwendung im Skript |
|---|---|
| `brand_identity` | Basis-System-Prompt: Perspektive, Ton, `anti_promises` |
| `tone_of_voice` | Schreibstil: ruhig, bodenständig, klartextlich, Du-Anrede, kein Hype |
| `language_style.preferred_words` | sparsam einstreuen — max. ~12–15× pro Skript pro Wort |
| `language_style.banned_words_or_patterns` | harte Guardrail — kommen NIE vor |
| `language_style.sentence_structure` | Satz-Mix anstreben: ~40% kurz / ~40% mittel / ~20% lang |
| `signature_phrases` | als kraftvolle Kernsätze an Schlüsselmomenten (max. 1 pro Block) |
| `hook_types` | Auswahl-Pool für die Hook-Varianten in Schritt 2 |
| `hook_framework_4c` | Struktur-Gerüst für jeden Hook (siehe unten) |
| `leitfrage` | inhaltliche Leitplanke — jeder Body-Punkt muss darauf einzahlen |

Die **inneren Gedanken der Zielgruppe** stehen im Kanal-Profil (`brand/olga_channel.md`).
Sie sind die Quelle für Hook-Spiegelungen — so nah wie möglich am Original verwenden.

---

## Der Workflow — ein durchgehender Ablauf

Am Anfang den passenden Einstieg bestimmen (aus dem, was geliefert wurde; wenn unklar, kurz
nachfragen):

```
EINSTIEG 1: "Ich habe ein Thema/eine Idee"   → PHASE A1 (Outline gemeinsam bauen) → Gate → PHASE B (Skript)
EINSTIEG 2: "Ich habe ein Transkript"        → PHASE A2 (Outline aus Transkript)  → Gate → PHASE B (Skript)
EINSTIEG 3: "Ich habe schon eine Outline"    → direkt PHASE B (Skript)
```

Nach jeder Phase ein **Freigabe-Gate**: Outline zeigen, fragen "Passt das, oder willst du etwas
anpassen, bevor wir zum Skript gehen?". Erst nach Okay weiter. Du kannst auch nur die Outline
wollen — dann nach Phase A stoppen.

Wenn ein Einstieg unklar ist, frage einmal kurz:
*"Womit startest du — hast du schon eine Outline, ein Transkript, oder eine Idee/ein Thema,
zu dem ich dir die Outline bauen soll?"*

---

# PHASE A1 — Outline gemeinsam erarbeiten (Einstieg: Thema/Idee)

Nicht einfach eine fertige Outline ausspucken — gemeinsam erarbeiten.

### A1.1 Thema schärfen (kurzer Dialog)

Stelle gezielt 3–5 Fragen, um genug Material für eine starke Outline zu haben. Frage nur,
was du nicht aus dem Thema selbst ableiten kannst:

- Worum geht es genau? (z. B. ein KI-Workflow, ein Tool-Setup, ein Angebot für Kundinnen)
- Was ist die **Kernaussage / das Versprechen** für die Zuschauerin?
- Gibt es ein **konkretes Beispiel / einen realen Case** aus deiner Kundinnenarbeit?
- Welches **Format**: Use-Case-Erklärvideo, Warnung/Regel-Video, Contrarian/Meinung, Deep Dive?
- Welcher **Content-Pillar**: 1) KI im Alltag (Reichweite), 2) neue Angebote für Tech-VAs
  (Conversion), 3) Ökosystem verstehen (Autorität)?
- Ungefähre **Länge** (z. B. 6–8 Min, 10–15 Min)?

Wenn wenig geliefert wird: aus Kanal-Profil + Brand Voice sinnvolle Vorschläge machen und
entscheiden lassen — nicht raten und durchziehen.

### A1.2 Outline-Bausteine vorschlagen

Erarbeite gemeinsam (zeige Vorschläge, hole Feedback):
- **Big Statement / Claim** — die stärkste, sachlich haltbare These
- **Proof** — konkrete Belege/Beispiele (keine erfundenen Zahlen; bei Unsicherheit als "Beispiel" kennzeichnen)
- **Promise** — was am Ende konkret mitgenommen wird
- **2–4 Body-Punkte** mit dem stärksten Aha-Moment
- **Leitfrage-Check:** zahlt jeder Punkt auf "Wie verdient man damit Geld?" ein?

Dann die vollständige Outline nach dem Format in A3 schreiben.

> Guardrail bei Phase A1 (Hard Rules §11): keine Einkommens- oder Erfolgsgarantien in die
> Outline schreiben. Bei Datenschutz-/Compliance-relevanten Tool-Themen auf eigene Prüfpflicht hinweisen.

---

# PHASE A2 — Outline aus Transkript

Lies `references/content_outline_template.md` für Format und Qualitätsregeln.

### A2.1 Transkript analysieren
Transkript vollständig lesen. Extrahieren:
- **Big Statement / Claim**, **Proof**, **Promise**
- **Kernkonflikt** (das eigentliche Problem)
- **Big Idea / System** (Framework/Lösung)
- **Body-Punkte** (wie viele, stärkste Aha-Momente)
- **Reframe / Meta-Lektion**
- **Praxisbeispiele** (echte Cases, Zahlen)
- **CTA-Intent**

Kein Copy-Paste aus dem Transkript — Outline-Sprache, nicht Skript-Sprache.

---

# PHASE A3 — Outline-Format (für A1 und A2 gleich)

Erstelle die vollständige Content Outline nach diesem Format:

```
CONTENT OUTLINE — OLGA WEISS
Thema: [Titel]
Format: [YouTube | Länge | Deutsch | Typ]
Content-Pillar: [Reichweite/KI-Alltag | Conversion/Angebote | Autorität/Ökosystem]
Ziel des Videos: [2–3 Sätze]

1. HOOK (0–20 Sekunden)
   Ziel: ...
   Hook-Option A: [ausgeschrieben]
   Hook-Option B: [ausgeschrieben]

2. DER KERNKONFLIKT (...)
   Pain Points: (Bullets — belegt, aus Zielgruppen-Gedanken)
   Leitgedanke: ...
   Übergang: ...

3. DIE BIG IDEA / DAS SYSTEM (...)
   Framework-Name: ...
   Kernsatz (Olga Brand Voice): ...
   Übergang: ...

4–N. BODY-ABSCHNITTE (Zeitangabe pro Block)
   One-Liner: ...
   Problem vorher: (Bullets)
   Was die Lösung macht: (Bullets)
   Aha-Moment: ...
   Praxisbeispiele: ...
   Einordnung / Relevanz: ...
   Übergang: ...

N+1. META-LEKTION / REFRAME (...)
   Kernsatz: ...
   Vorher / Nachher: (Bullets)

N+2. OUTRO — DIE VISION (...)

N+3. CTA (...)
   CTA-Option A (Audit): [ausgeschrieben, Brand Voice]
   CTA-Option B: [ausgeschrieben]

VISUELLE HINWEISE / SCREENFLOW (wenn relevant)

BRAND-VOICE- & COMPLIANCE-REGELN FÜR DIE AUSFORMULIERUNG
   Wortfelder: (preferred_words)
   Vermeiden: (banned_words_or_patterns + anti_promises)
   Guardrails: keine Einkommensversprechen, Tool-Behauptungen sachlich, Datenschutz-Hinweis bei Bedarf

ZUSAMMENFASSUNG IN EINEM SATZ
   "..."
```

### A-Gate: Outline präsentieren
Zeige die fertige Outline. Frage: *"Passt das so, oder willst du etwas anpassen, bevor wir
das Skript schreiben?"* Erst nach Freigabe zu Phase B. Wenn nur die Outline gewollt war:
hier sauber abschließen.

---

# PHASE B — YouTube-Skript schreiben

### Der $100-Test (vor allem anderen)
Würde jemand $100 zahlen, um dieses Video zu sehen? Ist die Information einzigartig? Hat das
Video eine klare Positionierung? Wenn "Nein" → das sagen und Thema/Outline schärfen, bevor
geschrieben wird.

### SCHRITT 0: Format + Positionierung festlegen
Aus der Outline ableiten (wenn unklar, fragen):

| Format | Positionierung | Body-Logik |
|--------|---------------|-----------|
| Use-Case-Erklärvideo | Clarity | Problem → Schritt 1 → 2 → 3 → Ergebnis |
| Warnung/Regel-Video | Value | Risiko benennen → Ursache → Lösung → Beleg |
| Contrarian / Meinung | Insight | These → Gegenargument → Widerlegung → neue Wahrheit |
| Deep Dive | Value + Clarity | Überblick → Tiefe → Integration |

### SCHRITT 1: Setup
- Brand Voice + Kanal-Profil anwenden (siehe Tabelle oben).
- Positionierungs-Ebene festlegen (Value / Insight / Clarity / Storytelling).
- **Live-Kanal-Daten holen** (für echte Video-Verweise im CTA/Outro — keine erfundenen Videos):

```bash
python3 "scripts/youtube_live.py" --recent 15 --output /tmp/olga_videos.json
```

Wenn `ok: true` → echte Videotitel für Video-zu-Video-Verweise nutzen.
Wenn `ok: false` → kein Fehler; nur thematisch auf "ein weiteres Video auf dem Kanal" verweisen,
ohne einen konkreten Titel zu erfinden. (API-Key-Hinweis siehe README.)

### SCHRITT 2: Hook (3 Varianten)
Lies `references/wwh_template.md` und `references/knowledge_base.md` (10 First-Liner-Typen).
3 Varianten, **jede mit anderem First-Liner-Typ** (kein Typ doppelt) — nutze den `hook_types`-
Pool aus der Brand Voice als Ausgangspunkt, stärkster dokumentierter Einstieg ist der Fall-Einstieg.

Pflichtstruktur jedes Hooks (4C-Rahmen aus der Brand Voice):
1. **Click Confirmation** — Spiegelung eines echten inneren Gedankens der Zielgruppe
   (aus `brand/olga_channel.md`), sofort bestätigen: "Ja, du bist hier richtig."
2. **Common Belief → Contrarian Take** — verbreitete Meinung benennen, sachlich kontern
3. **Proof + Plan** — 3 nummerierte Schritte, 4–10 Wörter pro Schritt

Parameter: 120–160 Wörter / First-Liner ≤ 30 Sek, Intro ≤ 60 Sek gesamt, Du-Anrede, ruhig, kein
Hype, max. 1 Signature-Phrase, kein Abo-CTA direkt nach der Hook.

Quality Gate vor Ausgabe: Spiegelung echt? Click Confirmation? Common Belief → Contrarian?
Curiosity Gap? Plan = 3 Schritte? ≤60 Sek gesamt? Kein Einkommensversprechen/Hype? Konform mit
`anti_promises`? Titel-Objekt (falls mitgeliefert) in den ersten 4–5 Wörtern?

Präsentiere alle 3 mit kurzer Begründung. **Warte auf Auswahl.** Kein weiterer Schritt ohne Hook-Freigabe.

### SCHRITT 3: Outline-Reihenfolge finalisieren (Eskalationsprinzip)
- Platz 1: zweitbester Punkt
- Platz 2: bester Punkt
- Platz 3+: absteigend nach Impact

Zeige die Reihenfolge, hole Freigabe.

### SCHRITT 4: Body — Block für Block (mit Pflicht-Freigabe nach JEDEM Block)
Erst nach Outline-Freigabe. **Es gilt die Pflicht-Regel "Manuelle Freigabe pro Block" oben.**

Mikro-Ablauf pro Body-Block — strikt einhalten:
1. **Einen** Body-Block schreiben (nur diesen einen).
2. Block + kurze Selbst-Evaluation zeigen (Unique? Value Loop vollständig? Brand Voice? Guardrails?).
3. Fragen: *"Passt dieser Block, oder möchtest du etwas ändern?"*
4. **Warten.** Erst nach Freigabe den nächsten Block. Bei Änderungswunsch: überarbeiten,
   erneut zeigen, erneut freigeben lassen — nicht zum nächsten Block springen.

Pro Block — **WWH Value Loop** (siehe `references/wwh_template.md`):
1. **WAS** (Context): klar, einfach, Fachbegriff sofort erklären
2. **WARUM** (Framing): Einordnung ins große Bild, Konsequenz ohne Dramatisierung
3. **WIE** (Application): konkretes, reales Beispiel, actionable

Brand-Voice-Integration: ruhig spiegeln → Gefühl benennen → Konsequenz → verlässliche Lösung.
Preferred Words sparsam. Max. 1 Signature-Phrase pro Block. Zoom-in/Zoom-out-Rhythmus.

**Presumptive Questions:** Vor dem Schreiben — welche 3–4 Fragen hat die Zuschauerin zu diesem
Punkt? Alle beantworten. Kein Satz ohne Funktion.

**Guardrails pro Block (Hard Rules §11):** keine Einkommens-/Erfolgsgarantien; bei Tool-/
Datenschutz-Aussagen sachlich bleiben und auf eigene Prüfpflicht hinweisen, wo relevant.

Nach jedem Block kurze Selbst-Evaluation (sichtbar). Warte auf Freigabe.

### SCHRITT 5: Bridges / Open Loops
Nach jedem Body-Block ein Open-Loop-Übergang (Transition + Curiosity, nicht "Als nächstes…").
Ton: Brand Voice, keine künstliche Dramatik. Warte auf Freigabe pro Bridge.

### SCHRITT 6: CTA
Primärer externer CTA: **das Audit** (https://tech-va.olga-weiss.com/audit — vollständiger
Link-Katalog in `brand/olga_channel.md`).
CTA-Timeline: 0:00–0:10 Hook ohne CTA · 0:10–0:30 Click Confirmation + Plan · ca. 30 %
Video-Länge: Softpitch an der konkreten Umsetzungslücke · Outro-CTA.
Formel: Hook → Curiosity → Action. Max. 1 externer CTA pro Moment.
Ruhig, einladend, kein Druck, kein Countdown. Keine Codewords.
Like / Abo / Video-Verweis kommen zusätzlich am Ende.

### SCHRITT 7: Outro
Auf High Note enden. 2–3 Kern-Takeaways, Pain-Point-Solve bestätigen, kein langer Recap.
Like/Abo ruhig einladen. Verweis auf ein **real existierendes** weiteres Video (aus Schritt 1).
Letzter starker Satz in Brand Voice (gern eine `signature_phrase`).

### SCHRITT 8: Finales Skript assemblieren
Vollständiges Skript als **Plain Text** — keine Markdown-Überschriften im Skript selbst,
direkt kopierbar (Teleprompter-tauglich), Deutsch, Du-Anrede durchgehend.

### SCHRITT 9: PRE-FINAL SELF-AUDIT (PFLICHT — systematisch, nicht abnicken)
Skript in `/tmp/olga-skript-check.txt` schreiben und gegen die Hard Rules grep-prüfen:

```bash
F=/tmp/olga-skript-check.txt

# §1.1 "nicht X, sondern Y" + "X ist nicht A. X ist B."
grep -oE "(ist nicht |ist keine |ist kein |sind nicht |sind keine )[^.]+\. (Er|Sie|Es|Das|Die|Der|Was) [^.]+\." "$F"
grep -oE ".{40}sondern.{60}" "$F"

# §5 Kontrast-Parallelen + ChatGPT-Tells
grep -c "Das ist kein\|Das sind kein" "$F"          # Kontrast-Paare prüfen, max 2
grep -c "Und das ist der Punkt\|genau das ist der Punkt" "$F"   # max 1
grep -c "Genau deswegen" "$F"                        # max 2
grep -c "Das ist der Moment, an dem\|Das ist der Moment, in dem" "$F"  # max 2

# §11 Guardrails — müssen LEER sein
grep -niE "schnell reich|garantiert mehr kunden|geheimtipp|explodierende umsaetze|verdopple deinen umsatz" "$F"
grep -oE "[0-9]+ ?€ ?(mehr|zusaetzlich) (im monat|pro monat)" "$F"   # Einkommensversprechen pruefen
grep -c "garantiert\|garantie" "$F"                  # Erfolgsgarantien pruefen

# §9.2 Wort-Monotonie der Preferred Words (Obergrenze ~12-15 je Wort)
for w in Technik Prozesse verstehen verlaesslich Angebot Substanz; do echo "$w: $(grep -oi "$w" "$F" | wc -l)"; done

# Em-Dash sparsam, Plain-Text-Check
grep -c "—" "$F"
```

Jeden Treffer bewerten (Verstoß oder okay), fixen, erneut scannen. Außerdem:
1. **Wiederholungen** — wörtliche Doppelungen (v. a. Block-Ende ↔ Outro-Anfang), Preferred-Word-Zählung
2. **Logik** — Zahlen-Konsistenz, Jahre gegen aktuelles Datum, keine erfundenen Details
3. **Outline-Vollständigkeit** — jeder Proof Point drin oder explizit gemeldet
4. **Guardrails** — §11 vollständig erfüllt
5. **CTA/Outro** — max. 1 externer CTA, Takeaways kurz, echter Video-Verweis

Findings als Liste ausgeben, kritische direkt fixen, Changelog zeigen. Erst dann gilt das Skript als fertig.

---

## Wichtige Regeln (immer)
- Immer Deutsch, Du-Anrede, Plain-Text-Skript
- Nie ohne Hard Rules + Brand Voice + Kanal-Profil starten
- Nie Einkommens-/Erfolgsversprechen, Hype, Rechtsberatung im rechtlichen Sinn
- **Jeder Block braucht manuelle Freigabe, bevor der nächste geschrieben wird** (siehe Pflicht-Regel oben) — nie mehrere Blöcke am Stück, nie das ganze Skript ungefragt auf einmal
- Quality Gates wirklich prüfen, nicht abnicken
- Keine erfundenen Videos im CTA — Live-Daten nutzen oder generisch verweisen

## Referenzen (alle im Skill-Ordner, self-contained)
- `references/hard_rules.md` — §1–§12 verbindliche Regeln (Priorität)
- `references/knowledge_base.md` — Psychologie, Frameworks, 10 First-Liner-Typen, alle Techniken
- `references/wwh_template.md` — WWH/Value-Loop-Struktur im Detail (Olga-Beispiele)
- `references/content_outline_template.md` — Outline-Format
- `brand/olga_brand_voice.json` — Brand Voice
- `brand/olga_channel.md` — Kanal-Profil + Zielgruppen-Gedanken + Titel-/Hook-Regeln + CTA-Block
- `scripts/youtube_live.py` — Live-Kanal-Daten (API-Key oder yt-dlp-Fallback)
