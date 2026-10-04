"""Media processing for multimodal assistant (image/video)."""

import base64
import logging
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

from PIL import Image

from assistant.config import (
    MEDIA_CACHE_DIR,
    MAX_IMAGE_SIZE,
    MAX_VIDEO_DURATION,
    MAX_VIDEO_FRAMES,
    OBSIDIAN_VAULT,
)

logger = logging.getLogger(__name__)

# Ensure cache dir exists
MEDIA_CACHE_DIR.mkdir(parents=True, exist_ok=True)

OBSIDIAN_VAULT_PATH = Path(OBSIDIAN_VAULT).expanduser()


def process_image(file_path: str) -> str:
    """Resize image to MAX_IMAGE_SIZE and return base64 encoded string."""
    p = Path(file_path)
    img = Image.open(p)

    # Convert to RGB if needed (RGBA, palette etc.)
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")

    # Resize if larger than limit
    w, h = img.size
    if max(w, h) > MAX_IMAGE_SIZE:
        ratio = MAX_IMAGE_SIZE / max(w, h)
        new_w, new_h = int(w * ratio), int(h * ratio)
        img = img.resize((new_w, new_h), Image.LANCZOS)

    # Save as JPEG to buffer
    out_path = p.with_suffix(".processed.jpg")
    img.save(out_path, "JPEG", quality=85)

    with open(out_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")

    out_path.unlink(missing_ok=True)
    return b64


def get_video_duration(file_path: str) -> float:
    """Get video duration in seconds using ffprobe."""
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "quiet",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                file_path,
            ],
            capture_output=True, text=True, timeout=10,
        )
        return float(result.stdout.strip())
    except Exception as e:
        logger.warning(f"ffprobe duration error: {e}")
        return 0.0


def extract_video_frames(file_path: str) -> list[str]:
    """Extract keyframes from video and return as base64 list."""
    duration = get_video_duration(file_path)
    if duration <= 0:
        return []

    if duration > MAX_VIDEO_DURATION:
        raise ValueError(f"Video {duration:.0f}s - limit {MAX_VIDEO_DURATION}s")

    # Calculate timestamps for evenly spaced frames
    frame_count = min(MAX_VIDEO_FRAMES, max(1, int(duration)))
    timestamps = [duration * (i + 1) / (frame_count + 1) for i in range(frame_count)]

    frames_b64 = []
    for i, ts in enumerate(timestamps):
        out_path = MEDIA_CACHE_DIR / f"frame_{i}.jpg"
        try:
            subprocess.run(
                [
                    "ffmpeg", "-y", "-v", "quiet",
                    "-ss", str(ts),
                    "-i", file_path,
                    "-vframes", "1",
                    "-vf", f"scale='min({MAX_IMAGE_SIZE},iw)':'min({MAX_IMAGE_SIZE},ih)':force_original_aspect_ratio=decrease",
                    str(out_path),
                ],
                capture_output=True, timeout=15,
            )
            if out_path.exists():
                with open(out_path, "rb") as f:
                    frames_b64.append(base64.b64encode(f.read()).decode("utf-8"))
                out_path.unlink(missing_ok=True)
        except Exception as e:
            logger.warning(f"Frame extraction error at {ts:.1f}s: {e}")

    return frames_b64


def save_media_to_obsidian(file_path: str, custom_name: str = "") -> str:
    """Copy media file to ObsidianVault/media/ and return relative path."""
    src = Path(file_path)
    media_dir = OBSIDIAN_VAULT_PATH / "media"
    media_dir.mkdir(parents=True, exist_ok=True)

    if custom_name:
        dest_name = custom_name + src.suffix
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        dest_name = f"{timestamp}{src.suffix}"

    dest = media_dir / dest_name
    shutil.copy2(str(src), str(dest))
    return f"media/{dest_name}"


def cleanup_media(file_path: str):
    """Delete temporary media file."""
    try:
        Path(file_path).unlink(missing_ok=True)
    except Exception as e:
        logger.warning(f"Media cleanup error: {e}")
