#!/usr/bin/env python3
"""Fetch André Ataíde's Medium RSS feed and write the latest posts to
writing/medium-posts.json so the homepage can render LATEST WRITING
dynamically. Python stdlib only."""
import html
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "writing" / "medium-posts.json"

FEED_URL = "https://medium.com/feed/@hadnu"
CONTENT_NS = "http://purl.org/rss/1.0/modules/content/"
MAX_POSTS = 4
EXCERPT_LENGTH = 220
USER_AGENT = "Mozilla/5.0 (hadnu.github.io refresh-medium)"

TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def clean_link(url):
    return url.split("?", 1)[0]


def extract_excerpt(content):
    m = re.search(r"<p>(.*?)</p>", content, re.DOTALL)
    if not m:
        return ""
    text = html.unescape(TAG_RE.sub("", m.group(1)))
    text = WS_RE.sub(" ", text).strip()
    if len(text) <= EXCERPT_LENGTH:
        return text
    return text[:EXCERPT_LENGTH].rsplit(" ", 1)[0] + "…"


def parse_posts(xml_bytes):
    root = ET.fromstring(xml_bytes)
    posts = []
    for item in root.iter("item"):
        title_el = item.find("title")
        link_el = item.find("link")
        date_el = item.find("pubDate")
        content_el = item.find(f"{{{CONTENT_NS}}}encoded")
        if title_el is None or link_el is None or link_el.text is None:
            continue
        title = html.unescape(title_el.text or "").strip()
        if not title:
            continue
        date_label = ""
        date_iso = ""
        if date_el is not None and date_el.text:
            try:
                dt = parsedate_to_datetime(date_el.text)
                date_label = dt.strftime("%b %d, %Y")
                date_iso = dt.astimezone(timezone.utc).strftime("%Y-%m-%d")
            except (TypeError, ValueError):
                pass
        content = (content_el.text or "") if content_el is not None else ""
        posts.append(
            {
                "title": title,
                "url": clean_link(link_el.text),
                "date": date_iso,
                "dateLabel": date_label,
                "excerpt": extract_excerpt(content),
            }
        )
        if len(posts) >= MAX_POSTS:
            break
    return posts


def main():
    try:
        xml_bytes = fetch(FEED_URL)
    except Exception as exc:
        sys.stderr.write(f"failed to fetch feed: {exc}\n")
        return 1

    posts = parse_posts(xml_bytes)
    if not posts:
        sys.stderr.write("no posts parsed from feed\n")
        return 1

    payload = {
        "source": FEED_URL,
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "posts": posts,
    }

    if OUT.exists():
        try:
            previous = json.loads(OUT.read_text())
            if previous.get("posts") == payload["posts"]:
                print("posts unchanged — nothing to write")
                return 0
        except (json.JSONDecodeError, OSError):
            pass

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {len(posts)} posts to {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())