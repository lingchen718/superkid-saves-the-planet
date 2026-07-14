"""Pre-bundle pygbag CDN runtime assets locally.

Pygbag 0.9.2's built index.html references these at runtime:
    https://pygame-web.github.io/archives/0.9/pythons.js
    https://pygame-web.github.io/archives/0.9/browserfs.min.js
    https://pygame-web.github.io/archives/0.9/empty.html
    https://pygame-web.github.io/archives/0.9/pythonrc.py
    https://pygame-web.github.io/archives/0.9/vt/xterm.js
    https://pygame-web.github.io/archives/0.9/vt/xterm-addon-image.js

We download each into the bundle (preserving the 'vt/' subdirectory)
and rewrite every <script src> / <link href> to point at the local copy.
"""
import glob
import os
import re
import sys
import urllib.error
import urllib.request

INDEX_PATH = "build/web/index.html"
CDN_RE = re.compile(r"https?://pygame-web\.github\.io/archives/0\.9/[^\"' )]+")


def fetch(url, dest):
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            data = r.read()
        os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
        with open(dest, "wb") as fp:
            fp.write(data)
        print(f"  fetched {dest} ({len(data):,} bytes)")
        return True
    except (urllib.error.URLError, urllib.error.HTTPError,
            TimeoutError, OSError) as exc:
        print(f"  FAILED {url}: {exc}")
        return False


def normalize_double_slash(url):
    """Fix pygbag's accidental double-slash (e.g. archives/0.9//browserfs)."""
    return re.sub(r"(archives/0\.9)/+", r"\1/", url)


def main():
    if not os.path.isfile(INDEX_PATH):
        print(f"{INDEX_PATH} not found. Run 'pygbag --build .' first.")
        sys.exit(1)

    with open(INDEX_PATH, encoding="utf-8") as fp:
        html = fp.read()

    raw_urls = sorted(set(CDN_RE.findall(html)))
    urls = sorted(set(normalize_double_slash(u) for u in raw_urls))

    if not urls:
        print("No CDN URLs in built index.html — clean.")
    else:
        print(f"Found {len(urls)} pygbag archive URL(s):")
        for u in urls:
            print(f"  {u}")

        for url in urls:
            # e.g. https://pygame-web.github.io/archives/0.9/vt/xterm.js
            #   -> ./vt/xterm.js
            suffix = url.split("/archives/0.9/", 1)[1]
            asset_rel = suffix  # 'browserfs.min.js' or 'vt/xterm.js'
            dest = os.path.join("build/web", asset_rel)

            if not os.path.exists(dest) or os.path.getsize(dest) == 0:
                if not fetch(url, dest):
                    continue

            with open(INDEX_PATH, encoding="utf-8") as fp:
                html = fp.read()
            local_path = "./" + asset_rel
            new_html = html.replace(url, local_path)
            # Also handle the original double-slash variant if present
            for u0 in raw_urls:
                if normalize_double_slash(u0) == url:
                    new_html = new_html.replace(u0, local_path)

            if new_html != html:
                with open(INDEX_PATH, "w", encoding="utf-8") as fp:
                    fp.write(new_html)
                print(f"  rewrote {url} -> {local_path}")

    # Strip stale APK (memory: APK path abandoned)
    for stale in glob.glob("build/web/*.apk"):
        os.remove(stale)
        print(f"  stripped APK: {stale}")

    with open(INDEX_PATH, encoding="utf-8") as fp:
        html = fp.read()
    remaining = CDN_RE.findall(html)
    print(f"\nRemaining CDN refs in {INDEX_PATH}:")
    if remaining:
        for r in remaining:
            print(f"  {r}")
    else:
        print("  (none)")


if __name__ == "__main__":
    main()
