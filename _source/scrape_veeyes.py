#!/usr/bin/env python3
"""
Crawl and archive https://www.veeyesdental.com/

What it does
- Starts at the homepage (plus any URLs listed in sitemap.xml)
- Follows every internal link on the same domain (breadth-first)
- Respects robots.txt and waits between requests
- Saves for each page: raw HTML, clean text, title, meta description,
  headings, links, images, phone numbers and emails
- Downloads images, PDFs, CSS and JS found on the site
- Writes a combined pages.json and pages.csv summary

Usage
    pip install requests beautifulsoup4 lxml
    python scrape_veeyes.py                    # full crawl
    python scrape_veeyes.py --max-pages 50     # limit pages
    python scrape_veeyes.py --no-assets        # skip images/PDFs/CSS/JS
    python scrape_veeyes.py --delay 2          # slower, gentler crawl
"""

import argparse
import csv
import hashlib
import json
import os
import re
import time
from collections import deque
from urllib import robotparser
from urllib.parse import urljoin, urlparse, urldefrag

import requests
from bs4 import BeautifulSoup

START_URL = "https://www.veeyesdental.com/"
USER_AGENT = "Mozilla/5.0 (compatible; VeeyesSiteArchiver/1.0)"
ASSET_EXTS = (
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".ico",
    ".pdf", ".css", ".js", ".woff", ".woff2", ".ttf", ".mp4", ".webm",
)
SKIP_EXTS = (".zip", ".rar", ".exe", ".dmg", ".mp3")
PHONE_RE = re.compile(r"(?:\+?91[\s-]?)?(?:\(?0?\d{2,4}\)?[\s-]?)?\d{3,5}[\s-]?\d{4,6}")
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")


def normalize(url: str) -> str:
    """Strip fragments and trailing slashes so duplicates collapse."""
    url, _ = urldefrag(url)
    p = urlparse(url)
    path = p.path or "/"
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    return f"{p.scheme}://{p.netloc.lower()}{path}" + (f"?{p.query}" if p.query else "")


def same_site(url: str, root_host: str) -> bool:
    host = urlparse(url).netloc.lower()
    return host == root_host or host == root_host.replace("www.", "") or host == "www." + root_host


def safe_filename(url: str, ext: str = "") -> str:
    p = urlparse(url)
    path = p.path.strip("/") or "index"
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", path)[:120]
    if p.query:
        name += "_" + hashlib.md5(p.query.encode()).hexdigest()[:8]
    if ext and not name.endswith(ext):
        name += ext
    return name


