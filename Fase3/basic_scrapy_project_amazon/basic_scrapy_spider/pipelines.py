# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class BasicScraperPipeline:
    def process_item(self, item, spider):
        return item

import json
import os

class JsonExportPipeline(object):
    def open_spider(self, spider):
        self.asin_to_exporter = {}

    def close_spider(self, spider):
        for exporter in self.asin_to_exporter.values():
            exporter.write('\n]')
            exporter.close()

    def process_item(self, item, spider):
        asin = item['asin']
        if asin not in self.asin_to_exporter:
            f = open(f'{asin}_reviews.json', 'w')
            f.write('[')
            self.asin_to_exporter[asin] = f
        else:
            f = self.asin_to_exporter[asin]
            f.write(',\n')
        
        # Create a copy of the item dictionary, remove the 'asin' field, and convert to JSON
        item_copy = dict(item)
        item_copy.pop('asin', None)
        line = json.dumps(item_copy)
        f.write(line)
        return item