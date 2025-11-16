# news_crawler/spiders/news_spider.py
import json
import re
from datetime import datetime
from urllib.parse import urlparse, urljoin

import scrapy
from scrapy_playwright.page import PageMethod
from dateutil import parser

# Load keywords and sites
with open("keywords.txt", "r", encoding="utf-8") as f:
    KEYWORDS = [line.strip().lower() for line in f if line.strip()]

with open("sites.json", "r", encoding="utf-8") as f:
    SITES = json.load(f).get("sites", [])

def snippet_from_text(text, keyword, radius=120):
    idx = text.lower().find(keyword.lower())
    if idx == -1:
        return text[:radius].strip()
    start = max(0, idx - radius // 2)
    end = min(len(text), idx + radius // 2)
    return ("..." + text[start:end].strip() + "...").replace("\n", " ")

def parse_year(date_str):
    try:
        return parser.parse(date_str, fuzzy=True).year
    except Exception:
        return None

class NewsSpider(scrapy.Spider):
    name = "news"

    custom_settings = {
        "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT": 30000,
        "DOWNLOAD_TIMEOUT": 60,
        "RETRY_TIMES": 3,
        "CONCURRENT_REQUESTS": 4,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "DOWNLOAD_DELAY": 0.5,
        # Block heavy resources to speed up Playwright
        "PLAYWRIGHT_ABORT_REQUEST": "news_crawler.utils.abort_request",
    }

    def start_requests(self):
        for site in SITES:
            if isinstance(site, list):
                site = site[0]
            if not isinstance(site, str) or not site.strip():
                continue

            yield scrapy.Request(
                url=site.strip(),
                callback=self.parse_listing,
                errback=self.handle_error,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_load_state", "domcontentloaded")
                    ],
                    "site_root": site.strip(),
                },
                headers={"User-Agent": self._random_ua()}
            )

    def handle_error(self, failure):
        self.logger.warning(f"Failed to download: {failure.request.url} -> {failure.value}")

    def parse_listing(self, response):
        site_root = response.meta["site_root"]
        anchors = response.css("a::attr(href)").getall()
        links = set()

        for href in anchors:
            if not href:
                continue
            href = urljoin(site_root, href)
            parsed = urlparse(href)
            if parsed.netloc and site_root.replace("https://", "").replace("http://", "") not in parsed.netloc:
                continue
            if re.search(r"/(news|article|story|202[4-5]|202[4-5]/|/202[4-5]-)", href, re.I) \
               or re.search(r"/\d{4}/\d{2}/\d{2}/", href):
                links.add(href)

        if not links:
            for href in anchors[:40]:
                links.add(urljoin(site_root, href))

        for link in links:
            yield scrapy.Request(
                url=link,
                callback=self.parse_article,
                errback=self.handle_error,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_load_state", "domcontentloaded")
                    ],
                    "site_root": site_root
                },
                headers={"User-Agent": self._random_ua()}
            )

    def parse_article(self, response):
        site_root = response.meta["site_root"]
        url = response.url

        # Title extraction
        title = (
            response.css("meta[property='og:title']::attr(content)").get()
            or response.css("title::text").get()
            or response.css("h1::text").get()
        )
        # Date extraction
        date = (
            response.css("meta[property='article:published_time']::attr(content)").get()
            or response.css("meta[name='pubdate']::attr(content)").get()
            or response.css("time::attr(datetime)").get()
            or response.css("time::text").get()
        )

        # Text extraction
        paragraphs = response.css(
            "article p::text, article p *::text, "
            "div[class*='content'] p::text, div[itemprop='articleBody'] p::text, p::text"
        ).getall()
        text = " ".join([p.strip() for p in paragraphs if p and p.strip()])

        if len(text) < 100:
            text = " ".join(response.css("body *::text").getall())[:10000]
        if len(text) < 100:
            return

        # Keyword matching
        lower_text = text.lower()
        matched = {kw for kw in KEYWORDS if kw in lower_text}
        if not matched:
            for kw in KEYWORDS:
                if re.search(rf"\b{re.escape(kw)}\b", lower_text, flags=re.I):
                    matched.add(kw)
        if not matched:
            return

        year = parse_year(date)
        if year not in (2024, 2025):
            return

        snippet = snippet_from_text(text, next(iter(matched)))
        source = urlparse(site_root).netloc.replace("www.", "")

        yield {
            "source": source,
            "url": url,
            "title": title.strip() if title else "",
            "date_published": date.strip() if date else "",
            "matched_keywords": "; ".join(sorted(matched)),
            "snippet": snippet.strip(),
            "scraped_at": datetime.utcnow().isoformat()
        }

    def _random_ua(self):
        import random
        uas = self.settings.get("USER_AGENT_LIST", [])
        if not uas:
            return "Scrapy/Playwright"
        return random.choice(uas)
