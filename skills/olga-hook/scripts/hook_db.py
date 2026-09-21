#!/usr/bin/env python3
"""
Hook-Datenbank für Olga Weiss: verbindet Video-Transkripte mit den YouTube-Studio-Zahlen.

Drei Unterbefehle, nur Standardbibliothek, kein API-Key:

  build   Studio-CSV + Transkript-Ordner einlesen, Zahlen und Perzentile berechnen,
          Hook-Text (Intro) aus jedem Transkript ziehen, hooks.json + hook-datenbank.md schreiben.
  tag     Einordnungen (Hook-Typ, Beats, Sprach-Inventar), die Claude im Gespräch erstellt hat,
          in hooks.json übernehmen und hook-datenbank.md neu schreiben.
  render  hook-datenbank.md aus hooks.json neu schreiben.

Datenordner (bleibt bei Skill-Updates erhalten): $OLGA_HOOK_DATA oder ~/Documents/olga-hook

Bewusste Grenzen:
- Klickrate (CTR) misst Titel und Thumbnail, Retention misst das ganze Video. Keine der beiden Zahlen
  sagt, an welcher Sekunde im Hook jemand aussteigt. Die beiden Ranglisten werden nie verrechnet.
- Retention wird aus "Durchschnittliche Wiedergabedauer" / "Dauer" berechnet. Die Spalte
  "Bis zum Ende angesehen (%)" ist eine andere Kennzahl und wird nicht als Retention gelesen.
"""

import argparse
import csv
import json
import os
import re
import sys
import unicodedata
from datetime import date, datetime
from pathlib import Path

DATA_DIR = Path(os.environ.get("OLGA_HOOK_DATA") or Path.home() / "Documents" / "olga-hook")

TABELLENDATEN = "Tabellendaten.csv"
MONTHS = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "mai": 5, "jun": 6, "jul": 7, "aug": 8,
          "sep": 9, "oct": 10, "okt": 10, "nov": 11, "dec": 12, "dez": 12}
MOJIBAKE_RE = re.compile(r"Ã[¤¶¼„–ŸŒŠ¦]|â€")
TRANSCRIPT_SUFFIXES = {".txt", ".md", ".srt", ".vtt"}

# Schwellen — Vorschlag, per Argument änderbar
HOCH, NIEDRIG = 0.70, 0.40          # Perzentil-Grenzen (0 = schlechtestes, 1 = bestes Video des Kanals)
KORRIDOR_CTR, KORRIDOR_RET = 4.0, 25.0   # Olgas eigene Zielkorridore (brand/olga_channel.md)
MIN_VIDEOS_BELASTBAR = 15

FIRST_LINER_TYPES = ["Question Hook", "Shocking Statement", "Storytelling Hook", "Preview Hook",
                     "Personal Connection", "Statistical Fact", "Challenge Hook", "Quotation Hook",
                     "Metaphor Hook", "Proof Hook"]
OLGA_HOOK_TYPES = ["Fall-Einstieg", "Persönliche Geschichte", "Direkter Schmerzpunkt",
                   "Sonntag-/Alltags-Hook", "Tool-Insight", "Klare Frage", "Empathie-Anker"]
BEATS = ["click_confirmation", "common_belief", "contrarian_take", "proof_plan"]


# ---------------------------------------------------------------- Zahlen einlesen

def fix_mojibake(text):
    if not text or not MOJIBAKE_RE.search(text):
        return text
    try:
        return text.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text


def to_seconds(s):
    s = (s or "").strip()
    if not s:
        return None
    try:
        parts = [int(p) for p in s.split(":")]
    except ValueError:
        return None
    sec = 0
    for p in parts:
        sec = sec * 60 + p
    return sec


def to_float(s):
    s = (s or "").strip().replace("%", "").replace(",", ".")
    try:
        return float(s) if s else None
    except ValueError:
        return None


def to_int(s):
    s = (s or "").strip().replace(" ", "")
    if re.match(r"^\d{1,3}(\.\d{3})+$", s):
        s = s.replace(".", "")
    try:
        return int(float(s)) if s else None
    except ValueError:
        return None


def to_date(s):
    s = (s or "").strip()
    m = re.match(r"([A-Za-zäöü]{3})\w*\.?\s+(\d{1,2}),\s*(\d{4})", s)
    if m and m.group(1).lower() in MONTHS:
        return date(int(m.group(3)), MONTHS[m.group(1).lower()], int(m.group(2))).isoformat()
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return m.group(0)
    m = re.match(r"(\d{1,2})\.(\d{1,2})\.(\d{4})", s)
    if m:
        return date(int(m.group(3)), int(m.group(2)), int(m.group(1))).isoformat()
    return None


