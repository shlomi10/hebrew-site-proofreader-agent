from urllib.parse import urlparse

from playwright.sync_api import sync_playwright


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.rstrip("/") or "/"
    return f"{parsed.scheme}://{parsed.netloc}{path}"


def is_same_domain(base_url: str, candidate_url: str) -> bool:
    return urlparse(base_url).netloc == urlparse(candidate_url).netloc


def extract_visible_text(url: str, timeout_ms: int = 30000) -> str:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
        page.wait_for_timeout(500)
        text = page.evaluate(
            """() => {
                const skip = new Set(['SCRIPT', 'STYLE', 'NOSCRIPT', 'SVG', 'PATH']);
                function visibleText(node) {
                    if (!node) return '';
                    if (node.nodeType === Node.TEXT_NODE) {
                        return node.textContent || '';
                    }
                    if (node.nodeType !== Node.ELEMENT_NODE) return '';
                    const tag = node.tagName;
                    if (skip.has(tag)) return '';
                    const style = window.getComputedStyle(node);
                    if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') {
                        return '';
                    }
                    return Array.from(node.childNodes).map(visibleText).join(' ');
                }
                const bodyText = visibleText(document.body);
                return bodyText.replace(/\\s+/g, ' ').trim();
            }"""
        )
        browser.close()
    return text


def extract_internal_links(url: str, timeout_ms: int = 30000) -> list[str]:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
        hrefs = page.eval_on_selector_all(
            "a[href]",
            """(elements) => elements.map((el) => el.href).filter(Boolean)""",
        )
        browser.close()

    seen: set[str] = set()
    links: list[str] = []
    for href in hrefs:
        if not is_same_domain(url, href):
            continue
        normalized = normalize_url(href)
        if normalized in seen:
            continue
        seen.add(normalized)
        links.append(normalized)
    return links
