# news_crawler/utils.py
def abort_request(resource_type):
    return resource_type in ("image", "media", "font", "stylesheet", "manifest")
