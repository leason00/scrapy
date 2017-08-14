# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from config.user_agents import agents
import random, json


class ScrapytestSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        # print 1
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.

        # 过滤url

        # print 2
        for i in result:
            # print i
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        # print 3
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        # print 4
        for r in start_requests:
            # print r
            yield r

    def spider_opened(self, spider):
        # print 5
        spider.logger.info('Spider opened: %s' % spider.name)

class UserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent


class CookiesMiddleware(object):
    """ 换Cookie """
    cookie = {
        'Hm_lpvt_2583df02aa8541db9378beae2ed00ba0': '1502265076',
        'Hm_lvt_2583df02aa8541db9378beae2ed00ba0': '1502263527',
        'ZyId': 'ada56e4598ab89a9944f'
    }

    def process_request(self, request, spider):
        # bs = ''
        # for i in range(32):
        #     bs += chr(random.randint(97, 122))
        # _cookie = json.dumps(self.cookie) % bs
        request.cookies = self.cookie