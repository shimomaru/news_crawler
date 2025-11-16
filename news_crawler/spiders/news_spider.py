import scrapy
from scrapy_playwright.page import PageMethod

class VanguardSpider(scrapy.Spider):
    name = "vanguard"
    start_urls = ["https://www.vanguardngr.com/search/endsars/"]

    custom_settings = {
        "FEEDS": {"vanguard_articles.csv": {"format": "csv"}},
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36",
        "CONCURRENT_REQUESTS": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 1,
        "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": True},
        "RETRY_ENABLED": True,
        "RETRY_TIMES": 5,
        "LOG_LEVEL": "INFO",
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", "article.entry.entry-list-large")
                    ],
                    "page_count": 1
                }
            )

    def parse(self, response):
        for article in response.css("article.entry.entry-list-large"):
            yield {
                "title": article.css("h3.entry-title a::text").get(),
                "link": article.css("h3.entry-title a::attr(href)").get(),
                "date": article.css("div.entry-date::text").get(),
            }

        # Pagination
        page_count = response.meta.get("page_count", 1)
        if page_count < 10:
            next_page = response.css("div.pagination__next a::attr(href)").get()
            if next_page:
                yield scrapy.Request(
                    next_page,
                    callback=self.parse,
                    meta={
                        "playwright": True,
                        "playwright_page_methods": [
                            PageMethod("wait_for_selector", "article.entry.entry-list-large")
                        ],
                        "page_count": page_count + 1
                    }
                )
