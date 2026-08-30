import subprocess, json, os, shutil, re, math, hashlib, sys, platform
from os import cpu_count as _cpu_count

def _worker_count(n_tasks):
    cpus = _cpu_count() or 2
    return min(n_tasks, max(2, cpus))
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageStat
try:
    import cv2
except Exception:
    cv2 = None

def resolve_binary(name):
    search_roots = [os.path.abspath(os.path.dirname(__file__))]
    if getattr(sys, "_MEIPASS", None):
        search_roots.insert(0, sys._MEIPASS)
    for root in search_roots:
        for candidate in (name, f"{name}.exe"):
            local_path = os.path.join(root, candidate)
            if os.path.exists(local_path) and os.access(local_path, os.X_OK):
                return local_path
    path_bin = shutil.which(name)
    if path_bin:
        return path_bin
    return name

FFMPEG = resolve_binary("ffmpeg")
FFPROBE = resolve_binary("ffprobe")

def _run_ffmpeg(cmd_args, force_software=False, timeout=None):
    if not force_software and platform.system() == "Darwin":
        hw_cmd = [FFMPEG, "-hwaccel", "videotoolbox"] + cmd_args
        try:
            result = subprocess.run(hw_cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=timeout)
        except subprocess.TimeoutExpired:
            return False
        if result.returncode == 0:
            return True
    try:
        result = subprocess.run([FFMPEG] + cmd_args, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=timeout)
    except subprocess.TimeoutExpired:
        return False
    return result.returncode == 0