def load_studio(path):
    """Tabellendaten.csv -> Liste von Video-Datensätzen (ohne Gesamt-Zeile)."""
    records = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        cols = set(reader.fieldnames or [])
        for need in ("Videos", "Videotitel", "Dauer", "Durchschnittliche Wiedergabedauer"):
            if need not in cols:
                sys.exit(f"Spalte '{need}' fehlt in {path.name}. Vorhanden: {sorted(cols)}")

        def pick(row, *names):
            for n in names:
                if n in cols:
                    return row.get(n)
            return None

        for row in reader:
            vid = (row.get("Videos") or "").strip()
            if not vid or vid == "Gesamt":
                continue
            duration = to_int(row.get("Dauer"))
            avg = to_seconds(row.get("Durchschnittliche Wiedergabedauer"))
            explicit = to_float(pick(row, "Durchschnittliche Wiedergabedauer in Prozent (%)",
                                     "Durchschnittlich angesehen (%)"))
            if explicit is not None:
                retention, retention_source = explicit, "studio_spalte"
            elif duration and avg is not None:
                retention, retention_source = round(100 * avg / duration, 2), "berechnet"
            else:
                retention, retention_source = None, None
            records.append({
                "video_id": vid,
                "title": fix_mojibake((row.get("Videotitel") or "").strip()),
                "publish_date": to_date(row.get("Veröffentlichungszeitpunkt des Videos")),
                "duration_sec": duration,
                "avg_view_duration_sec": avg,
                "retention_pct": retention,
                "retention_source": retention_source,
                "views": to_int(row.get("Aufrufe")),
                "impressions": to_int(pick(row, "Impressionen", "Thumbnail-Impressionen")),
                "ctr_pct": to_float(pick(row, "Klickrate der Impressionen (%)", "Thumbnail-Klickrate (%)")),
            })
    return records


def filter_records(records, min_duration, min_impressions, min_views, min_age_days, today):
    kept, excluded = [], []
    for r in records:
        why, codes = [], []

        def no(code, text):
            codes.append(code)
            why.append(text)

        if r["duration_sec"] is None or r["duration_sec"] < min_duration:
            no("kurz", f"Dauer {r['duration_sec']} s < {min_duration} s (Short?)")
        if r["publish_date"] is None:
            no("datum", "Veröffentlichungsdatum fehlt")
        elif (today - date.fromisoformat(r["publish_date"])).days < min_age_days:
            no("jung", f"jünger als {min_age_days} Tage")
        if r["impressions"] is None or r["impressions"] < min_impressions:
            no("impressionen", f"Impressionen {r['impressions']} < {min_impressions}")
        if r["views"] is None or r["views"] < min_views:
            no("aufrufe", f"Aufrufe {r['views']} < {min_views}")
        if r["ctr_pct"] is None:
            no("ctr", "Klickrate fehlt")
        if r["retention_pct"] is None:
            no("retention", "Retention nicht berechenbar")
        if why:
            excluded.append({"video_id": r["video_id"], "title": r["title"], "reason": "; ".join(why),
                             "codes": codes})
        else:
            kept.append(r)
    return kept, excluded


def add_percentile(records, key):
    ordered = sorted(records, key=lambda r: r[key])
    n = len(ordered)
    for r in records:
        idx = [i for i, o in enumerate(ordered) if o[key] == r[key]]
        r[f"{key.replace('_pct', '')}_percentile"] = round((sum(idx) / len(idx) + 1) / n, 3)


def classify(r):
    c, t = r["ctr_percentile"], r["retention_percentile"]
    if c >= HOCH and t >= HOCH:
        return "doppel_champion"
    if c >= HOCH and t <= NIEDRIG:
        return "klick_ohne_halt"      # Verpackung versprach mehr, als Video/Hook hielt
    if t >= HOCH and c <= NIEDRIG:
        return "halt_ohne_klick"      # Hook/Video stark, aber zu wenig gesehen
    if c <= NIEDRIG and t <= NIEDRIG:
        return "schwach"
    return "mittel"


# ---------------------------------------------------------------- Transkripte

