# import scrapy
# from scrapy_playwright.page import PageMethod

# class VanguardOct2020EndSARSSpider(scrapy.Spider):
#     name = "vanguard_oct2020_endsars"
#     allowed_domains = ["vanguardngr.com"]
#     archive_base = "https://www.vanguardngr.com/2020/10/page/{page_num}/"
#     max_page = 237  # as you observed

#     custom_settings = {
#         "FEEDS": {
#             "vanguard_2020_10_endsars.csv": {
#                 "format": "csv",
#                 "encoding": "utf-8",
#                 "fields": ["title", "url", "date", "snippet"]
#             }
#         },
#         "DOWNLOAD_HANDLERS": {
#             "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
#             "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
#         },
#         "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
#         "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                       "AppleWebKit/537.36 (KHTML, like Gecko) "
#                       "Chrome/120.0.0.0 Safari/537.36",
#         "CONCURRENT_REQUESTS": 1,
#         "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
#         "DOWNLOAD_DELAY": 0.5,
#         "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": True},
#         # Retry settings (optional)
#         "RETRY_ENABLED": True,
#         "RETRY_TIMES": 3,
#     }

#     def start_requests(self):
#         # Generate the archive page URLs for Oct 2020
#         for page_num in range(1, self.max_page + 1):
#             url = self.archive_base.format(page_num=page_num)
#             yield scrapy.Request(
#                 url,
#                 callback=self.parse_archive,
#                 meta={
#                     "playwright": True,
#                     "playwright_page_methods": [
#                         PageMethod("wait_for_selector", "article.entry")
#                     ],
#                     "page_num": page_num,
#                 },
#                 errback=self.errback
#             )

#     def parse_archive(self, response):
#         page_num = response.meta.get("page_num")
#         self.logger.info(f"Parsing archive page {page_num}: {response.url}")

#         # For each article on the archive page
#         for article in response.css("article.entry"):
#             title = article.css("h3.entry-title a::text").get()
#             url = article.css("h3.entry-title a::attr(href)").get()
#             date = article.css("div.entry-date::text").get()

#             # Get a snippet / excerpt
#             snippet = article.css("div.entry-excerpt p::text").get()
#             if snippet is None:
#                 snippet = ""  # fallback

#             # Filter by keyword "endsars" in title or snippet (case-insensitive)
#             text_to_check = ((title or "") + " " + snippet).lower()
#             if "endsars" in text_to_check or "#endsars" in text_to_check:
#                 yield {
#                     "title": title.strip() if title else "",
#                     "url": url,
#                     "date": date.strip() if date else "",
#                     "snippet": snippet.strip()
#                 }

#     def errback(self, failure):
#         self.logger.warning(f"Failed to download {failure.request.url}: {failure.value}")
#         # Optionally retry
#         req = failure.request
#         retry_count = req.meta.get("retry_count", 0)
#         if retry_count < self.custom_settings["RETRY_TIMES"]:
#             req.meta["retry_count"] = retry_count + 1
#             self.logger.info(f"Retrying {req.url} (retry {retry_count + 1})")
#             yield req
