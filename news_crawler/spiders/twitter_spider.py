import scrapy
from scrapy_playwright.page import PageMethod

class TwitterSpider(scrapy.Spider):
    name = "twitter"
    
    # List of search queries
    queries = ["rape", "sexual abuse", "fraud"]

    # Number of scrolls to perform per search
    max_scrolls = 3

    async def start(self):
        """Start async requests for each query."""
        for q in self.queries:
            url = f"https://twitter.com/search?q={q}&f=live"
            yield scrapy.Request(
                url=url,
                callback=self.parse_search,
                meta={
                    "playwright": True,  # Must include to attach playwright_page
                    "playwright_page_methods": [
                        PageMethod("wait_for_load_state", "domcontentloaded")
                    ],
                    "query": q,
                    "scroll_count": 0  # initialize scroll counter
                }
            )

    async def parse_search(self, response):
        """Parse tweets from the search page."""
        page = response.meta["playwright_page"]
        query = response.meta["query"]
        scroll_count = response.meta["scroll_count"]

        # Wait until tweets are loaded
        await page.wait_for_selector("article")

        # Select all tweet articles on the page
        tweets = await page.query_selector_all("article")
        for t in tweets:
            tweet_text = await t.query_selector_eval("div[lang]", "el => el.innerText")
            tweet_author = await t.query_selector_eval("div[dir='ltr'] > span", "el => el.innerText")
            yield {
                "query": query,
                "tweet_author": tweet_author,
                "tweet_text": tweet_text
            }

        # Scroll for more tweets if max_scrolls not reached
        if scroll_count < self.max_scrolls:
            scroll_count += 1
            await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000)  # wait 2 seconds for tweets to load
            yield scrapy.Request(
                url=response.url,
                callback=self.parse_search,
                meta={
                    "playwright": True,
                    "playwright_page": page,  # reuse the same Playwright page
                    "query": query,
                    "scroll_count": scroll_count
                },
                dont_filter=True  # allow same URL to be requested again
            )
        else:
            await page.close()  # close page when done
