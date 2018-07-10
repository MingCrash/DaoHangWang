# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import sys
from scrapy.conf import settings
from scrapy.signals import spider_closed

class Size16M_Pipeline(object):
    buffer_list = None
    filename = None

    def __init__(self):
        self.buffer_list = []
        self.filename = 0

    def close_spider(self, spider):
        if self.buffer_list:
            with open('{path}/{cfn}'.format(cfn='{}.txt'.format(self.filename + 1), path=settings.get('STORE_PATH')),
                      'a+') as f:
                f.writelines(self.buffer_list)
                self.buffer_list.clear()

    def process_item(self, item, spider):
        str = '《Root》《S1》{url}《/S1》《S5》{ct}《/S5》《S2》{pf}《/S2》《S3a》{sc}《/S3a》《S3b》{produc}《S3b》《S4》{pjn}《/S4》《S6》{pt}《/S6》《S7》{deadTime}《/S7》《S8》{address}《/S8》《S9》{st}《/S9》《S10》{sum}《/S10》《Q1》{detail}《/Q1》《G15》{bp}《/G15》《G16》{bpa}《/G16》《G17》{bpc}《/G17》《G18》{bpp}《/G18》《G19》{tenderee}《/G19》《G21》{tc}《/G21》《G22》{tpN}《/G22》《G23》{wb}《/G23》《G24》{wba}《/G24》《G25》{wbc}《/G25》《G24》{wbpN}《/G24》《Root》\n'.format(
            ct=item.setdefault('crawlTime', ''), url=item.setdefault('url', ''), pf=item.setdefault('platform', ''),
            sc=item.setdefault('search_column', ''), pjn=item.setdefault('projectName', ''),
            pt=item.setdefault('publishTime', ''),
            detail=item.setdefault('detail', ''), produc=item.setdefault('product', ''),
            st=item.setdefault('submitTime', ''),
            deadTime=item.setdefault('deadTime', ''), address=item.setdefault('address', ''),
            sum=item.setdefault('sum', ''),
            bp=item.setdefault('bidingProxy', ''), bpa=item.setdefault('bidingProxyAddr', ''),
            bpc=item.setdefault('bidingProxy_contacter', ''),
            bpp=item.setdefault('bidingProxy_phoneNum', ''), tenderee=item.setdefault('tenderee', ''),
            tc=item.setdefault('tenderee_contacter', ''),
            tpN=item.setdefault('tenderee_phoneNum', ''), wb=item.setdefault('winbider', ''),
            wba=item.setdefault('winbiderAddr', ''),
            wbc=item.setdefault('winbider_contacter', ''), wbpN=item.setdefault('winbider_phoneNum', ''))

        print(sys.getsizeof(self.buffer_list))
        if not sys.getsizeof(self.buffer_list) > settings.get('FILE_SIZE'):
            self.buffer_list.append(str)
        else:
            self.filename = self.filename
            with open('{path}/{cfn}'.format(cfn='{}.txt'.format(self.filename), path=settings.get('STORE_PATH')),'a+') as f:
                f.writelines(self.buffer_list)
                self.buffer_list.clear()

        return item
