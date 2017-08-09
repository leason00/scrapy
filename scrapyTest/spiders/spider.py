# -*-coding:utf-8-*-
import sys
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapyTest.items import ScrapytestItem
from scrapy.http import Request
from scrapy.selector import Selector
import re

reload(sys)
sys.setdefaultencoding("utf-8")


class ListSpider(CrawlSpider):
    # 爬虫名称
    name = "scrapyTest"
    # 设置下载延时
    download_delay = 1
    # 允许域名
    allowed_domains = ["news.cnblogs.com"]
    # allowed_domains = ["www.ireader.com"]
    # 开始URL
    start_urls = [
        # "http://www.ireader.com/"
        "https://news.cnblogs.com/"
    ]
    # 爬取规则,不带callback表示向该类url递归爬取
    rules = (
        Rule(SgmlLinkExtractor(allow=(r'https://news.cnblogs.com/n/page/\d',))),
        # Rule(SgmlLinkExtractor(allow=(r'http://www.ireader.com/index.php?ca=booksort.index&pca=booksort.index&pid=[92|10|68]&cid=\d{3}&order=download&status=[0|1|2|3|4]&page=\d+',))),
        Rule(SgmlLinkExtractor(allow=(r'https://news.cnblogs.com/n/\d+',)), callback='parse_content'),
        # Rule(SgmlLinkExtractor(allow=(r'http://www.ireader.com/index.php?ca=bookdetail.index&bid=\d+',)), callback='parse_content'),
    )

    # test = True
    def start_requests(self):
        for ph_type in self.start_urls:
            yield Request(url='https://www.pornhub.com/%s' % ph_type,
                          callback=self.parse_ph_key)

    def parse_ph_key(self, response):
        selector = Selector(response)

        # logging.info(selector)
        divs = selector.xpath('//div[@class="phimage"]')
        for div in divs:
            viewkey = re.findall('viewkey=(.*?)"', div.extract())
            # logging.debug(viewkey)
            yield Request(url='https://www.pornhub.com/embed/%s' % viewkey[0],
                          callback=self.parse_content)
        url_next = selector.xpath(
            '//a[@class="orangeButton" and text()="Next "]/@href').extract()
        if url_next:
            # if self.test:
            yield Request(url=self.host + url_next[0],
                          callback=self.parse_ph_key)

    # 解析内容函数
    def parse_content(self, response):
        item = ScrapytestItem()
        print 888888
        # 当前URL
        # title = response.selector.xpath('//div[@class="bookname"]')[0].extract().decode('utf-8')
        # item['title'] = title

        # author = response.selector.xpath('//div[@id="news_info"]/span/a/text()')[0].extract().decode('utf-8')
        # item['author'] = author
        #
        # releasedate = response.selector.xpath('//div[@id="news_info"]/span[@class="time"]/text()')[0].extract().decode(
        #     'utf-8')
        # item['releasedate'] = releasedate
        #
        # print item['author']
        # print item['title']

        yield item