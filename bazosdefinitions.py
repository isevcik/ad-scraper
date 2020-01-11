from scrapy.crawler import CrawlerProcess
from bazosspider import BazosSpider

import json
import time

definitions = {
    "nosic": {
        "hlokalita": ["60200", "68801"],
        "hledat": "stresni nosic",
        "cenado": 5000
    }
}

process = CrawlerProcess()
process.crawl(BazosSpider, definitions=definitions)
process.start()
