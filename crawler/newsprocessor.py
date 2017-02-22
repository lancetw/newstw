#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import arrow
from crawler.utils.crawlerutils import loadContext, loadSkips, loadTrimtext, detectNewsSource
from crawler.utils.datautils import normalizeNews, delKey, trimDataVal

class NewsDataProcessor:
    def __init__(self, url, html):
        self.data = {}
        self.soup = BeautifulSoup(html, "html.parser")
        self.url = url
        self.html = html
        self.source = detectNewsSource(self.url)
        self.context = loadContext(self.source)
        self.trimtext = loadTrimtext(self.source)

    def output(self):
        self._process(self.html)
        if 'pass' not in self.data:
            self.data['pass'] = True
        return self.data

    def _process(self, html):
        self.data['link'] = self.url
        self.data['from'] = self.source
        if self.source == 'any':
            self.data['pass'] = False

        self._news_processor(html)
        self._time_corrector()
        delKey("_rawtime", (not __debug__), self.data)

        for text in self.trimtext:
            trimDataVal("summary", text, self.data)

    def _soupFunc(self, name, path):
        return {"select": self._soupSelect, "findAll": self._soupFindAll, "attrs": self._soupAttrs}.get(name)(path)

    def _soupAttrs(self, path):
        for k, v in path.items():
            return self.soup.find(k).attrs[v]

    def _soupSelect(self, path):
        if isinstance(path, list):
            for p in path:
                target = self.soup.select(p)
                if len(target) > 0:
                    break
        else:
            target = self.soup.select(path)
        return target

    def _soupFindAll(self, path):
        return self.soup.find_all(path)

    def _soup(self, html, skips):
        if skips:
            for tag in self.soup(skips):
                tag.decompose()

    def _news_processor(self, html):
        skips = loadSkips(self.source)
        self._soup(skips, html)

        for context in self.context:
            if 'save' not in context:
                continue
            if 'soup' not in context or not context['soup']:
                context['soup'] = 'select'

            text = self._context_to_text(context)
            text = normalizeNews(text)
            if not text:
                self.data['pass'] = False
            self.data[context['save']] = text

    def _time_corrector(self):
        for c in self.context:
            published = None
            try:
                if 'tzinfo' in c and self.data['_rawtime']:
                    if 'format' in c and isinstance(c['format'], str):
                        c['format'] = [c['format']]

                    for i in range(len(c['format'])):
                        try:
                            published = arrow.get(self.data['_rawtime'], c['format'][i])
                            if 'pass' in self.data and not self.data['pass']:
                                self.data.pop('pass', None)
                        except arrow.parser.ParserError as err:
                            if len(c['format']) <= i:
                                raise
                            else:
                                continue
                else:
                    published = arrow.get(self.data['_rawtime'])

                if published:
                    self.data['published'] = published.replace(tzinfo=c['tzinfo']).format()

            except arrow.parser.ParserError as err:
                self.data['pass'] = False
                if __debug__: self.data['debug'] = err

    def _context_to_text(self, context):
        text = ''
        if context['ind'] >= 0:
            try:
                if not 'path' in context:
                    context['path'] = ''
                res = self._soupFunc(context['soup'], context['path'])
                if isinstance(res, str):
                    text = res
                else:
                    text = res[context['ind']].text

            except IndexError as err:
                self.data['pass'] = False
                if __debug__: self.data['debug'] = err
        else:
            tags = self._soupFunc(context['soup'], context['path'])
            text = ''.join([tag.text for tag in tags])

        return text
