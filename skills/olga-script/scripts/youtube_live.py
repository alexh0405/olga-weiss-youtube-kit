#!/usr/bin/env python3
"""
Olga Weiss — Live-Kanal-Daten.

Holt echte Videos des Kanals @OlgaWeissCoaching, damit der Skill bei CTA-Verweisen
auf real existierende Videos verweisen kann (statt sie zu erfinden).

Zwei Pfade, in dieser Reihenfolge:
  1. YouTube Data API v3  (wenn YOUTUBE_API_KEY gesetzt ist) — schnell, zuverlässig
  2. yt-dlp Fallback      (wenn kein Key, aber yt-dlp installiert ist) — kein Key nötig

Wenn beides fehlschlägt, wird sauber `{"ok": false, "reason": ...}` ausgegeben,
KEIN Crash — der Skill arbeitet dann nur mit dem statischen Kanal-Profil weiter.

Nutzung:
    python3 youtube_live.py --recent 15
    python3 youtube_live.py --recent 15 --output /tmp/olga_videos.json
    python3 youtube_live.py --search "Claude"           # nur Videos, deren Titel den Begriff enthält

API-Key (empfohlen, einmal setzen):
    export YOUTUBE_API_KEY="dein_key"
    (oder dauerhaft in ~/.zshrc / ~/.bashrc eintragen)
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request

CHANNEL_ID = "UC3BPfoLoiJaVshDvSUH7p9Q"
CHANNEL_URL = f"https://www.youtube.com/channel/{CHANNEL_ID}"


def _err(reason, hint=None):
    out = {"ok": False, "channel_id": CHANNEL_ID, "reason": reason}
    if hint:
        out["hint"] = hint
    return out


def fetch_via_api(api_key, count):
    """YouTube Data API v3: Uploads-Playlist des Kanals lesen."""
    # 1) Uploads-Playlist-ID des Kanals holen
    ch_url = "https://www.googleapis.com/youtube/v3/channels?" + urllib.parse.urlencode(
        {"part": "contentDetails,snippet", "id": CHANNEL_ID, "key": api_key}
    )
    with urllib.request.urlopen(ch_url, timeout=20) as r:
        ch = json.load(r)
    items = ch.get("items") or []
    if not items:
        return _err("api_no_channel", "Channel-ID nicht gefunden oder Key ungültig.")
    uploads = items[0]["contentDetails"]["relatedPlaylists"]["uploads"]
    channel_title = items[0]["snippet"]["title"]

    # 2) Letzte Videos aus der Uploads-Playlist
    pl_url = "https://www.googleapis.com/youtube/v3/playlistItems?" + urllib.parse.urlencode(
        {"part": "snippet", "playlistId": uploads, "maxResults": min(count, 50), "key": api_key}
    )
    with urllib.request.urlopen(pl_url, timeout=20) as r:
        pl = json.load(r)

    videos = []
    for it in pl.get("items", []):
        sn = it["snippet"]
        vid = sn.get("resourceId", {}).get("videoId")
        if not vid:
            continue
        videos.append({
            "title": sn.get("title", ""),
            "video_id": vid,
            "url": f"https://www.youtube.com/watch?v={vid}",
            "published_at": sn.get("publishedAt", ""),
        })
    return {"ok": True, "source": "api", "channel": channel_title,
            "channel_id": CHANNEL_ID, "videos": videos}


def fetch_via_ytdlp(count):
    """yt-dlp Fallback: kein API-Key nötig."""
    binary = shutil.which("yt-dlp")
    if not binary:
        return _err("ytdlp_missing",
                    "Weder YOUTUBE_API_KEY gesetzt noch yt-dlp installiert. "
                    "Setze einen API-Key (export YOUTUBE_API_KEY=...) oder installiere yt-dlp (pip install yt-dlp).")
    cmd = [binary, "--flat-playlist", "--playlist-end", str(count), "-J",
           f"{CHANNEL_URL}/videos"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    except subprocess.TimeoutExpired:
        return _err("ytdlp_timeout", "yt-dlp hat zu lange gebraucht. Erneut versuchen oder API-Key setzen.")
    if proc.returncode != 0 or not proc.stdout.strip():
        return _err("ytdlp_failed", (proc.stderr or "").strip()[:300])
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return _err("ytdlp_parse_failed")
    videos = []
    for e in (data.get("entries") or [])[:count]:
        vid = e.get("id")
        if not vid:
            continue
        videos.append({
            "title": e.get("title", ""),
            "video_id": vid,
            "url": f"https://www.youtube.com/watch?v={vid}",
            "published_at": "",
        })
    return {"ok": True, "source": "yt-dlp",
            "channel": data.get("channel") or data.get("title") or "Olga Weiss",
            "channel_id": CHANNEL_ID, "videos": videos}


def main():
    p = argparse.ArgumentParser(description="Olga Weiss — Live-Kanal-Daten")
    p.add_argument("--recent", type=int, default=15, help="Anzahl der letzten Videos")
    p.add_argument("--search", default=None, help="Nur Videos, deren Titel diesen Begriff enthält")
    p.add_argument("--output", default=None, help="Optional: Ergebnis in Datei schreiben")
    p.add_argument("--api-key", default=None, help="API-Key (sonst aus YOUTUBE_API_KEY)")
    args = p.parse_args()

    api_key = args.api_key or os.environ.get("YOUTUBE_API_KEY")

    result = None
    if api_key:
        try:
            result = fetch_via_api(api_key, args.recent)
        except Exception as ex:  # noqa: BLE001 — Key falsch/Quota/Netz → sauber auf Fallback gehen
            result = _err("api_error", str(ex)[:200])
    if not result or not result.get("ok"):
        fb = fetch_via_ytdlp(args.recent)
        # API-Fehler-Grund behalten, falls auch Fallback scheitert
        if not fb.get("ok") and result and result.get("reason"):
            fb["api_reason"] = result["reason"]
        result = fb

    if result.get("ok") and args.search:
        q = args.search.lower()
        result["videos"] = [v for v in result["videos"] if q in v["title"].lower()]
        result["filtered_by"] = args.search

    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"geschrieben: {args.output} ({len(result.get('videos', []))} Videos, source={result.get('source','-')})")
    else:
        print(text)

    sys.exit(0 if result.get("ok") else 1)


if __name__ == "__main__":
    main()
