#!/usr/bin/env python3
"""
Download every remote image and video this site uses (Wix CDN photos, the logo,
Mixkit stock videos) into assets/media/ and rewrite the HTML to use the local copies.

Run this once before you deploy, because the Wix CDN links stop working when the
Wix site is closed:

    python localize_media.py

Needs Python 3.8+ only (no extra packages). It's safe to run more than once.
"""
import hashlib, os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
MEDIA = os.path.join(ROOT, "assets", "media")
PAT = re.compile(r'https://(?:static\.wixstatic\.com|assets\.mixkit\.co|videos\.pexels\.com|images\.pexels\.com)/[^"\'\s)<>]+')

def local_name(url):
    ext = ".mp4" if url.endswith(".mp4") else (".png" if url.endswith(".png") else ".jpg")
    stem = re.sub(r"[^a-z0-9]+", "-", url.split("/media/")[-1].split("~")[0].lower())[:40] if "wixstatic" in url else url.rsplit("/", 1)[-1].rsplit(".", 1)[0][:40]
    return f"{stem}-{hashlib.md5(url.encode()).hexdigest()[:6]}{ext}"

def main():
    os.makedirs(MEDIA, exist_ok=True)
    html_files = [os.path.join(d, f) for d, _, fs in os.walk(ROOT) if "_source" not in d for f in fs if f.endswith(".html")]
    urls = set()
    for p in html_files:
        urls.update(PAT.findall(open(p, encoding="utf-8").read()))
    print(f"{len(urls)} remote files found")
    done = {}
    for i, u in enumerate(sorted(urls), 1):
        name = local_name(u)
        dest = os.path.join(MEDIA, name)
        if not os.path.exists(dest):
            try:
                req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
                    f.write(r.read())
                print(f"[{i}] saved {name}")
            except Exception as e:
                print(f"[{i}] FAILED {u}: {e}", file=sys.stderr)
                continue
        done[u] = name
    for p in html_files:
        depth = os.path.relpath(p, ROOT).count(os.sep)
        prefix = "../" * depth + "assets/media/"
        s = open(p, encoding="utf-8").read()
        for u, name in done.items():
            s = s.replace(u, prefix + name)
        open(p, "w", encoding="utf-8").write(s)
    print(f"Done. {len(done)} files in assets/media, {len(html_files)} pages updated.")
    print("Note: og:image tags now use relative paths; change them to full https:// URLs after deploying.")

if __name__ == "__main__":
    main()
