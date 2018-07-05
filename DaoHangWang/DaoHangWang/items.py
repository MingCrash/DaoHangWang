# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DaohangwangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    crawlTime = scrapy.Field() #S5 抓取时间
    platform = scrapy.Field() #S2 导航网
    search_column = scrapy.Field() #S3a 招标类型
    product = scrapy.Field() #S3b 招标产品 ->设置为所属行业
    tenderee_cor = scrapy.Field() #S11 招标商
    publishTime = scrapy.Field() #S6发布时间
    deadTime = scrapy.Field() #S7 截止时间
    submitTime = scrapy.Field() #S9 提交时间
    address = scrapy.Field() #S8 招标人地址
    projectName = scrapy.Field() #S4项目名称
    detail = scrapy.Field() #Q1 详细
    sum = scrapy.Field() #S10
    url = scrapy.Field() #S1
    bidingProxy = scrapy.Field() #G15 招标代理
    bidingProxyAddr = scrapy.Field() #G16 招标代理地址
    bidingProxy_contacter = scrapy.Field() #G17 联系人
    bidingProxy_phoneNum = scrapy.Field() #G18 联系电话
    tenderee = scrapy.Field() #G19 招标人
    tenderee_contacter = scrapy.Field() #G21 招标人联系人
    tenderee_phoneNum = scrapy.Field() #G22 招标人电话
    winbider = scrapy.Field() #G23 中标人
    winbiderAddr = scrapy.Field() #G24 中标人地址
    winbider_contacter = scrapy.Field()  # G25 中标人联系人
    winbider_phoneNum = scrapy.Field()  # G26 中标人电话
