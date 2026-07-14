"""Pre-bundle pygbag runtime CDN assets locally.

Pygbag 0.9.2's built index.html fetches runtime files at:
    https://pygame-web.github.io/archives/0.9/pythons.js
    https://pygame-web.github.io/archives/0.9//browserfs.min.js (note double slash bug)
    https://pygame-web.github.io/archives/0.9/empty.html
    https://pygame-web.github.io/archives/0.9/pythonrc.py
    https://pygame-web.github.io/archives/0.9/vt/xterm.js
    https://pygame-web.github.io/archives/0.9/vt/xterm-addon-image.js

We download each asset into the bundle (preserving the 'vt/' subdirectory),
rewrite every <script src> / <link href> to point at the local copy,
and convert any double-slash variant to a clean ./ path.
"""
import glob
import os
import re
import sys
import urllib.error
import urllib.request

INDEX_PATH = "build/web/index.html"
ASSET_DIR = "build/web"

# Match the full CDN pattern pygbag uses
CDN_RE = re.compile(
    r"https?://pygame-web\.github\.io/archives/0\.9/[^\"' )]+"
)


def fetch(url, dest):
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


def normalize_url(url):
    """Collapse any doubled slashes after archives/0.9/. The 0.9.x pygbag
    emits 'archives/0.9//browserfs.min.js' but the CDN serves it as
    'archives/0.9/browserfs.min.js'."""
    return re.sub(r"(/archives/0\.9)/+", r"\1/", url)


def main():
    if not os.path.isfile(INDEX_PATH):
        print(f"ERROR: {INDEX_PATH} not found.")
        print("Run 'pygbag --build .' first, then re-run this script.")
        sys.exit(1)

    with open(INDEX_PATH, encoding="utf-8") as fp:
        html = fp.read()

    raw_urls = sorted(set(CDN_RE.findall(html)))
    urls = sorted(set(normalize_url(u) for u in raw_urls))

    if not urls:
        print("No pygbag archive URLs found in index.html — clean.")
    else:
        print(f"Found {len(urls)} pygbag archive URL(s):")
        for u in urls:
            print(f"  {u}")

        for url in urls:
            suffix = url.split("/archives/0.9/", 1)[1]
            asset_rel = suffix
            dest = os.path.join(ASSET_DIR, asset_rel)

            downloaded = True
            if not os.path.exists(dest) or os.path.getsize(dest) == 0:
                if not fetch(url, dest):
                    # Don't bail — write a placeholder so the browser doesn't
                    # 404-stall the splash while waiting on a missing remote.
                    downloaded = False
                    try:
                        os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
                        with open(dest, "w", encoding="utf-8") as fp:
                            fp.write("# placeholder\n")
                        print(f"    wrote placeholder to {dest}")
                    except OSError as exc:
                        print(f"    could not create placeholder: {exc}")

            with open(INDEX_PATH, encoding="utf-8") as fp:
                html = fp.read()
            local_path = "./" + asset_rel
            new_html = html
            new_html = new_html.replace(url, local_path)
            for u0 in raw_urls:
                if normalize_url(u0) == url:
                    new_html = new_html.replace(u0, local_path)

            if new_html != html:
                with open(INDEX_PATH, "w", encoding="utf-8") as fp:
                    fp.write(new_html)
                tag = "rewrote" if downloaded else "rewrote (placeholder)"
                print(f"  {tag} -> {local_path}")

    # Final report — exit 0; the workflow has its own check for CDN residues.
    with open(INDEX_PATH, encoding="utf-8") as fp:
        html = fp.read()
    remaining_norm = sorted(set(normalize_url(u) for u in CDN_RE.findall(html)))
    print(f"\nRemaining CDN refs in {INDEX_PATH}:")
    if remaining_norm:
        for r in remaining_norm:
            print(f"  {r}")
    else:
        print("  (none)")



if __name__ == "__main__":
    main()