TS_LINE = re.compile(r"^\s*[\[(]?(?:(\d{1,2}):)?(\d{1,2}):(\d{2})(?:[.,]\d+)?[\])]?\s+(\S.*)$")
SRT_TIME = re.compile(r"^(\d{1,2}):(\d{2}):(\d{2})[.,]\d+\s*-->")
VTT_TIME = re.compile(r"^(?:(\d{1,2}):)?(\d{2}):(\d{2})[.,]\d+\s*-->")


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"['’`´]", "", s)
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def read_transcripts(folder):
    items = []
    for p in sorted(folder.rglob("*")):
        if p.is_file() and p.suffix.lower() in TRANSCRIPT_SUFFIXES and not p.name.startswith("."):
            items.append({"file": p, "text": p.read_text(encoding="utf-8-sig", errors="replace")})
    return items


def match_transcripts(records, transcripts):
    """Zuordnung nur bei eindeutigem Treffer. Rückgabe: (video_id -> transcript, mehrdeutig)."""
    by_video, ambiguous = {}, []
    for t in transcripts:
        head = t["text"][:600]
        name_n, head_n = norm(t["file"].stem), norm(head)
        hits = [r for r in records if r["video_id"] in t["file"].name or r["video_id"] in head]
        if not hits:
            hits = [r for r in records if norm(r["title"]) and len(norm(r["title"])) >= 8
                    and (norm(r["title"]) in name_n or name_n in norm(r["title"]) and len(name_n) >= 8
                         or norm(r["title"]) in head_n)]
        if len(hits) == 1:
            vid = hits[0]["video_id"]
            if vid in by_video:
                ambiguous.append((t["file"].name, f"zweite Datei für {vid} (erste: {by_video[vid]['file'].name})"))
            else:
                by_video[vid] = t
        elif len(hits) > 1:
            ambiguous.append((t["file"].name, "passt auf " + ", ".join(h["video_id"] for h in hits)))
    return by_video, ambiguous


def strip_frontmatter(text):
    if text.startswith("---"):
        m = re.match(r"^---\n.*?\n---\n", text, re.S)
        if m:
            return text[m.end():]
    return text


def extract_hook(text, seconds, words, title):
    """Wörtlicher Intro-Text. Mit Zeitstempeln bis `seconds`, sonst die ersten `words` Wörter."""
    text = strip_frontmatter(text).replace("\r\n", "\n")
    lines = text.split("\n")
    if lines and (lines[0].lstrip("# ").strip() == title or lines[0].startswith("# ")):
        lines = lines[1:]

    cues, i = [], 0
    while i < len(lines):                                  # SRT/VTT-Blöcke
        m = SRT_TIME.match(lines[i].strip()) or VTT_TIME.match(lines[i].strip())
        if m:
            g = [x for x in m.groups() if x is not None]
            h, mi, s = (int(g[0]), int(g[1]), int(g[2])) if len(g) == 3 else (0, int(g[0]), int(g[1]))
            j, buf = i + 1, []
            while j < len(lines) and lines[j].strip():
                buf.append(lines[j].strip())
                j += 1
            cues.append((h * 3600 + mi * 60 + s, " ".join(buf)))
            i = j
        i += 1
    if not cues:                                           # "[00:12] Text" / "0:12 Text"
        for ln in lines:
            m = TS_LINE.match(ln)
            if m:
                h, mi, s, rest = m.groups()
                cues.append((int(h or 0) * 3600 + int(mi) * 60 + int(s), rest.strip()))
    if len(cues) >= 5:
        picked = [t for sec, t in cues if sec < seconds]
        hook = " ".join(picked).strip()
        return hook, "zeitstempel", len(hook.split())

    plain = " ".join(ln.strip() for ln in lines if ln.strip())
    tokens = plain.split()
    return " ".join(tokens[:words]), "woerter", min(len(tokens), words)


# ---------------------------------------------------------------- Schreiben

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def save_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


PATTERN_TEXT = {
    "doppel_champion": "Doppel-Champion — Verpackung und Halt tragen (Goldstandard-Kandidat)",
    "klick_ohne_halt": "Klick ohne Halt — Verpackung versprach mehr, als Hook/Video hielt",
    "halt_ohne_klick": "Halt ohne Klick — Hook/Video stark, zu wenig gesehen (Schwäche liegt in Titel/Thumbnail)",
    "schwach": "Schwach — weder Klick noch Halt, als Vorbild meiden",
    "mittel": "Mittelfeld",
}
ORDER = ["doppel_champion", "halt_ohne_klick", "klick_ohne_halt", "mittel", "schwach"]


