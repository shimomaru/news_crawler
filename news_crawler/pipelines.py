class TwitterSpider(scrapy.Spider):
    name = "twitter"
    
    queries = ["rape", "sexual abuse", "fraud"]
    max_scrolls = 3

    def start_requests(self):
        for q in self.queries:
            url = f"https://twitter.com/search?q={q}&f=live"
            yield scrapy.Request(
                url=url,
                callback=self.parse_search,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_load_state", "domcontentloaded")
                    ],
                    "query": q,
                    "scroll_count": 0
                }
            )

    async def parse_search(self, response):
        page = response.meta["playwright_page"]
        query = response.meta["query"]
        scroll_count = response.meta["scroll_count"]

        await page.wait_for_selector("article")
        tweets = await page.query_selector_all("article")

        for t in tweets:
            tweet_text_el = await t.query_selector("div[lang]")
            tweet_text = await tweet_text_el.inner_text() if tweet_text_el else ""
            tweet_author_el = await t.query_selector("div[dir='ltr'] > span")
            tweet_author = await tweet_author_el.inner_text() if tweet_author_el else ""
            yield {
                "query": query,
                "tweet_author": tweet_author,
                "tweet_text": tweet_text
            }

        if scroll_count < self.max_scrolls:
            scroll_count += 1
            await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000)
            yield scrapy.Request(
                url=response.url,
                callback=self.parse_search,
                meta={
                    "playwright": True,
                    "playwright_page": page,
                    "query": query,
                    "scroll_count": scroll_count
                },
                dont_filter=True
            )
        else:
            await page.close()
