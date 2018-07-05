# -*- coding: utf-8 -*-
from scrapy.conf import settings
from scrapy.http import Request
from DaoHangWang.items import DaohangwangItem
import scrapy
import time
import re

class TenderinfospSpider(scrapy.Spider):
    name = 'tenderInfoSP'
    allowed_domains = ['okcis.cn']
    start_urls = ['http://www.okcis.cn/20180627-n2-20180627130254024334.html']

    column_map = {
        '招标公告':'search_column-bn',
        '中标结果':'search_column-rn',
        '招标预告':'search_column-bn_yg',
        '招标变更':'search_column-bn_bg'
    }

    timezb_map = {
        '当天内':'timezb-0',
        '一周内':'timezb-1',
        '一月内':'timezb-2',
        '三月内':'timezb-3',
        '半年内':'timezb-4',
        '一年内':'timezb-5'
    }
    stop = False

    def get_localtime(self):
        return time.strftime("%Y-%m-%d", time.localtime())

    def start_requests(self):
        for i in settings.get('SEARCH_WORDS'):
            for j in settings.get('COLUMN'):
                search_column = self.column_map[j]
                url = 'http://www.okcis.cn/as/keystr-{sw}/{sc}/{timzb}'.format(sw=i,sc=search_column,timzb=self.timezb_map[settings.get('TIMEZB')])
                yield Request(url=url,callback=self.nextRequest_generator,meta={'sc':j,'sw':i})

    # def nextRequest_generator(self, response):
    #     cur_page = 1
    #     stop = None
    #     while True:
    #         if stop: break
    #         url = response.url + '/page-{i}'.format(i=cur_page)
    #         print('发出第{dd}请求'.format(dd=cur_page))
    #         stop = yield Request(url=url, callback=self.test_parse,meta={'sc': response.meta['sc'], 'sw': response.meta['sw'], 'curnum':cur_page})
    #         cur_page += 1
    #         time.sleep(10)     #延迟5秒，等待响应返回配合self.stop做判断

    def nextRequest_generator(self, response):
        cur_page = 1
        url = response.url + '/page-{i}'.format(i=cur_page)
        print('发出第{dd}请求'.format(dd=cur_page))
        yield Request(url=url, callback=self.test_parse,meta={'sc': response.meta['sc'], 'sw': response.meta['sw'], 'curnum':cur_page})
        cur_page += 1
        # time.sleep(10)     #延迟5秒，等待响应返回配合self.stop做判断

    def test_parse(self, response):
        print('抓取{sw}结果第{num}页的所有招标项>>>>>>>'.format(sw=response.meta['sw'],num=response.meta['curnum']),response.url,'<<<<<<<')
        items = response.css('.xiangmu_ta_20140617').xpath('tr[@id]')
        if not items:
            print('>>>>>>>关键字"{sw}"在此页已再无"{sc}"信息<<<<<<<'.format(sw=response.meta['sw'],sc=response.meta['sc']))
            # self.nextRequest_generator().send(False)
            return
        else:
            self.nextRequest_generator()
            for item in items:
                url = 'http://www.okcis.cn/' + item.xpath('./td[4]/div/a/@href').extract_first()
                yield Request(url=url, callback=self.bidingContent_parse,
                              meta={'sc': response.meta['sc'], 'sw': response.meta['sw']})

    def bidingContent_parse(self, response):
        pipleitem = DaohangwangItem()
        pipleitem['crawlTime'] = self.get_localtime()
        pipleitem['platform'] = '导航网'
        pipleitem['search_column'] = response.meta['sc']
        pipleitem['url'] = response.url

        baseInfo = response.css('#zbggxx1 .xx').xpath('string(.)').extract_first()
        if baseInfo:
            address = re.findall('所属地区：(.*)', baseInfo)
            bidingProxy = re.findall('招标代理：(.*)',baseInfo)
            deadTime = re.findall('招标截止：(.*)',baseInfo)
            product = re.findall('所属行业：(.*)',baseInfo)
            publishTime = re.findall('加入日期 :(.*)',response.css('#xxbt2 .cheng').xpath('text()').extract_first())
            pjN1 = response.css('#zbggxx1 .xxbt').xpath('text()').extract()
            detail = response.css('#zbggxx1 .xxbt').xpath('text()').extract()

            pipleitem['address'] = address[0] if address else ''
            pipleitem['bidingProxy'] = bidingProxy[0] if bidingProxy else ''
            pipleitem['deadTime'] = deadTime[0] if deadTime else ''
            pipleitem['product'] = product[0] if product else ''
            pipleitem['publishTime'] = publishTime[0] if publishTime else ''
            pipleitem['projectName'] = pjN1[0] if pjN1 else ''
            pipleitem['detail'] = detail[0] if detail else ''
        else:
            print('>>>>这个页面需要VIP权限<<<<>>>>',response.url,'<<<<')

        return pipleitem


