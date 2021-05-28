from scrapy.crawler import CrawlerProcess
from bazosrealityspider import BazosSpider

import json
import time

definitions = {
    "brno": {
        "hlokalita": ["60200", "66434"],
    },
    "vyskov_kromeriz": {
        "hlokalita": ["68201", "76701"],
    },
    "zlin": {
        "hlokalita": ["76001"],
    },
}

process = CrawlerProcess()
process.crawl(BazosSpider, definitions=definitions)
process.start()
