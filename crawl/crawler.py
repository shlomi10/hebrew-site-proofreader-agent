import time
from collections import deque
from urllib.parse import urlparse

from config import CRAWL_DELAY_SECONDS, MAX_PAGES
from crawl.extractor import (
    extract_internal_links,
    extract_visible_text,
    is_same_domain,
    normalize_url,
)


def crawl_site(start_url: str, max_pages: int = MAX_PAGES) -> dict[str, str]:
    start_url = normalize_url(start_url)
    if not urlparse(start_url).scheme:
        start_url = f"https://{start_url}"

    queue: deque[str] = deque([start_url])
    visited: set[str] = set()
    pages: dict[str, str] = {}

    while queue and len(pages) < max_pages:
        url = queue.popleft()
        if url in visited:
            continue
        visited.add(url)

        try:
            text = extract_visible_text(url)
            pages[url] = text
            for link in extract_internal_links(url):
                if link not in visited and is_same_domain(start_url, link):
                    queue.append(link)
        except Exception as exc:
            pages[url] = f"[ERROR] {exc}"

        if CRAWL_DELAY_SECONDS:
            time.sleep(CRAWL_DELAY_SECONDS)

    return pages
