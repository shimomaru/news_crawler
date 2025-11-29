BOT_NAME = "news_crawler"

SPIDER_MODULES = ["news_crawler.spiders"]
NEWSPIDER_MODULE = "news_crawler.spiders"

ROBOTSTXT_OBEY = False

# REMOVE ANY GLOBAL PLAYWRIGHT DOWNLOAD HANDLER OVERRIDES!
# Do NOT include: DOWNLOAD_HANDLERS = {...}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

CONCURRENT_REQUESTS = 4
CONCURRENT_REQUESTS_PER_DOMAIN = 2
DOWNLOAD_DELAY = 0.5

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.5
AUTOTHROTTLE_MAX_DELAY = 5
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

RETRY_ENABLED = True
RETRY_TIMES = 2

LOG_LEVEL = "INFO"

COOKIES_ENABLED = False

USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko)"
]

FEEDS = {
    "endsars_oct2020.csv": {
        "format": "csv",
        "overwrite": True,
        "encoding": "utf-8"
    }
}

PLAYWRIGHT_LAUNCH_OPTIONS = {"headless": True}
