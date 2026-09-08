#!/usr/bin/env python3
"""
Extract transcript with timestamps from a YouTube video.
Uses yt-dlp auto-captions first; falls back to downloading audio + OpenAI Whisper.

Usage:
  python get_transcript.py <youtube_url> [--lang de|en] [--output transcript.json]

Output JSON format:
  {
    "title": "Video title",
    "duration": 3600,
    "source": "captions" | "whisper",
    "segments": [
      {"start": 0.0, "end": 12.5, "text": "Welcome to this video..."},
      ...
    ]
  }
"""

import argparse
import json
import os
import sys
import tempfile


def seconds_to_hhmmss(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def get_transcript_via_captions(url, lang="de"):
    """Try to get transcript from YouTube's auto-generated or manual captions."""
    import subprocess
    import glob

    with tempfile.TemporaryDirectory() as tmpdir:
        # Try requested language first, then 'en', then any auto-caption
        langs_to_try = list(dict.fromkeys([lang, "en", "de"]))

        for try_lang in langs_to_try:
            cmd = [
                "yt-dlp",
                "--write-auto-subs",
                "--write-subs",
                "--sub-lang", try_lang,
                "--sub-format", "json3",
                "--skip-download",
                "--no-playlist",
                "-o", os.path.join(tmpdir, "%(title)s.%(ext)s"),
                url,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)

            vtt_files = glob.glob(os.path.join(tmpdir, f"*.{try_lang}.json3"))
            if not vtt_files:
                vtt_files = glob.glob(os.path.join(tmpdir, "*.json3"))
            if not vtt_files:
                continue

            # Parse the JSON3 subtitle format
            with open(vtt_files[0], encoding="utf-8") as f:
                data = json.load(f)

            segments = []
            for event in data.get("events", []):
                if "segs" not in event:
                    continue
                start_ms = event.get("tStartMs", 0)
                dur_ms = event.get("dDurationMs", 0)
                text = "".join(s.get("utf8", "") for s in event["segs"]).strip()
                if text and text != "\n":
                    segments.append({
                        "start": start_ms / 1000,
                        "end": (start_ms + dur_ms) / 1000,
                        "text": text,
                    })

            if segments:
                # Get title via yt-dlp
                title_cmd = ["yt-dlp", "--get-title", "--no-playlist", url]
                title_result = subprocess.run(title_cmd, capture_output=True, text=True)
                title = title_result.stdout.strip() or "Unknown Title"

                return {
                    "title": title,
                    "source": "captions",
                    "lang": try_lang,
                    "segments": segments,
                }

    return None


def get_transcript_via_whisper(url, lang=None):
    """Download audio and transcribe with OpenAI Whisper API."""
    import subprocess

    try:
        import openai
    except ImportError:
        print("ERROR: openai package not installed. Run: pip install openai", file=sys.stderr)
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = os.path.join(tmpdir, "audio.mp3")

        # Download audio
        cmd = [
            "yt-dlp",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "3",
            "--no-playlist",
            "-o", audio_path,
            url,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"ERROR downloading audio: {result.stderr}", file=sys.stderr)
            sys.exit(1)

        # Get title
        title_cmd = ["yt-dlp", "--get-title", "--no-playlist", url]
        title_result = subprocess.run(title_cmd, capture_output=True, text=True)
        title = title_result.stdout.strip() or "Unknown Title"

        # Transcribe with Whisper
        client = openai.OpenAI()
        with open(audio_path, "rb") as audio_file:
            kwargs = {"model": "whisper-1", "response_format": "verbose_json", "timestamp_granularities": ["segment"]}
            if lang:
                kwargs["language"] = lang
            transcript = client.audio.transcriptions.create(file=audio_file, **kwargs)

        segments = [
            {
                "start": seg.start,
                "end": seg.end,
                "text": seg.text.strip(),
            }
            for seg in transcript.segments
        ]

        return {
            "title": title,
            "source": "whisper",
            "lang": lang or "auto",
            "segments": segments,
        }


def merge_segments(segments, target_count=40):
    """Merge many short segments into ~target_count larger chunks for readability."""
    if not segments or len(segments) <= target_count:
        return segments

    total_duration = segments[-1]["end"] - segments[0]["start"]
    chunk_duration = total_duration / target_count

    merged = []
    current_start = segments[0]["start"]
    current_texts = []
    current_end = 0

    for seg in segments:
        current_texts.append(seg["text"])
        current_end = seg["end"]
        if current_end - current_start >= chunk_duration:
            merged.append({
                "start": current_start,
                "end": current_end,
                "text": " ".join(current_texts).strip(),
            })
            current_start = current_end
            current_texts = []

    if current_texts:
        merged.append({
            "start": current_start,
            "end": current_end,
            "text": " ".join(current_texts).strip(),
        })

    return merged


def main():
    parser = argparse.ArgumentParser(description="Extract YouTube transcript with timestamps")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--lang", default="de", help="Preferred language (de, en, etc.)")
    parser.add_argument("--output", default="-", help="Output file path (- for stdout)")
    parser.add_argument("--merge", type=int, default=50, help="Merge into N segments (0 = no merge)")
    args = parser.parse_args()

    print(f"Trying captions for: {args.url}", file=sys.stderr)
    result = get_transcript_via_captions(args.url, args.lang)

    if not result:
        print("No captions found. Falling back to Whisper transcription...", file=sys.stderr)
        result = get_transcript_via_whisper(args.url, args.lang if args.lang != "de" else None)

    if args.merge > 0:
        result["segments"] = merge_segments(result["segments"], args.merge)

    # Add human-readable timestamps
    for seg in result["segments"]:
        seg["timestamp"] = seconds_to_hhmmss(seg["start"])

    output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output == "-":
        print(output)
    else:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Transcript saved to: {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