def render_md(db):
    vids = sorted(db["videos"].values(),
                  key=lambda v: (ORDER.index(v["pattern"]), -(v["ctr_percentile"] + v["retention_percentile"])))
    n_kept = db["counts"]["kept"]
    L = ["---", "cluster: olga-weiss", "generated: true", "---", "",
         "# Olga Weiss — Hook-Datenbank", "",
         "> Wird bei jedem `build`/`tag`/`render` aus `hooks.json` neu geschrieben. Nicht von Hand ändern, "
         "handgepflegt ist nur `goldstandard-hooks.md`.", "",
         f"Stand Studio-Export: **{db['studio_export']}** · erzeugt {db['generated_at']}", "",
         f"- Videos in der Tabelle: {db['counts']['csv_rows']} · in der Auswertung: {n_kept} · "
         f"ausgeschlossen: {db['counts']['excluded']} · mit Transkript in dieser Datenbank: {len(vids)}",
         f"- Ohne Transkript trotz Zahlen: {len(db['unmatched_csv'])} · Transkripte ohne eindeutige Zuordnung: "
         f"{len(db['unmatched_transcripts'])}"]
    if n_kept < MIN_VIDEOS_BELASTBAR:
        L += ["", f"> **Achtung:** Nur {n_kept} Videos in der Auswertung (unter {MIN_VIDEOS_BELASTBAR}). "
                  "Die Ranglisten sind Tendenzen, keine Belege."]
    L += ["", "**Wie lesen:** Klickrate misst Titel und Thumbnail. Retention (Ø Wiedergabedauer / Videolänge) "
              "misst das ganze Video, nicht den Hook. Beide Ranglisten stehen getrennt und werden nicht "
              "verrechnet. Perzentil 1,0 = bestes Video des Kanals. "
              f"Olgas Korridor: CTR > {KORRIDOR_CTR:g} %, Retention > {KORRIDOR_RET:g} %.", "",
         "## Übersicht", "",
         "| Video | Datum | CTR % | CTR-Perz. | Retention % | Ret.-Perz. | Muster | Typ getaggt |",
         "|---|---|---:|---:|---:|---:|---|---|"]
    for v in vids:
        tagged = v.get("tags", {}).get("hook_type") or "—"
        L.append(f"| {v['title']} | {v['publish_date']} | {v['ctr_pct']:g} | {v['ctr_percentile']} | "
                 f"{v['retention_pct']:g} | {v['retention_percentile']} | {v['pattern']} | {tagged} |")
    for v in vids:
        t = v.get("tags") or {}
        L += ["", f"## {v['title']}", "",
              f"- Video: https://www.youtube.com/watch?v={v['video_id']} · {v['publish_date']} · "
              f"{v['duration_sec']} s",
              f"- CTR {v['ctr_pct']:g} % (Perzentil {v['ctr_percentile']}"
              f"{', über Korridor' if v['ctr_pct'] > KORRIDOR_CTR else ', unter Korridor'}) · "
              f"Retention {v['retention_pct']:g} % (Perzentil {v['retention_percentile']}"
              f"{', über Korridor' if v['retention_pct'] > KORRIDOR_RET else ', unter Korridor'}) · "
              f"{v['impressions']} Impressionen · {v['views']} Aufrufe",
              f"- Muster: **{PATTERN_TEXT[v['pattern']]}**",
              f"- Hook-Text ({v['hook_words']} Wörter, geschnitten nach {v['cut_method']}, Quelle "
              f"`{v['transcript_file']}`):", "", "> " + v["hook_text"].replace("\n", "\n> "), ""]
        if t:
            L += [f"- Hook-Typ (Olga): {t.get('hook_type', '—')} · First-Liner-Typ: {t.get('first_liner_type', '—')}",
                  f"- Beats vorhanden: {', '.join(t.get('beats', [])) or '—'}",
                  f"- Spannung: {t.get('tension_pattern', '—')}"]
            lang = t.get("language") or {}
            for key, label in (("signature_phrases", "Wendungen"), ("verbs", "Verben"), ("anchors", "Anker/Zahlen")):
                if lang.get(key):
                    L.append(f"- {label}: " + " · ".join(f"„{x}“" for x in lang[key]))
            if t.get("note"):
                L.append(f"- Anmerkung: {t['note']}")
        else:
            L.append("- _Noch nicht eingeordnet (Hook-Typ, Beats, Sprach-Inventar) — `tag` fehlt._")
    if db["excluded"]:
        L += ["", "## Ausgeschlossene Videos", ""] + [f"- {e['title']} (`{e['video_id']}`): {e['reason']}"
                                                       for e in db["excluded"]]
    return "\n".join(L) + "\n"


