# -*- coding: utf-8 -*-
"""
    scraper.py

    :copyright: (c) 2017 by Joe Paul.
    :license: see LICENSE for details.
"""
import os
import json
from contextlib import contextmanager

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from redis import Redis
from bs4 import BeautifulSoup


class NSEScraper(object):

    SCRAPER = {
        'fields': [
            'symbol',
            'last_traded_price',
            'percent_of_change',
            'traded_qty',
            'value_in_lakhs',
            'open',
            'high',
            'low',
            'previous_close',
            'latest_ex_date'
        ],
        'top_gainers': {
            'tab': 'tab7',
            'table': 'topGainers'
        },
        'top_losers': {
            'tab': 'tab8',
            'table': 'topLosers'
        },
    }

    def __init__(self, url=None, *args, **kwargs):
        self.url = url or 'https://www.nseindia.com/live_market/dynaContent/live_analysis/top_gainers_losers.htm'  # noqa
        self.redis_store = self.get_redis_client()
        self.phantomjs = self.get_phantomjs_browser()

    def get_phantomjs_browser(self):
        """Return phantomjs headless browser
        """
        phantomjs = webdriver.PhantomJS()
        phantomjs.get(self.url)
        return phantomjs

    def get_redis_client(self):
        return Redis(
            host=os.environ.get('REDIS_HOST', 'localhost'),
            port=os.environ.get('REDIS_PORT', 6379),
            db=os.environ.get('REDIS_DB', 0)
        )

    def scrape_data_for(self, tab='top_gainers'):
        interesting_elements = self.SCRAPER.get(tab)
        # Trigger click
        self.phantomjs.find_element_by_id(
            interesting_elements['tab']
        ).click()

        with self.load_source_for_page(
                interesting_elements['table'], timeout=10
        ) as source:
            # Find table
            table_element = source.find(
                'table', id=interesting_elements['table']
            )
            return map(
                lambda t: self.extract_fields_from_table(t),
                table_element.findAll('tr')[1:]
            )
        return []

    def extract_fields_from_table(self, element):
        elements = [td.text for td in element.findAll('td')[:-1]]
        return dict(zip(self.SCRAPER['fields'], elements))

    def store_now(self):
        data = dict(
            (tab, self.scrape_data_for(tab))
            for tab in ['top_gainers', 'top_losers']
        )
        self.redis_store.set('nse:stock_info', json.dumps(data))

    @contextmanager
    def load_source_for_page(self, id, timeout=30):
        WebDriverWait(self.phantomjs, timeout).until(
            expected_conditions.visibility_of_element_located((By.ID, id))
        )
        yield BeautifulSoup(self.phantomjs.page_source)
