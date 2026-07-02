#!/usr/bin/env python3
"""Re-download and re-optimize the site's media from the live AMC site.

The repo commits only the optimized outputs (webp images + re-encoded video),
not the multi-hundred-MB originals. This script regenerates everything from
scratch so the pipeline is reproducible and the originals are never "lost":

    python3 tools/fetch_and_optimize.py            # images only (no ffmpeg needed)
    python3 tools/fetch_and_optimize.py --videos   # also re-encode the 4 videos

Images: downloaded from amchealthcareinc.com, converted to .webp (quality 82).
Videos: downloaded, then re-encoded with ffmpeg — the homepage background loop
is downscaled to 1080p (MP4 + WebM, no audio); the promo/feature films are
compressed MP4 (H.264, faststart) at 720p/1080p with poster frames.

Dependencies: Pillow (always), imageio-ffmpeg (only with --videos).
Requires outbound network access to amchealthcareinc.com.
"""
import argparse
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_ROOT = os.path.join(REPO, "assets", "img")
VIDEO_OUT = os.path.join(REPO, "assets", "video")
VIDEO_SRC = os.path.join(REPO, "assets", "video_src")
UPLOADS = "https://amchealthcareinc.com/wp-content/uploads/"
WEBP_QUALITY = 82

# Every image the generated pages reference (mirrors the URLs used in build.py,
# plus the leadership/process/partners sets). Paths are relative to UPLOADS.
IMAGES = [
    "2024/02/long-logo.png",
    "2024/09/AMC_Banner_3x6_page-0001-1024x512.jpg",
    "2024/09/AMC_Logo_Horizontal_Secondary_Dark-1024x91.png",
    "2024/09/Brent_Yessin_Edit-square.jpg",
    "2024/09/Graham_Russell-square.jpeg",
    "2024/09/Brett_Scott-Modified-square.jpeg",
    "2024/09/Jim_Cusack-Modified-square-scaled.jpeg",
    "2024/09/TFMCviewfromMainStreet-copy_3-1.jpg",
    "2024/09/unit-being-set-on-pier-and-beam.png",
    "2024/12/AMC-Hospital-Shot-Outter-V1.png",
    "2024/12/AMC-Hospital-Shot-Inner-V2.png",
    "2024/12/IMG_3339-rotated.jpg",
    "2024/12/IMG_3352-rotated.jpg",
    "2025/02/IMG_2606.jpg",
    "2025/07/IMG_4628.jpg",
    "2026/01/1758167803794.jpg",
    "2026/05/Essex-Capital-Group-Rob-Swain-1-600x600-1.jpg",
]

# (source URL suffix, output basename, ffmpeg args). The loop gets an extra
# WebM pass; everything else is MP4 only.
VIDEOS = [
    ("2025/12/Logo-Animation-2_medium.mp4", "logo-animation",
     ["-vf", "scale=1920:-2", "-an", "-c:v", "libx264", "-preset", "medium",
      "-crf", "28", "-pix_fmt", "yuv420p", "-movflags", "+faststart"], "loop"),
    ("2024/12/AMC-Healthcare-Hospital-Final-Reduced.mp4", "hospital-film",
     ["-c:v", "libx264", "-preset", "medium", "-crf", "25", "-pix_fmt", "yuv420p",
      "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart"], "film"),
    ("2026/02/AMC-60-1.mp4", "amc-60",
     ["-vf", "scale=1280:-2", "-c:v", "libx264", "-preset", "faster", "-crf", "28",
      "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart"], "film"),
    ("2025/12/AMC-America-First_medium.mp4", "america-first",
     ["-vf", "scale=1280:-2", "-c:v", "libx264", "-preset", "faster", "-crf", "28",
      "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart"], "film"),
]


def curl(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    r = subprocess.run(["curl", "-sS", "--max-time", "300", "-o", dest, "-w", "%{http_code}", url],
                       capture_output=True, text=True)
    return r.stdout.strip()[-3:] == "200" and os.path.exists(dest) and os.path.getsize(dest) > 0


def do_images():
    from PIL import Image
    print(f"Fetching + optimizing {len(IMAGES)} images...")
    for rel in IMAGES:
        src = os.path.join(IMG_ROOT, "_src_" + rel.replace("/", "_"))
        if not curl(UPLOADS + rel, src):
            print(f"  FAIL download {rel}")
            continue
        webp = os.path.join(IMG_ROOT, os.path.splitext(rel)[0] + ".webp")
        os.makedirs(os.path.dirname(webp), exist_ok=True)
        im = Image.open(src)
        if im.mode in ("P", "LA"):
            im = im.convert("RGBA")
        elif im.mode == "CMYK":
            im = im.convert("RGB")
        im.save(webp, "WEBP", quality=WEBP_QUALITY, method=6)
        os.remove(src)
        print(f"  ok  {os.path.relpath(webp, REPO)}")


def do_videos():
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    os.makedirs(VIDEO_OUT, exist_ok=True)
    os.makedirs(VIDEO_SRC, exist_ok=True)
    print(f"Fetching + re-encoding {len(VIDEOS)} videos...")
    for suffix, name, args, kind in VIDEOS:
        src = os.path.join(VIDEO_SRC, os.path.basename(suffix))
        if not os.path.exists(src) and not curl(UPLOADS + suffix, src):
            print(f"  FAIL download {suffix}")
            continue
        mp4 = os.path.join(VIDEO_OUT, name + ".mp4")
        subprocess.run([ff, "-y", "-hide_banner", "-loglevel", "error", "-i", src] + args + [mp4], check=True)
        if kind == "loop":
            webm = os.path.join(VIDEO_OUT, name + ".webm")
            subprocess.run([ff, "-y", "-hide_banner", "-loglevel", "error", "-i", src,
                            "-vf", "scale=1920:-2", "-an", "-c:v", "libvpx-vp9",
                            "-b:v", "0", "-crf", "34", "-row-mt", "1", "-deadline", "good", webm], check=True)
        poster = os.path.join(VIDEO_OUT, name + "-poster.webp")
        subprocess.run([ff, "-y", "-hide_banner", "-loglevel", "error", "-ss", "2", "-i", mp4,
                        "-frames:v", "1", "-c:v", "libwebp", "-q:v", "80", poster], check=True)
        print(f"  ok  {name}")
    # Originals are large and intentionally not committed; drop them.
    import shutil
    shutil.rmtree(VIDEO_SRC, ignore_errors=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--videos", action="store_true", help="also re-encode videos (needs imageio-ffmpeg)")
    args = ap.parse_args()
    do_images()
    if args.videos:
        do_videos()
    print("Done. Run `python3 build.py` to regenerate pages.")
