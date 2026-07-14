"""Mirror pygbag 0.9.2 runtime CDN assets locally.

Memory anchor: 'download missing CDN files into the project root and patch
the template index.html script src tags to point at local files. Pattern:
search the template index.html for any <script src> or <link href>
pointing to pygame-web.github.io/cdn and replace with relative paths.'

Behavior:
- Only rewrite URLs that point at pygame-web.github.io (the CDN host).
- Collapse double slashes first — pygbag 0.9.x emits 'archives/0.9//...'.
- Always write under ASSET_DIR, never an absolute path.
- If a file 404s on raw.githubusercontent.com, skip its rewrite (don't
  introduce a placeholder; the runtime reference is decorative).
"""
import os
import re
import sys
import urllib.error
import urllib.request

INDEX_PATH = "build/web/index.html"
ASSET_DIR = "build/web"
RAW_BASE = "https://raw.githubusercontent.com/pygame-web/archives/main/0.9"

# Match URLs inside <script src="...">, <link href="...">, or import("...").
ATTR_CONTEXT = re.compile(
    r"""(?:<script[^>]*?\bsrc\s*=\s*['"]|<link[^>]*?\bhref\s*=\s*['"]|import\s*\(\s*['"])([^'"]+)['"]""",
    re.VERBOSE | re.DOTALL,
)

# Only operate on URLs pointing at the pygbag CDN host.
CDN_HOST = "pygame-web.github.io"

# Split a CDN URL on either 'archives/<ver>/' or 'cdn/<ver>/'.
CDN_SPLIT = re.compile(r"/(?:archives|cdn)/[^/]+/")


def is_cdn_url(url):
    """Return True only if the URL points at the pygbag CDN host."""
    return CDN_HOST in url


def normalize_doubleslashes(url):
    """Collapse the doubled slashes that 0.9.x emits — e.g.
       'archives/0.9//browserfs.min.js' -> 'archives/0.9/browserfs.min.js'."""
    return re.sub(r"/+", "/", url)


def strip_query_anchor(url):
    return url.split("?", 1)[0].split("#", 1)[0]


def safe_rel_path(rel):
    if not rel:
        return None
    if rel.startswith("/") or os.path.isabs(rel) or rel in (".", ".."):
        return None
    return rel


def rel_from_cdn(url):
    """Map '...archives/0.9/vt/xterm.js' -> 'vt/xterm.js'.
       Also handles '...archives/0.9//browserfs.min.js' (double-slash)."""
    url = strip_query_anchor(url)
    url = normalize_doubleslashes(url)
    parts = CDN_SPLIT.split(url, maxsplit=1)
    if len(parts) != 2:
        return None
    rel = parts[1].strip("/")
    return safe_rel_path(rel)


def fetch(url, dest):
    try:
        parent = os.path.dirname(dest)
        if parent:
            os.makedirs(parent, exist_ok=True)
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


def main():
    if not os.path.isfile(INDEX_PATH):
        print(f"ERROR: {INDEX_PATH} not found.")
        print("Run 'pygbag --build .' first, then re-run this script.")
        sys.exit(1)

    with open(INDEX_PATH, encoding="utf-8") as fp:
        html = fp.read()

    attr_urls = sorted(set(ATTR_CONTEXT.findall(html)))
    if not attr_urls:
        print("No CDN URLs in <script src>/<link href>/import() — clean.")
        return

    # Filter: only CDN-host URLs. Drop things like 'favicon.png' that
    # are already local.
    cdn_urls = [u for u in attr_urls if is_cdn_url(u)]
    skipped_local = [u for u in attr_urls if not is_cdn_url(u)]
    if skipped_local:
        for u in skipped_local:
            print(f"  already-local (skipping): {u}")

    if not cdn_urls:
        print("\nNo CDN URLs to rewrite — clean.")
        return

    print(f"\nFound {len(cdn_urls)} CDN attribute URL(s):")
    for u in cdn_urls:
        print(f"  {u}")

    rewrote = 0
    for url in cdn_urls:
        rel = rel_from_cdn(url)
        if not rel:
            print(f"  skipping (not a file ref): {url}")
            continue

        dest = os.path.join(ASSET_DIR, rel)
        if os.path.isabs(dest) or not dest.startswith(
            os.path.abspath(ASSET_DIR) + os.sep
        ):
            print(f"  skipping (refuses to write outside bundle): {rel}")
            continue

        if not os.path.isfile(dest) or os.path.getsize(dest) == 0:
            if not fetch(f"{RAW_BASE}/{rel}", dest):
                print(f"  leaving URL unrewritten (CDN 4xx): {url}")
                continue

        with open(INDEX_PATH, encoding="utf-8") as fp:
            html = fp.read()
        local_path = "./" + rel
        new_html = html.replace(url, local_path)
        if new_html != html:
            with open(INDEX_PATH, "w", encoding="utf-8") as fp:
                fp.write(new_html)
            print(f"  rewrote -> {local_path}")
            rewrote += 1

    with open(INDEX_PATH, encoding="utf-8") as fp:
        html = fp.read()
    remaining = sorted(set(u for u in ATTR_CONTEXT.findall(html) if is_cdn_url(u)))
    print(f"\n{rewrote} URL(s) rewritten. Remaining CDN attribute refs:")
    if remaining:
        for r in remaining:
            print(f"  {r}")
    else:
        print("  (none)")


if __name__ == "__main__":
    main()
