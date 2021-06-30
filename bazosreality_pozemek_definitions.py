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
url = "https://reality.bazos.cz/prodam/pozemek/?hledat=&rubriky=reality&hlokalita={hlokalita}&humkreis=30&cenaod=&cenado=&kitx=ano"
jsonfile = "bazosreality_pozemek.json"

process = CrawlerProcess()
process.crawl(BazosSpider, jsonfile=jsonfile, url=url, definitions=definitions)
process.start()
