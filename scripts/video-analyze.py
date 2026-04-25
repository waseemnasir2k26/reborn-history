#!/usr/bin/env python3
"""
video-analyze.py — Real Phase-2 backend for Agent 02 (v2.1.0)

Fetches a YouTube video's transcript + shot boundaries so Agent 02 doesn't
have to hallucinate. Optionally runs Whisper (audio re-transcription) and
librosa (BPM detection) when the relevant flags are passed.

Requirements (do NOT auto-install — user runs manually):
    pip install youtube-transcript-api scenedetect[opencv]
    # optional: pip install openai-whisper  (or faster-whisper)
    # optional: pip install librosa soundfile

Usage:
    python scripts/video-analyze.py <youtube_url> [--whisper] [--audio]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from statistics import mean
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "outputs" / "analyzed"


def extract_video_id(url: str) -> str:
    u = urlparse(url)
    if u.hostname in {"youtu.be"}:
        return u.path.lstrip("/")
    if u.hostname and "youtube" in u.hostname:
        if u.path == "/watch":
            return parse_qs(u.query).get("v", [""])[0]
        m = re.match(r"^/(embed|shorts|v)/([\w-]+)", u.path)
        if m:
            return m.group(2)
    raise ValueError(f"could not extract video id from {url}")


def fetch_transcript(video_id: str) -> dict:
    try:
        from youtube_transcript_api import YouTubeTranscriptApi  # type: ignore
    except ImportError:
        return {"error": "youtube-transcript-api not installed (pip install youtube-transcript-api)"}
    try:
        items = YouTubeTranscriptApi.get_transcript(video_id)
        return {
            "segments": items,
            "text": " ".join(i.get("text", "") for i in items),
            "duration_s": (items[-1]["start"] + items[-1].get("duration", 0)) if items else 0,
        }
    except Exception as ex:
        return {"error": f"transcript fetch failed: {ex}"}


def detect_shots(video_path: Path, threshold: float = 27.0) -> dict:
    try:
        from scenedetect import detect, ContentDetector  # type: ignore
    except ImportError:
        return {"error": "scenedetect not installed (pip install scenedetect[opencv])"}
    if not video_path.exists():
        return {"error": f"video file not found locally: {video_path}", "hint": "download with yt-dlp first"}
    try:
        scenes = detect(str(video_path), ContentDetector(threshold=threshold))
        lengths = [(end - start).get_seconds() for start, end in scenes]
        if not lengths:
            return {"shot_count": 0, "lengths_s": []}
        return {
            "shot_count": len(lengths),
            "mean_shot_s": round(mean(lengths), 2),
            "min_shot_s": round(min(lengths), 2),
            "max_shot_s": round(max(lengths), 2),
            "total_duration_s": round(sum(lengths), 2),
            "threshold": threshold,
        }
    except Exception as ex:
        return {"error": f"scene detection failed: {ex}"}


def whisper_transcribe(video_path: Path) -> dict:
    """Optional: re-transcribe audio with openai-whisper or faster-whisper.

    Usage note: install one of `openai-whisper` or `faster-whisper`. Both
    produce comparable text; faster-whisper is ~4x faster on CPU.
    """
    try:
        import whisper  # type: ignore
    except ImportError:
        return {"error": "whisper not installed (pip install openai-whisper)"}
    if not video_path.exists():
        return {"error": f"audio source not found: {video_path}"}
    try:
        model = whisper.load_model("base")
        res = model.transcribe(str(video_path))
        return {"text": res.get("text", ""), "language": res.get("language")}
    except Exception as ex:
        return {"error": f"whisper failed: {ex}"}


def detect_bpm(audio_path: Path) -> dict:
    try:
        import librosa  # type: ignore
    except ImportError:
        return {"error": "librosa not installed (pip install librosa soundfile)"}
    if not audio_path.exists():
        return {"error": f"audio not found: {audio_path}"}
    try:
        y, sr = librosa.load(str(audio_path))
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        return {"bpm": round(float(tempo), 2)}
    except Exception as ex:
        return {"error": f"librosa failed: {ex}"}


def main() -> int:
    p = argparse.ArgumentParser(description="Phase-2 video analyzer for Agent 02.")
    p.add_argument("url", help="YouTube URL")
    p.add_argument("--video-file", help="Local video file for shot detection (yt-dlp first)")
    p.add_argument("--whisper", action="store_true", help="Run Whisper on the local file")
    p.add_argument("--audio", action="store_true", help="Run librosa BPM on the local file")
    args = p.parse_args()

    try:
        vid = extract_video_id(args.url)
    except ValueError as ex:
        print(f"[ERR] {ex}", file=sys.stderr)
        return 2

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[info] analyzing {vid}")
    result: dict = {"video_id": vid, "url": args.url}

    print("  -> transcript ...")
    result["transcript"] = fetch_transcript(vid)

    if args.video_file:
        vp = Path(args.video_file)
        print("  -> shot boundaries ...")
        result["shots"] = detect_shots(vp)
        if args.whisper:
            print("  -> whisper ...")
            result["whisper"] = whisper_transcribe(vp)
        if args.audio:
            print("  -> bpm ...")
            result["audio"] = detect_bpm(vp)
    else:
        result["shots"] = {"skipped": "pass --video-file <path> after downloading with yt-dlp"}

    out = OUT_DIR / f"{vid}.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[ok] wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
