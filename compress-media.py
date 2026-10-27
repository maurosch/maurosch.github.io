#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyvips[binary]>=3"]
#
# # pyvips is only published as source. If uv can see a system libvips while
# # building it (e.g. Homebrew's), it compiles a wrapper linked to that one,
# # which overrides the libvips 8.18 bundled in pyvips-binary (Ultra HDR
# # support). Hiding pkg-config during the build avoids that.
# [tool.uv.extra-build-variables]
# pyvips = { PKG_CONFIG_LIBDIR = "/nonexistent", PKG_CONFIG_PATH = "/nonexistent" }
# ///
"""Compress photos and videos in a folder for the web.

Usage:
    ./compress_media.py DIR [--backup-root PATH] [--dry-run] [--redo] [--sdr]

Originals are copied to BACKUP_ROOT/<dir-name>/ (default ~/photo-originals),
outside the site. Safe to re-run: anything already backed up is skipped,
unless --redo is given, which re-processes from those originals.

Photos (.jpg/.jpeg): auto-rotated, resized to fit 2000px, quality 80.
  EXIF/XMP (GPS, camera info) is removed, but the ICC color profile is kept
  so Display P3 photos keep their colors. Ultra HDR photos (Pixel, Samsung,
  recent iPhones) keep their gain map, resized and rotated with the photo,
  so they still look HDR on HDR screens. Use --sdr to drop gain maps.

Videos (.mp4/.mov): H.264 + AAC .mp4, fit 1920px, CRF 26, faststart.
  HDR (HLG / PQ) is tone-mapped to SDR. All metadata, including GPS, is
  removed. .mov files are replaced by .mp4, so update the links in your
  posts. Needs ffmpeg (built with zimg) and ffprobe on PATH.
"""

from __future__ import annotations

import argparse
import functools
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pyvips

IMAGE_EXTS = {".jpg", ".jpeg"}
VIDEO_EXTS = {".mp4", ".mov"}

IMAGE_MAX = 2000
IMAGE_QUALITY = 80

VIDEO_MAX = 1920
VIDEO_CRF = 26
AUDIO_BITRATE = "128k"

HDR_TRANSFERS = {"arib-std-b67", "smpte2084"}  # HLG, PQ


def human(n: int) -> str:
    size = float(n)
    for unit in ("B", "K", "M", "G"):
        if size < 1024 or unit == "G":
            return f"{size:.0f}{unit}" if unit == "B" else f"{size:.1f}{unit}"
        size /= 1024
    return f"{n}B"


def atomic_output(directory: Path, suffix: str) -> Path:
    """Temp file in the target dir, so the final rename is atomic."""
    fd, name = tempfile.mkstemp(prefix=".compress.", suffix=suffix, dir=directory)
    os.close(fd)
    return Path(name)


def publish(tmp: Path, dest: Path) -> None:
    tmp.chmod(0o644)  # mkstemp creates 0600; web servers need to read it
    tmp.replace(dest)


# ---------- photos ----------


def compress_image(src: Path, tmp: Path, keep_hdr: bool) -> str:
    # thumbnail() applies the EXIF rotation and, for Ultra HDR, resizes and
    # rotates the gain map together with the photo. size="down": never upscale.
    im = pyvips.Image.thumbnail(str(src), IMAGE_MAX, height=IMAGE_MAX, size="down").copy()

    fields = im.get_fields()
    has_gainmap = any(f.startswith("gainmap") for f in fields)

    # Remove EXIF (GPS, camera, dates), XMP and IPTC by hand. The `keep`
    # save option can't be used: it would also drop the gain map metadata.
    for f in fields:
        if f.startswith("exif-") or f in ("xmp-data", "iptc-data"):
            im.remove(f)

    if has_gainmap and keep_hdr:
        im.uhdrsave(str(tmp), Q=IMAGE_QUALITY)
        return " (Ultra HDR)"

    for f in fields:
        if f.startswith("gainmap"):
            im.remove(f)
    im.jpegsave(
        str(tmp),
        Q=IMAGE_QUALITY,
        interlace=True,         # progressive
        optimize_coding=True,
        subsample_mode="on",    # 4:2:0
    )
    return " (HDR gain map dropped)" if has_gainmap else ""


# ---------- videos ----------


@functools.cache
def has_filter(name: str) -> bool:
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-filters"], capture_output=True, text=True, check=True
    ).stdout
    # Lines look like: " .SC zscale            V->V       Apply resizing..."
    return any(
        len(parts) > 1 and parts[1] == name
        for parts in (line.split() for line in out.splitlines())
    )


def video_transfer(src: Path) -> str:
    out = subprocess.run(
        [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=color_transfer",
            "-of", "default=nw=1:nk=1", str(src),
        ],
        capture_output=True, text=True, check=True,
    )
    return out.stdout.strip()


