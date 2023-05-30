import scrapy
from scrapy.selector import Selector
from scrapy.spiders import SitemapSpider
from bs4 import BeautifulSoup as bs
import html
import re
import os

class ThehartfordSpider(SitemapSpider):
    name = "thehartford"
    allowed_domains = ["www.thehartford.com"]
    # start_urls = ["https://www.thehartford.com/business-insurance/strategy/"]
    # start_urls = ["https://www.thehartford.com/business-insurance/strategy/startup","https://www.thehartford.com/business-insurance/strategy/startup-financing/borrowing-from-401k"]
    sitemap_urls = ["https://www.thehartford.com/sitemap.xml"]
    sitemap_rules = [("/business-insurance/strategy/", "parse_strategy")]

    def sitemap_filter(self, entries):
        requireLink = ''
        for entry in entries:
            if requireLink in entry.get('loc'):
                yield entry

    def parse_strategy(self, response):
        title = response.xpath("//header[1]/following-sibling::*[(@class='jumbotron')]").get()
        content = response.xpath("//header[1]/following-sibling::*[(self::main)]").get()
        if title or content:
            ## Create Folder to store the results
            folderName = response.url[28:].replace("/","_")
            if not os.path.exists(folderName):
                os.makedirs(folderName)

            if title is not None:
                soup = bs(title)          #make BeautifulSoup
                title = soup.prettify()   #prettify the html

                clean = re.compile('<.*?>')
                title = re.sub(clean, '', html.unescape(title))
                open(folderName+"/title.html", 'w', encoding='UTF-8').write(title)

            if content is not None:
                soup = bs(content)                #make BeautifulSoup
                content = soup.prettify()   #prettify the html

                clean = re.compile('<.*?>')
                content = re.sub(clean, '', html.unescape(content))
                open(folderName+"/content.html", 'w', encoding='UTF-8').write(content)
        pass

    def parse(self, response):
        pass


