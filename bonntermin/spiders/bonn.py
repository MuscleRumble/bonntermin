# -*- coding: utf-8 -*-
import scrapy
import urlparse
import dateparser

from bonntermin.items import BookableItem
from scrapy.mail import MailSender


class BonnSpider(scrapy.Spider):
    name = 'bonn'
    allowed_domains = ['netappoint.de']
    start_urls = ['https://netappoint.de/ot/stadtbonn/?company=stadtbonn']

    # customize for your own needs
    form_data = {'casetype_9664': '1', 'casetype_9656': '1'}
    wanted_year = 2016
    wanted_month = 6
    notification_email = 'mail@example.com'

    def parse(self, response):
        yield scrapy.FormRequest.from_response(response,
                                               formname='frm_casetype',
                                               formdata=self.form_data,
                                               callback=self.parse_step2)

    def parse_step2(self, response):
        # retrieve bookable days
        bookable_days = []
        for href in response.css('a.nat_calendar_weekday_bookable::attr(href)').extract():
            queries = dict(urlparse.parse_qsl(href))
            bookable_day = int(queries['day'])
            bookable_days.append(bookable_day)

        # retrieve bookable month and year
        bookable_month_year = response.css('.nat_navigation_currentmonth > abbr::text').extract_first()
        bookable_datetime = dateparser.parse(bookable_month_year)
        bookable_month = bookable_datetime.date().month
        bookable_year = bookable_datetime.date().year

        # send mail, if bookable year/month == wanted year/month
        if (bookable_year == self.wanted_year and
                bookable_month == self.wanted_month):
            self.send_mail(bookable_month_year)

        # yield bookable item
        item = BookableItem()
        item['year'] = bookable_year
        item['month'] = bookable_month
        item['days'] = bookable_days
        yield item

    def send_mail(self, month_year):
        subject = 'Bonn: Neuer Termin frei im ' + month_year
        body = self.start_urls[0]
        # you have to set up the mail settings in your own settings.py
        # http://doc.scrapy.org/en/latest/topics/email.html#topics-email-settings
        mailer = MailSender.from_settings(self.settings)
        mailer.send(to=[self.notification_email], subject=subject, body=body)