def compress_video(src: Path, tmp: Path) -> str:
    # Fit inside VIDEO_MAX x VIDEO_MAX, never upscale, even dimensions for H.264
    vf = [
        f"scale=w='min({VIDEO_MAX},iw)':h='min({VIDEO_MAX},ih)'"
        ":force_original_aspect_ratio=decrease:force_divisible_by=2"
    ]
    color: list[str] = []
    note = ""
    if video_transfer(src) in HDR_TRANSFERS:
        # HDR -> SDR tone mapping (needs ffmpeg built with libzimg)
        if not has_filter("zscale"):
            raise RuntimeError(
                "HDR video, but this ffmpeg has no 'zscale' filter (built without zimg). "
                "On macOS: brew uninstall ffmpeg && brew tap homebrew-ffmpeg/ffmpeg && "
                "brew install homebrew-ffmpeg/ffmpeg/ffmpeg --with-zimg"
            )
        vf += [
            "zscale=t=linear:npl=100", "format=gbrpf32le", "zscale=p=bt709",
            "tonemap=tonemap=hable:desat=0", "zscale=t=bt709:m=bt709:r=tv",
        ]
        color = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
        note = " (HDR tone-mapped to SDR)"
    vf.append("format=yuv420p")

    subprocess.run(
        [
            "ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(src),
            "-vf", ",".join(vf),
            "-c:v", "libx264", "-preset", "slow", "-crf", str(VIDEO_CRF),
            *color,
            "-c:a", "aac", "-b:a", AUDIO_BITRATE,
            "-map_metadata", "-1", "-map_chapters", "-1",
            "-movflags", "+faststart",
            "-f", "mp4", str(tmp),
        ],
        check=True,
    )
    return note


# ---------- main ----------


def is_video(p: Path) -> bool:
    return p.suffix.lower() in VIDEO_EXTS


def find_backup(src: Path, backup: Path) -> Path | None:
    """The original of `src` in the backup folder, if it was already processed."""
    if not is_video(src):
        candidate = backup / src.name
        return candidate if candidate.exists() else None
    # foo.MOV becomes foo.mp4, so match any video original with the same stem
    for p in sorted(backup.iterdir()):
        if p.stem == src.stem and is_video(p):
            return p
    return None


def output_path(src: Path) -> Path:
    if is_video(src) and src.suffix.lower() != ".mp4":
        return src.with_suffix(".mp4")
    return src


def process(src: Path, backup: Path, *, dry_run: bool, redo: bool, keep_hdr: bool) -> bool:
    dest = output_path(src)
    original = find_backup(src, backup)

    if original and not redo:
        print(f"skip (already processed): {src.name}")
        return True
    if not original and dest != src and dest.exists():
        print(f"skip: {dest.name} already exists, won't overwrite it with {src.name}",
              file=sys.stderr)
        return True
    if dry_run:
        action = "would redo from backup" if original else "would compress"
        print(f"{action}: {src.name}" + (f" -> {dest.name}" if dest != src else ""))
        return True

    created_backup = original is None
    if original is None:
        original = backup / src.name
        shutil.copy2(src, original)

    tmp = atomic_output(src.parent, ".mp4" if is_video(src) else ".jpg")
    try:
        if is_video(src):
            note = compress_video(original, tmp)
        else:
            note = compress_image(original, tmp, keep_hdr)
        publish(tmp, dest)
    except Exception as e:  # noqa: BLE001 - report and continue with the next file
        tmp.unlink(missing_ok=True)
        if created_backup:
            original.unlink(missing_ok=True)  # so the next run retries this file
        if isinstance(e, subprocess.CalledProcessError):
            e = f"{e.cmd[0]} exited with status {e.returncode} (see its output above)"
        elif isinstance(e, pyvips.Error):
            e = str(e).strip().splitlines()[-1]
        print(f"FAILED: {src.name} (original untouched): {e}", file=sys.stderr)
        return False

    if dest != src:
        src.unlink()
    print(f"{original.name}: {human(original.stat().st_size)} -> "
          f"{dest.name} {human(dest.stat().st_size)}{note}")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("dir", type=Path, help="folder with photos/videos")
    ap.add_argument("--backup-root", type=Path, default=Path.home() / "photo-originals",
                    help="where originals are kept (default: ~/photo-originals)")
    ap.add_argument("--dry-run", action="store_true", help="only show what would be done")
    ap.add_argument("--redo", action="store_true",
                    help="re-process already processed files from their backed-up originals")
    ap.add_argument("--sdr", action="store_true",
                    help="drop Ultra HDR gain maps (plain SDR JPEGs)")
    args = ap.parse_args()

    src_dir: Path = args.dir.resolve()
    if not src_dir.is_dir():
        ap.error(f"not a directory: {args.dir}")

    files = sorted(
        p for p in src_dir.iterdir()
        if p.is_file() and not p.name.startswith(".")
        and p.suffix.lower() in IMAGE_EXTS | VIDEO_EXTS
    )
    if not files:
        print("nothing to do")
        return 0

    if any(is_video(p) for p in files):
        missing = [c for c in ("ffmpeg", "ffprobe") if shutil.which(c) is None]
        if missing:
            print(f"missing command(s) for videos: {', '.join(missing)}", file=sys.stderr)
            return 1

    if not args.sdr and pyvips.type_find("VipsOperation", "uhdrsave") == 0:
        v = ".".join(str(pyvips.version(i)) for i in range(3))
        print(
            f"warning: loaded libvips {v} has no Ultra HDR support (needs 8.18+ built with "
            "libultrahdr), so HDR gain maps will be dropped. pyvips is probably picking up "
            "another libvips (e.g. Homebrew's) instead of the one bundled with pyvips[binary]. "
            "Stop with Ctrl-C, or use --sdr to silence this.",
            file=sys.stderr,
        )

    backup = args.backup_root.expanduser() / src_dir.name
    backup.mkdir(parents=True, exist_ok=True)

    results = [
        process(p, backup, dry_run=args.dry_run, redo=args.redo, keep_hdr=not args.sdr)
        for p in files
    ]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())