def write_outputs(out, db):
    save_json(out / "hooks.json", db)
    (out / "hook-datenbank.md").write_text(render_md(db), encoding="utf-8")
    gs = out / "goldstandard-hooks.md"
    if not gs.exists():
        gs.write_text("---\ncluster: olga-weiss\n---\n\n# Olga Weiss — Goldstandard-Hooks\n\n"
                      "Nur von Olga freigegebene Hooks. Datum + Titel identifizieren den Eintrag, keine "
                      "Nummern. Den vollen Hook-Text nicht hier ablegen, sondern in "
                      "`videos/<datum>-<slug>/hook.md`.\n\n## Freigegebene Hooks\n\n", encoding="utf-8")


# ---------------------------------------------------------------- Befehle

def cmd_build(a):
    studio = Path(a.studio).expanduser()
    csv_path = studio / TABELLENDATEN if studio.is_dir() else studio
    if not csv_path.exists():
        sys.exit(f"Studio-Datei nicht gefunden: {csv_path}")
    tdir = Path(a.transcripts).expanduser()
    if not tdir.is_dir():
        sys.exit(f"Transkript-Ordner nicht gefunden: {tdir}")
    out = Path(a.out).expanduser()

    records = load_studio(csv_path)
    kept, excluded = filter_records(records, a.min_duration, a.min_impressions, a.min_views,
                                    a.min_age_days, date.today())
    if not kept:
        sys.exit("Kein Video übrig nach den Filtern. Ausschlüsse:\n" +
                 "\n".join(f"  {e['title']}: {e['reason']}" for e in excluded[:20]))
    add_percentile(kept, "ctr_pct")
    add_percentile(kept, "retention_pct")
    for r in kept:
        r["pattern"] = classify(r)

    transcripts = read_transcripts(tdir)
    by_video, ambiguous = match_transcripts(records, transcripts)   # gegen ALLE Zeilen, damit Ausgeschlossene nicht als "ohne Zeile" gelten
    matched_files = {t["file"].name for t in by_video.values()}

    previous = load_json(out / "hooks.json") or {"videos": {}}
    videos, unmatched_csv = {}, []
    for r in kept:
        t = by_video.get(r["video_id"])
        if not t:
            unmatched_csv.append({"video_id": r["video_id"], "title": r["title"]})
            continue
        hook, method, n = extract_hook(t["text"], a.hook_seconds, a.hook_words, r["title"])
        if not hook:
            unmatched_csv.append({"video_id": r["video_id"], "title": r["title"], "reason": "Hook-Text leer"})
            continue
        entry = dict(r, hook_text=hook, cut_method=method, hook_words=n, transcript_file=t["file"].name)
        old = previous["videos"].get(r["video_id"], {})
        if old.get("tags") and old.get("hook_text") == hook:      # Einordnung nur behalten, wenn der Hook gleich blieb
            entry["tags"] = old["tags"]
        videos[r["video_id"]] = entry

    excluded_ids = {e["video_id"] for e in excluded}
    unmatched_transcripts = [{"file": t["file"].name,
                              "reason": next((why for f, why in ambiguous if f == t["file"].name),
                                             "Video-ID/Titel nicht in der Studio-Tabelle")}
                             for t in transcripts if t["file"].name not in matched_files]
    only_excluded = [str(t["file"].name) for v, t in by_video.items() if v in excluded_ids]
    db = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "studio_export": csv_path.parent.name + "/" + csv_path.name,
        "params": {k: getattr(a, k) for k in ("min_duration", "min_impressions", "min_views",
                                              "min_age_days", "hook_seconds", "hook_words")},
        "counts": {"csv_rows": len(records), "kept": len(kept), "excluded": len(excluded),
                   "transcripts": len(transcripts), "matched": len(by_video), "in_database": len(videos)},
        "videos": videos, "excluded": excluded, "unmatched_csv": unmatched_csv,
        "unmatched_transcripts": unmatched_transcripts, "transcripts_of_excluded_videos": only_excluded,
    }
    if sum(1 for e in excluded) + len(kept) != len(records):
        sys.exit("Interner Fehler: Zeilenzahl passt nicht (kept + excluded != CSV-Zeilen).")
    write_outputs(out, db)

    c = db["counts"]
    print(f"Studio-Tabelle: {c['csv_rows']} Videos · ausgeschlossen: {c['excluded']} · in Auswertung: {c['kept']}")
    print(f"Transkripte: {c['transcripts']} · eindeutig zugeordnet: {c['matched']} · in der Datenbank: {c['in_database']}")
    if excluded:
        from collections import Counter
        codes = Counter(c for e in excluded for c in e["codes"])
        print("  Ausschlussgründe (ein Video kann mehrere haben): " +
              ", ".join(f"{k} {v}" for k, v in codes.most_common()) + "  — Liste in hook-datenbank.md")
    for u in unmatched_csv:
        print(f"  Zahlen ohne Transkript: {u['title'][:60]} ({u['video_id']})")
    for u in unmatched_transcripts:
        print(f"  Transkript ohne Zuordnung: {u['file']} — {u['reason']}")
    for f in only_excluded:
        print(f"  Transkript gehört zu einem ausgeschlossenen Video: {f}")
    if c["kept"] < MIN_VIDEOS_BELASTBAR:
        print(f"ACHTUNG: nur {c['kept']} Videos in der Auswertung (< {MIN_VIDEOS_BELASTBAR}) — Tendenzen, keine Belege.")
    dc = sum(1 for v in videos.values() if v["pattern"] == "doppel_champion")
    print(f"Doppel-Champions mit Transkript: {dc}")
    print(f"→ {out / 'hooks.json'}\n→ {out / 'hook-datenbank.md'}")


