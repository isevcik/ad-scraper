import scrapy
import json
import time

class BazosSpider(scrapy.Spider):
    name = "bazos_spider"
    custom_settings = {
        'ITEM_PIPELINES': {
            'bazosspider.JsonWriterPipeline': 300,
        }
    }

    # def __init__(self, *args, **kwargs):
    #     self.definitions = {}
    #     super(BazosSpider, self).__init__(*args, **kwargs)

    def definitions_to_start_requests(self, definitions):
        for query, params in definitions.items():
            hledat = params["hledat"]
            cenado = params["cenado"]
            for hlokalita in params["hlokalita"]:
                url = f"https://www.bazos.cz/search.php?hledat={hledat}&rubriky=www&hlokalita={hlokalita}&humkreis=25&cenaod=&cenado={cenado}&kitx=ano"
                yield scrapy.Request(url=url, dont_filter=True, cb_kwargs={"query": query})

    def start_requests(self):
        return self.definitions_to_start_requests(self.definitions)

    def parse(self, response, query):
        ITEM_SELECTOR = "table[class=inzeraty]"
        for item in response.css(ITEM_SELECTOR):
            yield {
                "query": query,
                "link": item.css("a::attr(href)").extract_first(),
                "name": item.css(".nadpis").extract_first(),
                "desc": item.css(".popis").extract_first()
            }

class JsonWriterPipeline(object):
    items = {}

    def open_spider(self, spider):
        try:
            with open("bazos.json","r") as f:
                self.items = json.load(f)
        except FileNotFoundError as _:
            pass

    def close_spider(self, spider):
        with open("bazos.json","w+") as f:
            json.dump(self.items, f, sort_keys=True, indent=4, separators=(',', ': '))

    def process_item(self, item, spider):
        if item["link"] not in self.items:
            item["time"] = time.time()
            self.items[item["link"]] = item