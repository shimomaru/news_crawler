# news_crawler/settings.py
BOT_NAME = "news_crawler"

SPIDER_MODULES = ["news_crawler.spiders"]
NEWSPIDER_MODULE = "news_crawler.spiders"

# Disable robots.txt for news crawling (enable only if required)
ROBOTSTXT_OBEY = False

# Playwright download handler
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Abort useless resources to reduce 70% page load cost
PLAYWRIGHT_ABORT_REQUEST = "news_crawler.utils.abort_request"

# Resource timeouts (critical)
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 60000     # 60 sec
PLAYWRIGHT_DEFAULT_PAGE_TIMEOUT = 60000

# Concurrency (safe for Playwright)
CONCURRENT_REQUESTS = 4
CONCURRENT_REQUESTS_PER_DOMAIN = 2
DOWNLOAD_DELAY = 0.5

# Playwright resource limits
PLAYWRIGHT_MAX_CONTEXTS = 1
PLAYWRIGHT_MAX_PAGES_PER_CONTEXT = 1

# AutoThrottle (keeps sites happy)
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.5
AUTOTHROTTLE_MAX_DELAY = 5
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# Retry
RETRY_ENABLED = True
RETRY_TIMES = 2

# Logging
LOG_LEVEL = "INFO"

# Disable cookies (scrapy & playwright)
COOKIES_ENABLED = False

# User agent rotation
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko)"
]

# Feed export (corrected; no flush issue)
FEEDS = {
    "results.jl": {
        "format": "jsonlines",
        "overwrite": True,
        "encoding": "utf-8",
    }
}

PLAYWRIGHT_LAUNCH_OPTIONS = {"headless": True}
