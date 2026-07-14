"""Mirror pygbag runtime CDN assets locally from the GitHub raw archive.

The dev pygbag (0.9.4) ships no runtime assets in the Python package —
the runtime is served from pygame-web.github.io/archives/0.9/ at iPad
boot, but the GitHub Pages URLs intermittently return 'Connection reset
by peer' or 404 errors. The raw.githubusercontent.com URLs return 200
reliably for every file. We mirror from raw.githubusercontent.com and
rewrite index.html to use only ./ relative paths.

Memory anchor: 'download missing CDN files into the project root and patch
the template index.html script src tags to point at local files. Pattern:
search the template index.html for any <script src> or <link href>
pointing to pygame-web.github.io/cdn and replace with relative paths.'
"""
import glob
import os
import re
import sys
import urllib.error
import urllib.request

INDEX_PATH = "build/web/index.html"
ASSET_DIR = "build/web"
RAW_BASE = "https://raw.githubusercontent.com/pygame-web/archives/main/0.9"

# Match any pygbag archive URL — handles 0.9, 0.10, etc. consistently.
CDN_RE = re.compile(r"https?://pygame-web\.github\.io/archives/[0-9.]+/[^\"' )]+")


def normalize_url(url):
    """Collapse any doubled slashes after archives/0.9/ (the 0.9.x bug)."""
    return re.sub(r"(/archives/[0-9.]+)/+", r"\1/", url)


def rel_from_cdn(url):
    """Extract the relative path inside 'archives/X.Y/...', e.g. 'vt/vtx.js'."""
    parts = re.split(r"/archives/[0-9.]+/", url, maxsplit=1)
    if len(parts) != 2:
        return None
    rel = parts[1]
    rel = re.sub(r"/+", "/", rel)
    return rel


def fetch(url, dest):
    """Fetch url to dest, creating parent dirs. Returns True on success."""
    try:
        os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
        with urllib.request.urlopen(url, timeout=30) as r:
            data = r.read()
        with open(dest, "wb") as fp:
            fp.write(data)
        print(f"  fetched {dest} ({len(data):,} bytes)")
        return True
    except (urllib.error.URLError, urllib.error.HTTPError,
            TimeoutError, OSError) as exc:
        print(f"  FAILED {url}: {exc}")
        return False


def safe_fetch(rel):
    """Mirror a file from the raw archive (relative path)."""
    if not rel:
        return False
    src = f"{RAW_BASE}/{rel}"
    dest = os.path.join(ASSET_DIR, rel)
    return fetch(src, dest)


def main():
    if not os.path.isfile(INDEX_PATH):
        print(f"ERROR: {INDEX_PATH} not found.")
        print("Run 'pygbag --build .' first, then re-run this script.")
        sys.exit(1)

    with open(INDEX_PATH, encoding="utf-8") as fp:
        html = fp.read()

    # ── Pass 1: rewrite every CDN URL referenced in index.html ──
    raw_urls = sorted(set(CDN_RE.findall(html)))
    urls = sorted(set(normalize_url(u) for u in raw_urls))

    if not urls:
        print("No CDN URLs found in index.html.")
    else:
        print(f"Found {len(urls)} pygbag archive URL(s):")
        for u in urls:
            print(f"  {u}")
        for url in urls:
            rel = rel_from_cdn(normalize_url(url))
            if not rel:
                continue
            dest = os.path.join(ASSET_DIR, rel)
            if not os.path.exists(dest) or os.path.getsize(dest) == 0:
                if not safe_fetch(rel):
                    os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
                    with open(dest, "w", encoding="utf-8") as fp:
                        fp.write("// placeholder\n")
                    print(f"    wrote placeholder: {dest}")

            with open(INDEX_PATH, encoding="utf-8") as fp:
                html = fp.read()
            local_path = "./" + rel
            new_html = html.replace(url, local_path)
            for u0 in raw_urls:
                if normalize_url(u0) == url:
                    new_html = new_html.replace(u0, local_path)
            if new_html != html:
                with open(INDEX_PATH, "w", encoding="utf-8") as fp:
                    fp.write(new_html)
                print(f"  rewrote -> {local_path}")

    # ── Pass 2: pre-mirror known transitive runtime deps ──
    # The iPad's browser pulls these dynamically via ES module imports.
    transitive = [
        "vtx.js",
        "browserfs.min.js",
        "pythons.js",
        "empty.html",
        "pythonrc.py",
        "cpythonrc.py",
        "banner.png",
        "bind.c",
        "bind.js",
        "vt/vtx.js",
        "vt/xterm.js",
        "vt/xterm.css",
        "vt/xterm-addon-image.js",
        "vt/xterm-addon-fit.js",
        "vt/xterm-addon-web-links.js",
    ]
    print(f"\nPre-mirroring {len(transitive)} transitive dep(s):")
    for rel in transitive:
        dest = os.path.join(ASSET_DIR, rel)
        if os.path.isfile(dest) and os.path.getsize(dest) > 0:
            continue
        if safe_fetch(rel):
            print(f"  mirrored {rel}")
        else:
            os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
            with open(dest, "w", encoding="utf-8") as fp:
                fp.write("// placeholder\n")
            print(f"  wrote placeholder: {dest}")

    # ── Final report ──
    with open(INDEX_PATH, encoding="utf-8") as fp:
        html = fp.read()
    remaining = sorted(set(CDN_RE.findall(html)))
    print(f"\nRemaining CDN refs in {INDEX_PATH}:")
    if remaining:
        for r in remaining:
            print(f"  {r}")
    else:
        print("  (none)")


if __name__ == "__main__":
    main()
