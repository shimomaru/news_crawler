  # news_crawler/items.py
from dataclasses import dataclass

@dataclass
class ArticleMatch:
    source: str
    url: str
    title: str
    date_published: str
    matched_keywords: str
    snippet: str
    scraped_at: str
