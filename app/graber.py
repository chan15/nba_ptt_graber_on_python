# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
from config import *

class Graber(object):
    def __init__(self, ptt_id):
        self.contents = ''
        self.ptt_id = ptt_id
        self.counter = 0

    def run(self):
        self.get_main(DEFAULT_URL)

    def get_main(self, url):
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        titles = soup.find_all('div', 'title')
        for title in titles:
            title_string = title.text.strip()
            a = title.find('a')
            if a:
                href = URL_HEAD + a['href']
                sub_content = self.get_sub_content(href)
                if sub_content != '':
                    self.contents += '<h3>%s</h3>' % title.text.strip()
                    self.contents += '<a href="%s" target="_blank">%s</a>' % (href, href)
                    self.contents += sub_content + '<br>'
                    self.contents += '<hr>'
        self.counter += 1
        last_page = URL_HEAD + soup.find('div', 'btn-group-paging').find_all('a')[1]['href']

        if self.counter < PAGES:
            self.get_main(last_page)

    def get_sub_content(self, href):
        content = ''
        res = requests.get(href)
        soup = BeautifulSoup(res.text, 'html.parser')
        pushes = soup.find_all('div', 'push')
        for push in pushes:
            ptt_id = push.find_all('span')[1].text.strip()
            if ptt_id.lower() == self.ptt_id.lower():
                content += push.prettify()
        return content

    def result(self):
        if self.contents == '':
            return 'no data'
        return self.contents
