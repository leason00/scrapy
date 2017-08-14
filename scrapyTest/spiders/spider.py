# -*-coding:utf-8-*-
import sys
import logging
from scrapy.spiders import CrawlSpider
from scrapyTest.items import ScrapytestItem
from scrapy.http import Request
from scrapy.selector import Selector
import urlparse

reload(sys)
sys.setdefaultencoding("utf-8")


class ListSpider(CrawlSpider):
    logging.getLogger("requests").setLevel(logging.WARNING)  # 将requests的日志级别设成WARNING
    logging.basicConfig(
        level=logging.DEBUG,
        format=
        '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='cataline.log',
        filemode='w')

    # 爬虫名称
    name = "scrapyTest"
    # 设置下载延时
    download_delay = 1
    # 允许域名
    allowed_domains = ["www.ireader.com"]
    # 开始URL
    start_urls = [
        "http://www.ireader.com/index.php?ca=booksort.index&pca=booksort.index&pid=92",
        "http://www.ireader.com/index.php?ca=booksort.index&pca=booksort.index&pid=10",
        "http://www.ireader.com/index.php?ca=booksort.index&pca=booksort.index&pid=68"
    ]

    def start_requests(self):
        for ph_type in self.start_urls:
            yield Request(url=ph_type,
                          callback=self.parse_type_key)

        # yield Request(url='http://www.ireader.com/index.php?ca=bookdetail.index&pca=booksort.index&bid=11525158',
        #                   callback=self.parse_content)

    def parse_type_key(self, response):
        selector = Selector(response)
        # 获取书籍类型
        types = selector.xpath('//div[@class="difgenre"]')[1].xpath('.//div[@class="right"]/ul/li')
        for type in types:
            type_url = type.xpath('.//a/@href')[0].extract()
            logging.info('类型' + type_url)
            # print '类型',type_url
            yield Request(url=type_url,
                          callback=self.parse_ph_key)

    def parse_ph_key(self, response):
        selector = Selector(response)
        # 获取书籍列表
        lis = selector.xpath('//ul[@class="newShow"]/li')
        for li in lis:
            view_url = li.xpath('.//a/@href')[0].extract()
            # print '爬取地址', view_url
            logging.info('爬取地址' + view_url)
            yield Request(url=view_url, callback=self.parse_content)
        # 获取下一页
        url_next = selector.xpath('//a[@class="down"]/@href')[0].extract()
        if url_next:
            # print '下一页地址', url_next
            logging.info('下一页地址' + url_next)
            yield Request(url=url_next,
                          callback=self.parse_ph_key)

    # 解析内容函数
    def parse_content(self, response):

        logging.debug('正在爬取地址' + response.url)

        item = ScrapytestItem()

        item['_id'] = dict([(k, v[0]) for k, v in urlparse.parse_qs(urlparse.urlparse(response.url).query).items()])['bid']
        # 当前URL
        item['url'] = response.url
        # title
        item['title'] = response.selector.xpath('//div[@class="bookname"]/h2/a/text()')[0].extract().decode('utf-8')

        item['tag'] = response.selector.xpath('//div[@class="bookL"]/s/text()')[0].extract().decode('utf-8')

        item['img'] = response.selector.xpath('//div[@class="bookL"]/a/img/@src')[0].extract().decode('utf-8')

        item['des'] = response.selector.xpath('//div[@class="bookinf03"]/p/text()')[0].extract().decode('utf-8')

        try:
            # 评分
            item['rate'] = response.selector.xpath('//div[@class="bookname"]/span/text()')[0].extract().decode('utf-8')
            # 评价人数
            item['num_rate'] = response.selector.xpath('//div[@class="bookinf01"]/p/span[@class="manyMan"]/text()')[0].extract().decode('utf-8').split('人')[0]
        except Exception:
            item['rate'] = ''
            item['num_rate'] = ''

        # 作者
        item['author'] = response.selector.xpath('//div[@class="bookinf01"]/p/span[@class="author"]/text()')[0].extract().decode('utf-8').split('：')[1]
        # 字数
        item['num_word'] = response.selector.xpath('//div[@class="bookinf01"]/p/span')[1].xpath('.//text()')[0].extract().decode('utf-8').split('：')[1]

        try:
            # 出版社
            item['press'] = response.selector.xpath('//div[@class="bookinf01"]/p/span')[2].xpath('.//text()')[0].extract().decode('utf-8').split('：')[1]
        except Exception:
            item['press'] = ''

        # 价格
        item['price'] = response.selector.xpath('//div[@class="bookinf02"]/div[@class="left"]/p/i[@class="price"]/text()')[0].extract().decode('utf-8').split('：')[1]

        get_similar = response.selector.xpath('//div[@class="seeWrap"]/ul/li')

        similar = []

        for a in get_similar:
            url = a.xpath('.//p[@class="bookNume"]/a/@href')[0].extract()
            name = a.xpath('.//p[@class="bookNume"]/a/text()')[0].extract()
            similar.append({'name': name, 'url': url})

        # 相似推荐
        item['similar'] = similar

        logging.debug(item)

        yield item