def _run_capture(cmd):
    return subprocess.run(cmd, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def _parse_rate(rate_str):
    if not rate_str:
        return 0.0
    if "/" in str(rate_str):
        try:
            num, den = str(rate_str).split("/")
            num_f, den_f = float(num), float(den)
            return num_f / den_f if den_f != 0 else 0.0
        except Exception:
            return 0.0
    try:
        return float(rate_str)
    except Exception:
        return 0.0

def _human_mbps(bit_rate):
    try:
        value = int(bit_rate or 0)
    except Exception:
        value = 0
    return "Unknown" if value <= 0 else f"{round(value / 1_000_000, 1)} Mbps"

def _human_kbps(bit_rate):
    try:
        value = int(bit_rate or 0)
    except Exception:
        value = 0
    return "Unknown" if value <= 0 else f"{round(value / 1000)} Kbps"

def _human_gb_mb(size_bytes):
    try:
        size_bytes = int(size_bytes or 0)
    except Exception:
        size_bytes = 0
    mb = size_bytes / (1024 * 1024) if size_bytes > 0 else 0.0
    gb = size_bytes / (1024 * 1024 * 1024) if size_bytes > 0 else 0.0
    return {"bytes": size_bytes, "mb": round(mb, 2), "gb": round(gb, 2), "display": f"{round(gb, 2)} GB / {round(mb, 2)} MB" if size_bytes > 0 else "Unknown"}

def _format_channels(ch):
    try:
        ch = int(ch or 0)
    except Exception:
        ch = 0
    if ch <= 0:
        return "Unknown"
    return "1 channel" if ch == 1 else f"{ch} channels"

def _format_sample_rate(sr):
    try:
        sr = int(sr or 0)
    except Exception:
        sr = 0
    return "Unknown" if sr <= 0 else f"{round(sr / 1000, 1)} KHz"

def _format_level(codec_name, level):
    try:
        level = int(level)
    except Exception:
        return ""
    codec_name = (codec_name or "").lower()
    if level <= 0:
        return ""
    if codec_name in ("hevc", "h265", "libx265"):
        main = level / 30.0
        return f"L{int(main)}" if float(main).is_integer() else f"L{main:.1f}"
    if codec_name in ("h264", "avc", "libx264"):
        main = level / 10.0
        return f"L{int(main)}" if float(main).is_integer() else f"L{main:.1f}"
    return f"L{level}"

def _format_prores_profile(profile):
    profile = (profile or "").strip()
    profile_map = {
        "proxy": "422 Proxy",
        "lt": "422 LT",
        "standard": "422",
        "hq": "422 HQ",
        "4444": "4444",
        "4444 xq": "4444 XQ",
    }
    return profile_map.get(profile.lower(), profile)

def _format_pcm_codec(codec_name, codec_long):
    long_name = codec_long or ""
    details = []
    bits = re.search(r"(\d+)-bit", long_name)
    if bits:
        details.append(f"{bits.group(1)}-bit")
    if "float" in long_name.lower():
        details.append("float")
    return f"PCM ({' '.join(details)})" if details else "PCM"

def _video_codec_full(v):
    codec_name = v.get("codec_name", "") or ""
    codec_long = v.get("codec_long_name", "") or ""
    profile = (v.get("profile", "") or "").strip()
    codec_tag = (v.get("codec_tag_string", "") or "").strip()
    if codec_name.lower() == "prores":
        sub = []
        if codec_tag and codec_tag != "????":
            sub.append(codec_tag)
        prores_profile = _format_prores_profile(profile)
        if prores_profile:
            sub.append(prores_profile)
        return f"ProRes ({', '.join(sub)})" if sub else "ProRes"
    level_text = _format_level(codec_name, v.get("level"))
    pieces = []
    if codec_name:
        pieces.append("HEVC" if codec_name.lower() == "hevc" else "AVC" if codec_name.lower() == "h264" else codec_name.upper())
    sub = []
    if codec_long:
        sub.append(codec_long)
    if profile:
        prof = profile
        if level_text:
            prof = f"{prof}@{level_text}"
        sub.append(prof)
    elif level_text:
        sub.append(level_text)
    return f"{pieces[0]} ({', '.join(sub)})" if sub and pieces else (pieces[0] if pieces else "Unknown")

def _audio_codec_full(a):
    codec_name = a.get("codec_name", "") or ""
    codec_long = a.get("codec_long_name", "") or ""
    profile = (a.get("profile", "") or "").strip()
    if codec_name.lower().startswith("pcm"):
        return _format_pcm_codec(codec_name, codec_long)
    audio_names = {
        "aac": "AAC",
        "ac3": "AC-3",
        "eac3": "E-AC-3",
        "mp3": "MP3",
        "flac": "FLAC",
        "alac": "ALAC",
        "opus": "Opus",
        "vorbis": "Vorbis",
    }
    head = audio_names.get(codec_name.lower(), codec_name.upper() if codec_name else "Unknown")
    sub = []
    if codec_long:
        sub.append(codec_long)
    if profile and profile.lower() not in codec_long.lower():
        sub.append(profile)
    return f"{head} ({', '.join(sub)})" if sub else head

def should_force_software_decode(meta):
    if not meta:
        return False
    video_line = (meta.get("video_line", "") or "").lower()
    return ("vp9" in video_line) or ("av1" in video_line)

def get_video_metadata(path):
    cmd = [
        FFPROBE, "-v", "error", "-show_entries",
        "format=duration,size,bit_rate:stream=index,codec_type,codec_name,codec_long_name,codec_tag_string,profile,level,width,height,avg_frame_rate,bit_rate,pix_fmt,bits_per_raw_sample,sample_rate,channels,channel_layout",
        "-of", "json", path
    ]
    try:
        data = json.loads(subprocess.check_output(cmd))
        streams = data.get("streams", [])
        v = next((s for s in streams if s.get("codec_type") == "video"), {})
        a = next((s for s in streams if s.get("codec_type") == "audio"), {})
        fps = round(_parse_rate(v.get("avg_frame_rate", "0/0")), 3)
        size_info = _human_gb_mb(data.get("format", {}).get("size", 0))
        duration = float(data.get("format", {}).get("duration", 0) or 0)
        v_bitrate = _human_mbps(v.get("bit_rate") or data.get("format", {}).get("bit_rate"))
        a_bitrate = _human_kbps(a.get("bit_rate"))
        sample_rate_text = _format_sample_rate(a.get("sample_rate"))
        channels_text = _format_channels(a.get("channels"))
        video_line = f"{_video_codec_full(v)}, {v_bitrate}, {fps} fps"
        audio_parts = [_audio_codec_full(a)]
        if a_bitrate != "Unknown":
            audio_parts.append(a_bitrate)
        if sample_rate_text != "Unknown":
            audio_parts.append(sample_rate_text)
        if channels_text != "Unknown":
            audio_parts.append(channels_text)
        audio_parts.append("1 stream" if a else "0 stream")
        return {
            "name": os.path.basename(path),
            "size": size_info["mb"],
            "size_display": size_info["display"],
            "width": int(v.get("width", 0) or 0),
            "height": int(v.get("height", 0) or 0),
            "duration": duration,
            "fps": fps,
            "video_line": video_line,
            "audio_line": ", ".join(audio_parts),
        }
    except Exception as e:
        print(f"Metadata Error: {e}")
        return None

def detect_effective_end_time(path, meta, start_t, requested_end_t):
    if not meta:
        return requested_end_t
    duration = meta.get("duration", 0)
    if duration <= 0:
        return requested_end_t
    tail_window = min(12.0, max(3.0, requested_end_t - start_t))
    scan_start = max(start_t, requested_end_t - tail_window)
    scan_len = max(0.5, requested_end_t - scan_start)
    cmd = [FFMPEG, "-hide_banner", "-ss", str(scan_start), "-t", str(scan_len), "-i", path, "-vf", "blackdetect=d=0.20:pix_th=0.98", "-an", "-f", "null", "-"]
    result = _run_capture(cmd)
    matches = re.findall(r"black_start:(\S+)\s+black_end:(\S+)\s+black_duration:(\S+)", result.stderr or "")
    if matches:
        best_black_start = None
        for bs, be, bd in matches:
            try:
                bs_f, be_f, bd_f = float(bs), float(be), float(bd)
            except Exception:
                continue
            if be_f >= requested_end_t - 0.15 and bd_f >= 0.20:
                if best_black_start is None or bs_f < best_black_start:
                    best_black_start = bs_f
        if best_black_start is not None:
            return max(start_t, best_black_start - 0.20)
    return max(start_t, requested_end_t - 0.20)

def _build_thumbnail_timestamps(start_t, end_t, count):
    if count <= 0:
        return []
    if count == 1:
        return [(start_t + end_t) / 2.0]
    dur = max(0.1, end_t - start_t)
    interval = dur / (count - 1)
    return [start_t + (i * interval) for i in range(count)]

def _candidate_timestamps(target, safe_start, safe_end, index, count):
    span = max(0.1, safe_end - safe_start)
    small = max(0.45, min(2.0, span * 0.01))
    medium = max(1.2, min(5.0, span * 0.025))
    large = max(2.5, min(9.0, span * 0.05))
    if count <= 1:
        offsets = [0.0, small, -small, medium, -medium]
    elif index == 0:
        offsets = [0.0, small, medium, large, -small]
    elif index == count - 1:
        offsets = [0.0, -small, -medium, -large, small]
    else:
        offsets = [0.0, small, -small, medium, -medium, large, -large]
    candidates = []
    seen = set()
    for offset in offsets:
        ts = min(safe_end, max(safe_start, target + offset))
        key = round(ts, 3)
        if key not in seen:
            seen.add(key)
            candidates.append(ts)
    return candidates

def _extract_single_frame(path, ts, out_path, scale_width, quality=3, force_software=False, accurate=True, timeout=None):
    ext = os.path.splitext(out_path)[1].lower()
    cmd = ["-y", "-ss", str(ts)]
    if not accurate:
        cmd += ["-noaccurate_seek"]
    cmd += ["-i", path, "-vf", f"scale={scale_width}:-1", "-frames:v", "1"]
    if ext in (".jpg", ".jpeg"):
        cmd += ["-q:v", str(quality)]
    cmd += [out_path]
    return _run_ffmpeg(cmd, force_software=force_software, timeout=timeout)

def _rgb_distance(a, b):
    return math.sqrt(((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2) + ((a[2] - b[2]) ** 2))

def _mean_rgb(img):
    stat = ImageStat.Stat(img.convert("RGB"))
    return tuple(float(x) for x in stat.mean[:3])

def _calc_sharpness(gray_img):
    edges = gray_img.filter(ImageFilter.FIND_EDGES)
    stat = ImageStat.Stat(edges)
    return float(stat.mean[0] * stat.mean[0])

def _calc_faces(gray_img, color_img):
    if cv2 is None:
        return {"count": 0, "largest_ratio": 0.0, "centered_bonus": 0.0}
    try:
        import numpy as np
        detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = detector.detectMultiScale(np.array(gray_img), scaleFactor=1.1, minNeighbors=4, minSize=(24, 24))
        if faces is None or len(faces) == 0:
            return {"count": 0, "largest_ratio": 0.0, "centered_bonus": 0.0}
        w, h = color_img.size
        img_area = max(1.0, float(w * h))
        largest_ratio = 0.0
        centered_bonus = 0.0
        for (x, y, fw, fh) in faces:
            ratio = (fw * fh) / img_area
            largest_ratio = max(largest_ratio, ratio)
            cx, cy = x + fw / 2.0, y + fh / 2.0
            dx, dy = abs((cx / w) - 0.5), abs((cy / h) - 0.5)
            centered_bonus = max(centered_bonus, max(0.0, 1.0 - ((dx + dy) * 1.5)))
        return {"count": int(len(faces)), "largest_ratio": float(largest_ratio), "centered_bonus": float(centered_bonus)}
    except Exception:
        return {"count": 0, "largest_ratio": 0.0, "centered_bonus": 0.0}

def _analyze_frame(image_path, allow_faces=False):
    try:
        img = Image.open(image_path).convert("RGB")
        small = img.resize((160, 90), Image.Resampling.BILINEAR)
        gray = small.convert("L")
        mean_rgb = _mean_rgb(small)
        hsv_stat = ImageStat.Stat(small.convert("HSV"))
        avg_sat, avg_val = float(hsv_stat.mean[1]), float(hsv_stat.mean[2])
        pixels = list(gray.getdata())
        if not pixels:
            return None
        dark_ratio = sum(1 for p in pixels if p < 18) / len(pixels)
        bright_ratio = sum(1 for p in pixels if p > 245) / len(pixels)
        contrast = float(max(pixels) - min(pixels))
        sharpness = _calc_sharpness(gray)
        faces = _calc_faces(gray, small) if allow_faces else {"count": 0, "largest_ratio": 0.0, "centered_bonus": 0.0}
        return {
            "mean_rgb": mean_rgb,
            "avg_sat": avg_sat,
            "avg_val": avg_val,
            "dark_ratio": dark_ratio,
            "bright_ratio": bright_ratio,
            "contrast": contrast,
            "sharpness": sharpness,
            "face_count": faces["count"],
            "face_ratio": faces["largest_ratio"],
            "face_centered": faces["centered_bonus"],
        }
    except Exception:
        return None

def _is_usable_stats(stats):
    return bool(stats) and stats["dark_ratio"] <= 0.92 and stats["avg_val"] >= 20 and stats["contrast"] >= 10

def _quality_score(stats):
    if not stats:
        return -999999.0
    if not _is_usable_stats(stats):
        return -500000.0
    score = 0.0
    score += min(stats["sharpness"], 700.0) * 0.12
    score += min(stats["contrast"], 120.0) * 1.8
    score += min(stats["avg_sat"], 180.0) * 0.45
    score += min(stats["avg_val"], 210.0) * 0.35
    score += stats["face_count"] * 28.0
    score += min(stats["face_ratio"], 0.18) * 420.0
    score += stats["face_centered"] * 22.0
    score -= stats["dark_ratio"] * 140.0
    score -= stats["bright_ratio"] * 60.0
    return score

def _palette_target_from_selected(selected_stats):
    if not selected_stats:
        return None
    r = sum(s["mean_rgb"][0] for s in selected_stats) / len(selected_stats)
    g = sum(s["mean_rgb"][1] for s in selected_stats) / len(selected_stats)
    b = sum(s["mean_rgb"][2] for s in selected_stats) / len(selected_stats)
    sat = sum(s["avg_sat"] for s in selected_stats) / len(selected_stats)
    val = sum(s["avg_val"] for s in selected_stats) / len(selected_stats)
    return {"rgb": (r, g, b), "sat": sat, "val": val}

def _palette_score(stats, target):
    if not stats or not target:
        return 0.0
    rgb_dist = _rgb_distance(stats["mean_rgb"], target["rgb"])
    sat_dist = abs(stats["avg_sat"] - target["sat"])
    val_dist = abs(stats["avg_val"] - target["val"])
    return -min(rgb_dist, 180.0) * 0.28 - min(sat_dist, 120.0) * 0.22 - min(val_dist, 120.0) * 0.16

def _diversity_penalty(stats, selected_stats):
    if not stats or not selected_stats:
        return 0.0
    penalties = []
    for prev in selected_stats[-4:]:
        rgb_dist = _rgb_distance(stats["mean_rgb"], prev["mean_rgb"])
        sharp_dist = abs(stats["sharpness"] - prev["sharpness"])
        face_dist = abs(stats["face_ratio"] - prev["face_ratio"])
        val_dist = abs(stats["avg_val"] - prev["avg_val"])
        similarity = 0.0
        if rgb_dist < 26:
            similarity += (26 - rgb_dist) * 1.9
        if sharp_dist < 40:
            similarity += (40 - sharp_dist) * 0.18
        if face_dist < 0.018:
            similarity += (0.018 - face_dist) * 1000.0
        if val_dist < 14:
            similarity += (14 - val_dist) * 0.7
        penalties.append(similarity)
    return max(penalties) if penalties else 0.0

def _variety_bonus(stats, selected_stats):
    if not stats or not selected_stats:
        return 0.0
    rgb_dists = [_rgb_distance(stats["mean_rgb"], s["mean_rgb"]) for s in selected_stats[-4:]]
    bonus = min(sum(rgb_dists) / len(rgb_dists), 75.0) * 0.18
    recent_facey = any(s["face_ratio"] > 0.02 for s in selected_stats[-3:])
    this_facey = stats["face_ratio"] > 0.02
    if recent_facey != this_facey:
        bonus += 10.0
    return bonus

def _build_pool(path, tmp, start, end, meta, preview_width, pool_size, fast_mode=False, allow_faces=False, progress=None):
    duration = meta["duration"]
    if duration <= 0:
        return {"frames": [], "meta": meta, "start": start, "end": end}
    force_software = should_force_software_decode(meta)
    s_t = (start / 100.0) * duration
    raw_e_t = (end / 100.0) * duration
    e_t = raw_e_t if fast_mode else detect_effective_end_time(path, meta, s_t, raw_e_t)
    if fast_mode:
        safe_margin = min(8.0, max(0.6, (e_t - s_t) * 0.015))
    else:
        safe_margin = min(0.35, max(0.0, (e_t - s_t) / 20.0))
    safe_start = min(e_t, s_t + safe_margin)
    safe_end = max(safe_start, e_t - safe_margin)
    try:
        stat = os.stat(path)
        cache_basis = f"{os.path.abspath(path)}|{stat.st_size}|{int(stat.st_mtime)}|{start}|{end}|{preview_width}|{pool_size}|v2|{'fast' if fast_mode else 'refined'}"
    except Exception:
        cache_basis = f"{os.path.abspath(path)}|{start}|{end}|{preview_width}|{pool_size}|v2|{'fast' if fast_mode else 'refined'}"
    cache_key = hashlib.sha1(cache_basis.encode("utf-8")).hexdigest()[:16]
    workdir = os.path.join(tmp, "preview_cache", cache_key)
    os.makedirs(workdir, exist_ok=True)
    sample_count = max(10, int(pool_size))
    range_duration = max(0.1, safe_end - safe_start)
    existing = [f for f in os.listdir(workdir) if re.match(r"pool_\d+\.jpg$", f)]
    if len(existing) < sample_count:
        for f in existing:
            try:
                os.remove(os.path.join(workdir, f))
            except Exception:
                pass
        if progress:
            progress("Seeking thumbnails...")
        if fast_mode:
            timestamps = _build_thumbnail_timestamps(safe_start, safe_end, sample_count)
            workers = _worker_count(len(timestamps))
            def extract_one(item):
                idx, ts = item
                out_path = os.path.join(workdir, f"pool_{idx + 1:03d}.jpg")
                fallback_path = None
                fallback_ts = ts
                for attempt_idx, attempt_ts in enumerate(_candidate_timestamps(ts, safe_start, safe_end, idx, sample_count)):
                    attempt_path = os.path.join(workdir, f"pool_{idx + 1:03d}_try_{attempt_idx}.jpg")
                    ok = _extract_single_frame(path, attempt_ts, attempt_path, preview_width, quality=9, force_software=force_software, accurate=False, timeout=6)
                    if not ok or not os.path.exists(attempt_path):
                        continue
                    stats = _analyze_frame(attempt_path, allow_faces=False)
                    if fallback_path is None:
                        fallback_path = attempt_path
                        fallback_ts = attempt_ts
                    if stats and stats["dark_ratio"] <= 0.92 and stats["avg_val"] >= 18:
                        os.replace(attempt_path, out_path)
                        return idx, True, attempt_ts
                if fallback_path and os.path.exists(fallback_path):
                    os.replace(fallback_path, out_path)
                    return idx, True, fallback_ts
                return idx, False, ts
            done = 0
            timestamp_map = {}
            with ThreadPoolExecutor(max_workers=workers) as pool:
                futures = [pool.submit(extract_one, item) for item in enumerate(timestamps)]
                for future in as_completed(futures):
                    done += 1
                    try:
                        idx, ok, actual_ts = future.result()
                        if ok:
                            timestamp_map[str(idx + 1)] = actual_ts
                    except Exception:
                        pass
                    if progress:
                        progress(f"Seeking thumbnails {done}/{len(timestamps)}...")
            try:
                with open(os.path.join(workdir, "timestamps.json"), "w", encoding="utf-8") as f:
                    json.dump(timestamp_map, f)
            except Exception:
                pass
        else:
            if progress:
                progress("Refine: extracting candidate frames...")
            fps = sample_count / range_duration
            pattern = os.path.join(workdir, "pool_%03d.jpg")
            cmd = ["-y", "-ss", str(safe_start), "-t", str(range_duration), "-i", path, "-vf", f"fps={fps:.6f},scale={preview_width}:-1", "-q:v", "5", pattern]
            _run_ffmpeg(cmd, force_software=force_software)
    try:
        with open(os.path.join(workdir, "timestamps.json"), "r", encoding="utf-8") as f:
            timestamp_map = json.load(f)
    except Exception:
        timestamp_map = {}
    frames = []
    frame_files = [f for f in sorted(os.listdir(workdir)) if re.search(r"pool_(\d+)\.jpg$", f)]
    total_files = len(frame_files)
    for done_idx, fname in enumerate(frame_files, start=1):
        if not fname.endswith(".jpg"):
            continue
        m = re.search(r"pool_(\d+)\.jpg$", fname)
        if not m:
            continue
        idx = int(m.group(1)) - 1
        ts = float(timestamp_map.get(str(idx + 1), safe_start + (idx * range_duration / max(1, sample_count - 1))))
        fpath = os.path.join(workdir, fname)
        stats = _analyze_frame(fpath, allow_faces=allow_faces)
        if fast_mode:
            if not stats:
                stats = {
                    "mean_rgb": (0.0, 0.0, 0.0),
                    "avg_sat": 0.0,
                    "avg_val": 0.0,
                    "dark_ratio": 1.0,
                    "bright_ratio": 0.0,
                    "contrast": 0.0,
                    "sharpness": 0.0,
                    "face_count": 0,
                    "face_ratio": 0.0,
                    "face_centered": 0.0,
                }
        else:
            if not stats or not _is_usable_stats(stats):
                continue
        frames.append({"path": fpath, "timestamp": ts, "stats": stats, "base_score": _quality_score(stats)})
        if progress and not fast_mode and (done_idx == total_files or done_idx % 6 == 0):
            progress(f"Refine: analyzing frames {done_idx}/{total_files}...")
    return {"frames": frames, "meta": meta, "start": start, "end": end, "safe_start": safe_start, "safe_end": safe_end}

def build_preview_pool_ultrafast(path, tmp, start=0, end=100, meta=None, target_count=12, progress=None):
    if meta is None:
        meta = get_video_metadata(path)
    if not meta:
        return {"frames": [], "meta": meta, "start": start, "end": end}
    force_software = should_force_software_decode(meta)
    if force_software:
        preview_width = 160
    else:
        preview_width = 200
    pool_size = max(1, int(target_count or 12))
    return _build_pool(path, tmp, start, end, meta, preview_width, pool_size, fast_mode=True, allow_faces=False, progress=progress)

def build_preview_pool_refined(path, tmp, start=0, end=100, meta=None, target_count=12, progress=None):
    if meta is None:
        meta = get_video_metadata(path)
    if not meta:
        return {"frames": [], "meta": meta, "start": start, "end": end}
    force_software = should_force_software_decode(meta)
    preview_width = 190 if force_software else 240
    needed = max(1, int(target_count or 12))
    pool_size = min(40 if force_software else 56, max(needed * 3, 18))
    allow_faces = not force_software
    return _build_pool(path, tmp, start, end, meta, preview_width, pool_size, fast_mode=False, allow_faces=allow_faces, progress=progress)

def select_frames_from_pool_fast(pool, count):
    if not pool or not pool.get("frames") or count <= 0:
        return []
    frames = pool["frames"]
    safe_start = pool.get("safe_start", 0.0)
    safe_end = pool.get("safe_end", 0.0)
    targets = _build_thumbnail_timestamps(safe_start, safe_end, count)
    chosen = []
    used_paths = set()
    for target_ts in targets:
        candidates = [f for f in frames if f["path"] not in used_paths]
        if not candidates:
            candidates = frames
        best = min(candidates, key=lambda f: abs(f["timestamp"] - target_ts))
        used_paths.add(best["path"])
        chosen.append({"path": best["path"], "timestamp": best["timestamp"]})
    return chosen

def select_frames_from_pool_refined(pool, count):
    if not pool or not pool.get("frames") or count <= 0:
        return []
    frames = pool["frames"]
    safe_start = pool.get("safe_start", 0.0)
    safe_end = pool.get("safe_end", 0.0)
    targets = _build_thumbnail_timestamps(safe_start, safe_end, count)
    chosen = []
    selected_stats = []
    locked_palette = None
    used_paths = set()
    for target_ts in targets:
        window = max(0.6, (safe_end - safe_start) / max(count * 2.2, 8))
        candidates = [f for f in frames if f["path"] not in used_paths and abs(f["timestamp"] - target_ts) <= window]
        if not candidates:
            candidates = [f for f in frames if f["path"] not in used_paths]
        palette_target = locked_palette or _palette_target_from_selected(selected_stats)
        best = None
        best_score = -999999999.0
        for cand in candidates:
            total = cand["base_score"]
            total += _palette_score(cand["stats"], palette_target)
            total += _variety_bonus(cand["stats"], selected_stats)
            total -= _diversity_penalty(cand["stats"], selected_stats)
            total -= abs(cand["timestamp"] - target_ts) * 7.0
            if best is None or total > best_score:
                best = cand
                best_score = total
        if best:
            used_paths.add(best["path"])
            chosen.append({"path": best["path"], "timestamp": best["timestamp"]})
            selected_stats.append(best["stats"])
            if locked_palette is None and len(selected_stats) >= min(3, count):
                locked_palette = _palette_target_from_selected(selected_stats)
    return chosen

def extract_final_frames_from_timestamps(path, timestamps, tmp, scale_width=1280, meta=None, progress=None, lossless=False):
    os.makedirs(tmp, exist_ok=True)
    final_dir = os.path.join(tmp, "final_export")
    os.makedirs(final_dir, exist_ok=True)
    if meta is None:
        meta = get_video_metadata(path)
    force_software = should_force_software_decode(meta)
    duration = float((meta or {}).get("duration", 0) or 0)
    workers = _worker_count(len(timestamps))

    def extract_one(item):
        i, ts = item
        out_path = os.path.join(final_dir, f"final_{i:03d}.{'png' if lossless else 'jpg'}")
        try:
            if os.path.exists(out_path):
                os.remove(out_path)
        except Exception:
            pass
        attempts = [ts]
        if duration > 0 and (i == len(timestamps) - 1 or ts >= duration - 1.25):
            attempts += [max(0.0, ts - 0.10), max(0.0, ts - 0.22), max(0.0, ts - 0.40), max(0.0, ts - 0.65), max(0.0, ts - 0.90)]
        else:
            attempts += [max(0.0, ts + 0.08), max(0.0, ts - 0.08), max(0.0, ts + 0.18), max(0.0, ts - 0.18)]
        saved = False
        for attempt_ts in attempts:
            try:
                if os.path.exists(out_path):
                    os.remove(out_path)
            except Exception:
                pass
            try:
                ok = _extract_single_frame(path, attempt_ts, out_path, scale_width, quality=2, force_software=force_software)
            except Exception:
                ok = False
            if not ok or not os.path.exists(out_path):
                continue
            stats = _analyze_frame(out_path, allow_faces=False)
            if stats and stats["dark_ratio"] <= 0.94:
                return i, {"path": out_path, "timestamp": attempt_ts}
        if not saved and os.path.exists(out_path):
            return i, {"path": out_path, "timestamp": ts}
        return i, None

    frames_by_index = {}
    done = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(extract_one, item) for item in enumerate(timestamps)]
        for future in as_completed(futures):
            done += 1
            try:
                idx, frame = future.result()
                if frame:
                    frames_by_index[idx] = frame
            except Exception:
                pass
            if progress:
                progress(done, len(timestamps))
    return [frames_by_index[i] for i in range(len(timestamps)) if i in frames_by_index]

def process_scaling(img, tw, th, mode):
    iw, ih = img.size
    if mode == "Stretch":
        return img.resize((tw, th), Image.Resampling.LANCZOS)
    if mode == "Fit":
        out = img.copy()
        out.thumbnail((tw, th), Image.Resampling.LANCZOS)
        return out
    tar_asp, cur_asp = tw / th, iw / ih
    if cur_asp > tar_asp:
        nw = int(tar_asp * ih)
        off = (iw - nw) // 2
        img = img.crop((off, 0, off + nw, ih))
    else:
        nh = int(iw / tar_asp)
        off = (ih - nh) // 2
        img = img.crop((0, off, iw, off + nh))
    return img.resize((tw, th), Image.Resampling.LANCZOS)

def generate_sheet(frames, meta, out=None, bg=(255, 255, 255), margin=30, cols=4, rows=3, spacing=0, f_size=28, t_pos=(30, 30), g_off=(0, 0), vis=None, f_fam="Arial", tc=None, mode="Fill", output_size=(1920, 1080)):
    if vis is None:
        vis = {}
    if tc is None:
        tc = {"show": True, "size": 24, "opacity": 255, "shadow_show": True, "shadow_opacity": 180}
    W, H = output_size
    scale_factor = W / 1920.0
    margin = int(margin * scale_factor)
    spacing = int(spacing * scale_factor)
    f_size = max(1, int(f_size * scale_factor))
    t_pos = (int(t_pos[0] * scale_factor), int(t_pos[1] * scale_factor))
    g_off = (int(g_off[0] * scale_factor), int(g_off[1] * scale_factor))
    if tc:
        tc = tc.copy()
        tc["size"] = max(1, int(tc.get("size", 24) * scale_factor))
    canvas = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(canvas)

    def get_f(s):
        for p in [f"/Library/Fonts/{f_fam}.ttf", f"/System/Library/Fonts/Supplemental/{f_fam}.ttf", f"/System/Library/Fonts/{f_fam}.ttc", "/Library/Fonts/Arial.ttf"]:
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, s)
                except Exception:
                    pass
        return ImageFont.load_default()

    def get_unicode_f(s, text):
        # If the text contains Arabic/RTL codepoints, force GeezaPro first —
        # it's built into every macOS install and has full Arabic coverage.
        # PingFang (first in the old list) has no Arabic glyphs, so it was
        # the source of the □□ boxes.
        is_arabic = any(0x0600 <= ord(c) <= 0x06FF or 0x0750 <= ord(c) <= 0x077F for c in text)
        priority = []
        if is_arabic:
            priority += [
                "/System/Library/Fonts/GeezaPro.ttc",
                "/System/Library/Fonts/ArabicUI.ttc",
            ]
        priority += [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/Thonburi.ttc",
            "/System/Library/Fonts/Supplemental/Arial Unicode MS.ttf",
            "/Library/Fonts/Arial Unicode MS.ttf",
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simsun.ttc",
            "C:/Windows/Fonts/arial.ttf",
        ]
        needed = {ord(c) for c in text if ord(c) > 127}
        for p in priority:
            if not os.path.exists(p):
                continue
            try:
                from fontTools.ttLib import TTCollection, TTFont
                def check_one(tt):
                    cmap = tt.getBestCmap()
                    return cmap and needed.issubset(cmap.keys())
                if p.lower().endswith(".ttc"):
                    faces = TTCollection(p).fonts
                    # find the specific face index that has the needed glyphs
                    face_idx = next((i for i, f in enumerate(faces) if check_one(f)), None)
                    if face_idx is not None:
                        return ImageFont.truetype(p, s, index=face_idx)
                else:
                    tt = TTFont(p, fontNumber=0, lazy=True)
                    if check_one(tt):
                        return ImageFont.truetype(p, s)
            except Exception:
                continue
        return get_f(s)

    def _needs_unicode(text):
        return any(ord(c) > 127 for c in text)

    def _fix_bidi(text):
        def _bidi_part(s):
            try:
                import arabic_reshaper
                from bidi.algorithm import get_display
                cfg = arabic_reshaper.ArabicReshaper(configuration={
                    'delete_tatweel': True,
                    'support_ligatures': False,
                })
                return get_display(cfg.reshape(s))
            except ImportError:
                # arabic_reshaper not installed — bidi reorder only.
                # PIL does not apply GSUB so letters won't join without reshaping,
                # but at least the string reads in the correct visual direction.
                try:
                    from bidi.algorithm import get_display
                    return get_display(s)
                except Exception:
                    return s[::-1]
            except Exception:
                return s
        # Keep extension on the right in PIL's LTR draw order
        if '.' in text and not text.startswith('.'):
            stem, _, ext = text.rpartition('.')
            return _bidi_part(stem) + '.' + ext
        return _bidi_part(text)

    font = get_f(f_size)
    text_fill = (255, 255, 255) if bg == (0, 0, 0) else (0, 0, 0)
    h = int(meta["duration"] // 3600)
    m = int((meta["duration"] % 3600) // 60)
    s = int(meta["duration"] % 60)
    # (key, label, value) — label is always ASCII, value may be unicode/RTL
    lines = [
        ("name",  "File Name   : ", meta['name']),
        ("size",  "File Size   : ", meta.get('size_display', str(meta.get('size', 0)) + ' MB')),
        ("res",   "Resolution  : ", f"{meta['width']}x{meta['height']} / {meta['fps']} fps"),
        ("dur",   "Duration    : ", f"{h:02}:{m:02}:{s:02}"),
        ("video", "Video       : ", meta.get('video_line', 'Unknown')),
        ("audio", "Audio       : ", meta.get('audio_line', 'Unknown')),
    ]
    tx, ty = t_pos
    for key, label, value in lines:
        if vis.get(key, True):
            if _needs_unicode(value):
                # Reshape/bidi FIRST so get_unicode_f checks the codepoints
                # that will actually be drawn (U+FExx shaped forms), not the
                # original U+06xx codepoints. Mismatch was causing box glyphs.
                shaped_value = _fix_bidi(value)
                label_w = font.getlength(label) if hasattr(font, 'getlength') else draw.textlength(label, font=font)
                draw.text((tx, ty), label, fill=text_fill, font=font)
                uf = get_unicode_f(f_size, shaped_value)
                draw.text((tx + int(label_w), ty), shaped_value, fill=text_fill, font=uf)
            else:
                draw.text((tx, ty), label + value, fill=text_fill, font=font)
            ty += (f_size + 8)
    g_top = max(ty + 20 + g_off[1], 1)
    g_left = max(margin + g_off[0], 1)
    aw, ah = W - (g_left * 2), H - g_top - margin
    tw = max(1, (aw - (spacing * (cols - 1))) // cols)
    th = max(1, (ah - (spacing * (rows - 1))) // rows)
    for i, frame in enumerate(frames[:cols * rows]):
        try:
            img = Image.open(frame["path"]).convert("RGBA")
            img = process_scaling(img, int(tw), int(th), mode)
            if tc.get("show"):
                overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
                d_tc = ImageDraw.Draw(overlay)
                t_f = get_f(tc["size"])
                ts = frame["timestamp"]
                ts_s = f"{int(ts//3600):02}:{int((ts%3600)//60):02}:{int(ts%60):02}"
                if tc.get("shadow_show"):
                    d_tc.text((14, img.height - tc["size"] - 13), ts_s, font=t_f, fill=(0, 0, 0, tc["shadow_opacity"]))
                d_tc.text((12, img.height - tc["size"] - 15), ts_s, font=t_f, fill=(255, 255, 255, tc["opacity"]))
                img = Image.alpha_composite(img, overlay)
            cx = g_left + (i % cols) * (tw + spacing)
            cy = g_top + (i // cols) * (th + spacing)
            canvas.paste(img.convert("RGB"), (int(cx), int(cy)))
        except Exception as e:
            print(f"Error pasting frame {i}: {e}")
    if out:
        canvas.save(out)
    return canvas
