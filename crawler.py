#-*-coding:utf-8-*-
import sys
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
reload(sys)
sys.setdefaultencoding('utf-8')

configure_logging
settings = get_project_settings()
runner = CrawlerRunner(settings)

@defer.inlineCallbacks

def crawl():
    #yield runner.crawl('userfollow')
    #yield runner.crawl('userinfo')
    #yield runner,crawl('weibocontent')
    yield runner.crawl('keyuser',keyword = sys.argv[1])
    reactor.stop()

crawl()
reactor.run()