def cmd_tag(a):
    out = Path(a.out).expanduser()
    db = load_json(out / "hooks.json")
    if not db:
        sys.exit(f"{out / 'hooks.json'} fehlt — erst `build` ausführen.")
    tags = json.loads(Path(a.file).expanduser().read_text(encoding="utf-8"))
    n = 0
    for vid, t in tags.items():
        if vid not in db["videos"]:
            print(f"  übersprungen (nicht in der Datenbank): {vid}")
            continue
        if t.get("first_liner_type") and t["first_liner_type"] not in FIRST_LINER_TYPES:
            print(f"  {vid}: first_liner_type '{t['first_liner_type']}' ist keiner der 10 Typen")
        bad = [b for b in t.get("beats", []) if b not in BEATS]
        if bad:
            print(f"  {vid}: unbekannte Beats {bad} (erlaubt: {BEATS})")
        if t.get("hook_type") and t["hook_type"] not in OLGA_HOOK_TYPES:
            print(f"  {vid}: hook_type '{t['hook_type']}' steht nicht in Olgas 7 Typen (als Sonderfall gespeichert)")
        db["videos"][vid]["tags"] = t
        n += 1
    write_outputs(out, db)
    print(f"{n} Videos eingeordnet, {len(db['videos']) - sum(1 for v in db['videos'].values() if v.get('tags'))} offen.")


def cmd_render(a):
    out = Path(a.out).expanduser()
    db = load_json(out / "hooks.json")
    if not db:
        sys.exit(f"{out / 'hooks.json'} fehlt — erst `build` ausführen.")
    write_outputs(out, db)
    print(f"→ {out / 'hook-datenbank.md'}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", default=str(DATA_DIR), help=f"Datenordner (Default {DATA_DIR})")
    sub = p.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="Zahlen + Transkripte zusammenführen")
    b.add_argument("--studio", required=True, help="Tabellendaten.csv oder der Ordner, der sie enthält")
    b.add_argument("--transcripts", required=True, help="Ordner mit den Transkripten (.txt .md .srt .vtt)")
    b.add_argument("--min-duration", type=int, default=180, help="Sekunden; darunter = Short, ausgeschlossen")
    b.add_argument("--min-impressions", type=int, default=1000)
    b.add_argument("--min-views", type=int, default=100)
    b.add_argument("--min-age-days", type=int, default=28)
    b.add_argument("--hook-seconds", type=int, default=60, help="Intro-Länge (Olga: Intro <= 60 s)")
    b.add_argument("--hook-words", type=int, default=160, help="Wörter, falls Transkript keine Zeitstempel hat")
    b.set_defaults(fn=cmd_build)
    t = sub.add_parser("tag", help="Einordnungen aus einer JSON-Datei übernehmen")
    t.add_argument("--file", required=True)
    t.set_defaults(fn=cmd_tag)
    r = sub.add_parser("render", help="hook-datenbank.md neu schreiben")
    r.set_defaults(fn=cmd_render)
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
