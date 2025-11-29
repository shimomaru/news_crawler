# import scrapy
# from scrapy_playwright.page import PageMethod

# class EndSARSOctoberSpider(scrapy.Spider):
#     name = "endsars_oct2020"
#     start_urls = [
#         "https://dailypost.ng/2020/10/",
#         "https://www.naijanews.com/2020/10/",
#         "https://dailytimes.ng/2020/10/"
#     ]

#     custom_settings = {
#         "DOWNLOAD_HANDLERS": {
#             "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
#             "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
#         },
#         "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
#         "PLAYWRIGHT_BROWSER_TYPE": "chromium",
#     }

#     def start_requests(self):
#         for url in self.start_urls:
#             yield scrapy.Request(
#                 url,
#                 meta={
#                     "playwright": True,
#                     "playwright_page_methods": [
#                         PageMethod("wait_for_load_state", "domcontentloaded")
#                     ],
#                 },
#                 callback=self.parse
#             )

#     async def parse(self, response):
#         page = response.meta.get("playwright_page")

#         # Extract articles
#         articles = response.css("div.mvp-blog-story-out")
#         for article in articles:
#             yield {
#                 "title": article.css("h2::text").get(),
#                 "category": article.css("span.mvp-cd-cat::text").get(),
#                 "date": article.css("span.mvp-cd-date::text").get(),
#                 "summary": article.css("div.mvp-blog-story-text p::text").get(),
#                 "image_url": article.css("div.mvp-blog-story-img img::attr(src)").get(),
#                 "source": response.url,
#             }

#         # Follow pagination links
#         next_page = response.css("a.next.page-numbers::attr(href)").get()
#         if next_page:
#             yield response.follow(
#                 next_page,
#                 meta={
#                     "playwright": True,
#                     "playwright_page_methods": [
#                         PageMethod("wait_for_load_state", "domcontentloaded")
#                     ],
#                 },
#                 callback=self.parse
#             )
