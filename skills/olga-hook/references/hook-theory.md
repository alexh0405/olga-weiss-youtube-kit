# Hook-Theorie für Olga Weiss

Grundlage: `olga-script/references/knowledge_base.md` (10 First-Liner-Typen), `brand/olga_brand_voice.json`
(7 Kanal-Typen, 4C-Rahmen), `brand/olga_channel.md` (Zielgruppe, Korridore). Diese Datei legt fest, wie
Hooks **eingeordnet** werden, damit Datenbank und Generator dieselbe Sprache sprechen.

## Zwei Typ-Achsen je Hook

Jeder Hook bekommt genau **einen** Wert auf jeder Achse.

**Achse 1 — `hook_type` (Olgas 7 Kanal-Typen, wie sie einsteigt):**

| Typ | Erkennungsmerkmal |
|---|---|
| Fall-Einstieg | Konkrete Kundin oder Szene („Letzte Woche saß eine Kundin vor genau diesem Problem…") |
| Persönliche Geschichte | Olga erzählt aus dem eigenen Erleben |
| Direkter Schmerzpunkt | Benennt das Problem der Zuschauerin direkt („Du sitzt seit 3 Stunden an…") |
| Sonntag-/Alltags-Hook | Beiläufiger, augenzwinkernder Einstieg mit Alltagsbezug |
| Tool-Insight | Verspricht einen konkreten Kniff oder versteckten Punkt in einem Tool |
| Klare Frage | Eine direkte Frage an die Zuschauerin |
| Empathie-Anker | Zuerst Verständnis („Kenn ich. Ich war lange genau da.") |

Passt keiner: `hook_type` = `Sonstiger` und in `note` beschreiben, was der Hook tut.

**Achse 2 — `first_liner_type` (die 10 First-Liner-Typen, was der erste Satz tut):**
Question Hook · Shocking Statement · Storytelling Hook · Preview Hook · Personal Connection ·
Statistical Fact · Challenge Hook · Quotation Hook · Metaphor Hook · Proof Hook.

Beide Achsen sind nötig: Ein „Fall-Einstieg" kann als Storytelling Hook oder als Proof Hook beginnen.
Der Generator schreibt drei Varianten mit drei verschiedenen `first_liner_type`.

## 4C-Rahmen (Beats)

Guter Standard, gegen den geprüft wird. Nicht jeder Hook hat alle vier.

| Beat (Wert in `beats`) | Aufgabe |
|---|---|
| `click_confirmation` | Löst das Titel-/Thumbnail-Versprechen ein und bestätigt einen echten inneren Gedanken der Zielgruppe. Sinngemäß: „Ja, du bist hier richtig." |
| `common_belief` | Benennt die verbreitete Meinung |
| `contrarian_take` | Kontert sachlich mit der eigenen These |
| `proof_plan` | Beweis plus Plan in 3 nummerierten Schritten, je 4–10 Wörter |

Zeiten: First-Liner ≤ 30 Sekunden, Intro ≤ 60 Sekunden gesamt, kein Intro-Bumper. Abo-CTA erst später
im Video. 0:00–0:10 Hook ohne CTA, 0:10–0:30 Click Confirmation und Plan.

Beim Einordnen zählt nur, was im Text steht. Fehlt ein Baustein, bleibt er weg.

## Spannungsmuster (`tension_pattern`, eines pro Hook)

- Schmerz: Problem der Zuschauerin wird explizit
- False Belief: verbreitete Annahme wird angegriffen
- Contrarian Take: These widerspricht dem Konsens
- Verpasste Chance: Lücke, die jetzt offen ist
- Insider-Wissen: „So läuft das unter der Haube wirklich"
- Urgency: echte, belegbare Verknappung (kein FOMO ohne Beleg)
- Warnung: vor Fehlkonfiguration, Kosten, Sackgassen
- Ergebnis als Beweis: eigenes laufendes System oder echte Kundinnenarbeit

## Anti-Patterns (sofort verwerfen)

Aus `olga_channel.md` und `olga-script/references/hard_rules.md`, dort maßgeblich:

- „In diesem Video erfährst du…", „Lass uns eintauchen…", „Bevor wir starten…"
- Hype-Sprache („Game-Changer", „nächstes Level")
- Einkommensversprechen, Euro-Zahl im Hook
- „Nicht weil X, sondern weil Y" und jede Variante davon
- Leere Adjektiv-Ketten, klassische Fazit-Abschlüsse
- Gedankenstriche, englische Anführungszeichen statt „…"
- Denglisch ohne Erklärung, Einstieg mit Selbstvorstellung als Beat

## CTR/Retention-Diagnose

Zwei getrennte Leistungssignale je Video, nicht verrechnet:

- **Klickrate-Perzentil:** Hat Titel/Thumbnail zum Klick bewegt?
- **Retention-Perzentil:** Hat das Video gehalten, was der Klick versprach? (Ø Wiedergabedauer / Videolänge)

Perzentil 1,0 = bestes Video von Olgas Kanal. Zusätzlich Olgas Zielkorridore: CTR > 4 %, Retention > 25 %.
Perzentile zeigen den Rang im eigenen Kanal, der Korridor die absolute Lage. Beide anzeigen.

| Muster | Bedeutung | Konsequenz |
|---|---|---|
| Hohe CTR + hohe Retention (Doppel-Champion) | Verpackung und Halt liefern | Typ und Beat-Struktur als Vorbild bevorzugen |
| Niedrige CTR + hohe Retention (Halt ohne Klick) | Hook/Video stark, zu wenig gesehen | Hook als Vorbild nutzen, Schwäche liegt in Titel/Thumbnail |
| Hohe CTR + niedrige Retention (Klick ohne Halt) | Verpackung versprach mehr, als das Video hielt | Typ nicht verwerfen, Sprache nicht als Vorbild nehmen, kennzeichnen |
| Niedrige CTR + niedrige Retention (schwach) | Nichts trug | als Vorbild meiden |

**Grenzen:** Retention gilt fürs ganze Video, nicht für die ersten Sekunden. Es gibt keine Daten, an welcher
Sekunde jemand aus dem Hook aussteigt. Die Klickrate misst vor allem Titel und Thumbnail. Doppel-Champions
sind deshalb das stärkste Signal, alles andere ist schwächer. Bei weniger als 15 Videos sind die
Ranglisten Tendenzen.

## Hook-Typ-Auswahl (Heuristik, vor den Daten)

- Neues Tool / Update vorstellen: Tool-Insight oder Fall-Einstieg
- Ein Problem, das die Zielgruppe schon spürt: Direkter Schmerzpunkt oder Empathie-Anker
- Ein Workflow, der zur verkaufbaren Leistung wird (Kern-USP): Fall-Einstieg
- Gegen eine verbreitete Meinung: Klare Frage oder Shocking Statement
- Ist die Datenlage besser als diese Heuristik, gewinnen die Daten.
