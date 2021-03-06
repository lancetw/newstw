#!/usr/bin/env python
# -*- coding: utf-8 -*-

from crawler.utils.crawler_utils import load_context, load_skips, load_trimtext, detect_news_source
from crawler.utils.crawler_helper import fetch_news
from utils.pprint_helper import pprint_color

import unittest


class TestCrawler(unittest.TestCase):

    def setUp(self):
        url = self.urls = {}
        # 四大報
        url['ltn'] = [None] * 1
        url['ltn'][0] = "http://news.ltn.com.tw/news/life/breakingnews/1979996"

        url['appledaily'] = [None] * 1
        url['appledaily'][0] = "http://www.appledaily.com.tw/appledaily/article/headline/20170308/37575364//"

        url['chinatimes'] = [None] * 1
        url['chinatimes'][0] = "http://www.chinatimes.com/realtimenews/20170219000888-260408"

        url['udn'] = [None] * 1
        url['udn'][0] = "https://udn.com/news/story/7316/2294464"

        # 電視傳媒
        url['pts'] = [None] * 1
        url['pts'][0] = "http://news.pts.org.tw/article/350012"

        url['ftv'] = [None] * 1
        url['ftv'][0] = "https://news.ftv.com.tw/news/detail/2017703P07M1"

        url['setn'] = [None] * 2
        url['setn'][0] = "http://www.setn.com/News.aspx?NewsID=226627"
        url['setn'][1] = "http://www.setn.com/E/News.aspx?NewsID=226596"

        url['eranews'] = [None] * 1

        url['eranews'][0] = "http://eranews.eracom.com.tw/files/news/xml/era/n59250.xml"

        url['tvbs'] = [None] * 1
        url['tvbs'][0] = "http://news.tvbs.com.tw/fun/708444"

        url['ctitv'] = [None] * 1
        url['ctitv'][0] = "http://gotv.ctitv.com.tw/2017/02/384052.htm"

    def test_detect_news_source(self):
        for source, urls in self.urls.items():
            for url in urls:
                self.assertEqual(detect_news_source(url), source)

    def test_load_context(self):
        from crawler.web_shape_var import context

        for c, _ in self.urls.items():
            self.assertNotEqual(load_context(c), {})
            self.assertNotEqual(load_context(c), context['any'], "(%s)" % c)

    def test_load_skips(self):
        for c, _ in self.urls.items():
            load_skips(c)
            self.assertTrue(True)

    def test_fetch_news(self):
        for c, urls in self.urls.items():
            for url in urls:
                news = fetch_news(url)
                self.assertIn("title", news)
                self.assertIn("summary", news)
                self.assertIn("_rawtime", news)
                self.assertIn("published", news)
                self.assertIn("link", news)
                self.assertIn("source", news)
                print(url)
                self.assertTrue(news["pass"])
                self.assertTrue(True)
                # pprint_color(news)

    def test_shorten_url(self):
        news = fetch_news("https://goo.gl/6IXNnC")
        # pprint_color(news)

        self.assertIn("source", news)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