class Scraper:
    def __init__(self, start_url, out_dir, delay, max_pages, get_assets):
        self.start_url = normalize(start_url)
        self.root_host = urlparse(self.start_url).netloc.lower()
        self.out_dir = out_dir
        self.delay = delay
        self.max_pages = max_pages
        self.get_assets = get_assets

        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})

        self.robots = robotparser.RobotFileParser()
        self.robots.set_url(urljoin(self.start_url, "/robots.txt"))
        try:
            self.robots.read()
        except Exception:
            self.robots = None

        self.queue = deque([self.start_url])
        self.seen = {self.start_url}
        self.assets = set()
        self.pages = []

        for sub in ("html", "text", "assets"):
            os.makedirs(os.path.join(out_dir, sub), exist_ok=True)

    # ---------- helpers ----------
    def allowed(self, url):
        return self.robots is None or self.robots.can_fetch(USER_AGENT, url)

    def fetch(self, url, stream=False):
        for attempt in range(3):
            try:
                r = self.session.get(url, timeout=20, stream=stream)
                if r.status_code == 429:
                    time.sleep(10 * (attempt + 1))
                    continue
                return r
            except requests.RequestException as e:
                print(f"   ! {e} (attempt {attempt + 1})")
                time.sleep(3)
        return None

    def enqueue(self, url):
        url = normalize(url)
        if url in self.seen or not same_site(url, self.root_host):
            return
        if url.lower().endswith(SKIP_EXTS):
            return
        if url.lower().endswith(ASSET_EXTS):
            self.assets.add(url)
            return
        self.seen.add(url)
        self.queue.append(url)

    def load_sitemap(self):
        for path in ("/sitemap.xml", "/sitemap_index.xml", "/wp-sitemap.xml"):
            r = self.fetch(urljoin(self.start_url, path))
            if not r or r.status_code != 200:
                continue
            locs = re.findall(r"<loc>\s*(.*?)\s*</loc>", r.text)
            for loc in locs:
                if loc.endswith(".xml"):  # nested sitemap
                    sub = self.fetch(loc)
                    if sub and sub.status_code == 200:
                        for l2 in re.findall(r"<loc>\s*(.*?)\s*</loc>", sub.text):
                            self.enqueue(l2)
                else:
                    self.enqueue(loc)
            print(f"Loaded {len(locs)} entries from {path}")

    # ---------- page parsing ----------
    def parse(self, url, html):
        soup = BeautifulSoup(html, "lxml")

        # collect links and assets before stripping tags
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if href.startswith(("mailto:", "tel:", "javascript:", "whatsapp:")):
                links.append(href)
                continue
            full = urljoin(url, href)
            links.append(full)
            self.enqueue(full)

        images = []
        for img in soup.find_all("img"):
            src = img.get("src") or img.get("data-src") or img.get("data-lazy-src")
            if src:
                full = urljoin(url, src)
                images.append({"src": full, "alt": img.get("alt", "")})
                if same_site(full, self.root_host):
                    self.assets.add(full)
        for tag, attr in (("link", "href"), ("script", "src"), ("source", "src")):
            for t in soup.find_all(tag):
                v = t.get(attr)
                if v:
                    full = urljoin(url, v)
                    if same_site(full, self.root_host) and full.lower().split("?")[0].endswith(ASSET_EXTS):
                        self.assets.add(full)

        title = soup.title.get_text(strip=True) if soup.title else ""
        meta = soup.find("meta", attrs={"name": "description"})
        description = meta.get("content", "") if meta else ""
        headings = {
            h: [x.get_text(" ", strip=True) for x in soup.find_all(h)]
            for h in ("h1", "h2", "h3")
        }

        for t in soup(["script", "style", "noscript", "svg", "iframe"]):
            t.decompose()
        text = soup.get_text("\n", strip=True)
        text = re.sub(r"\n{3,}", "\n\n", text)

        phones = sorted({p.strip() for p in PHONE_RE.findall(text) if len(re.sub(r"\D", "", p)) >= 10})
        emails = sorted(set(EMAIL_RE.findall(text)))

        return {
            "url": url,
            "title": title,
            "meta_description": description,
            "headings": headings,
            "phones": phones,
            "emails": emails,
            "images": images,
            "links": sorted(set(links)),
            "word_count": len(text.split()),
            "text": text,
        }

    # ---------- main loop ----------
    def crawl(self):
        self.load_sitemap()
        while self.queue and (self.max_pages is None or len(self.pages) < self.max_pages):
            url = self.queue.popleft()
            if not self.allowed(url):
                print(f"[robots] skip {url}")
                continue
            print(f"[{len(self.pages) + 1}] {url}")
            r = self.fetch(url)
            time.sleep(self.delay)
            if not r or r.status_code != 200:
                print(f"   ! status {getattr(r, 'status_code', 'none')}")
                continue
            if "text/html" not in r.headers.get("Content-Type", ""):
                self.assets.add(url)
                continue

            # redirects may land on a new URL
            final = normalize(r.url)
            if final != url and final in {p["url"] for p in self.pages}:
                continue

            data = self.parse(final, r.text)
            base = safe_filename(final)
            with open(os.path.join(self.out_dir, "html", base + ".html"), "w", encoding="utf-8") as f:
                f.write(r.text)
            with open(os.path.join(self.out_dir, "text", base + ".txt"), "w", encoding="utf-8") as f:
                f.write(f"URL: {final}\nTITLE: {data['title']}\n\n{data['text']}")
            self.pages.append(data)

        if self.get_assets:
            self.download_assets()
        self.write_outputs()

    def download_assets(self):
        print(f"\nDownloading {len(self.assets)} assets...")
        for i, url in enumerate(sorted(self.assets), 1):
            if not self.allowed(url):
                continue
            p = urlparse(url)
            rel = p.path.lstrip("/") or "index"
            dest = os.path.join(self.out_dir, "assets", *rel.split("/"))
            if os.path.exists(dest):
                continue
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            r = self.fetch(url, stream=True)
            if r and r.status_code == 200:
                with open(dest, "wb") as f:
                    for chunk in r.iter_content(8192):
                        f.write(chunk)
                print(f"  [{i}] {rel}")
            time.sleep(self.delay / 2)

    def write_outputs(self):
        with open(os.path.join(self.out_dir, "pages.json"), "w", encoding="utf-8") as f:
            json.dump(self.pages, f, ensure_ascii=False, indent=2)
        with open(os.path.join(self.out_dir, "pages.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["url", "title", "meta_description", "h1", "phones", "emails", "word_count"])
            for p in self.pages:
                w.writerow([
                    p["url"], p["title"], p["meta_description"],
                    " | ".join(p["headings"]["h1"]),
                    " | ".join(p["phones"]), " | ".join(p["emails"]),
                    p["word_count"],
                ])
        print(f"\nDone. {len(self.pages)} pages, {len(self.assets)} assets -> {self.out_dir}/")


def main():
    ap = argparse.ArgumentParser(description="Archive veeyesdental.com")
    ap.add_argument("--url", default=START_URL)
    ap.add_argument("--out", default="veeyes_site")
    ap.add_argument("--delay", type=float, default=1.0, help="seconds between requests")
    ap.add_argument("--max-pages", type=int, default=None)
    ap.add_argument("--no-assets", action="store_true")
    a = ap.parse_args()
    Scraper(a.url, a.out, a.delay, a.max_pages, not a.no_assets).crawl()


if __name__ == "__main__":
    main()
