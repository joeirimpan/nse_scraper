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


class NSEScraper(object):

    SCRAPER = {
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
        self.chrome = self.get_chrome_browser()

    def get_chrome_browser(self):
        chrome = webdriver.Chrome()
        chrome.get(self.url)
        return chrome

    def get_redis_client(self):
        return Redis(
            host=os.environ.get('REDIS_HOST', 'localhost'),
            port=os.environ.get('REDIS_PORT', 6379),
            db=os.environ.get('REDIS_DB', 0)
        )

    def scrape_data_for(self, tab='top_gainers'):
        interesting_elements = self.SCRAPER.get(tab)
        # Trigger click
        self.chrome.find_element_by_id(
            interesting_elements['tab']
        ).click()

        with self.wait_for_page_load(
                interesting_elements['table'], timeout=10
        ):
            # Find table
            table = self.chrome.find_element_by_id(
                interesting_elements['table']
            )
            return filter(
                None,
                map(
                    lambda t: t and t.text,
                    table.find_elements_by_tag_name('tr')[1:]
                )
            )
        return []

    def store_now(self):
        data = dict(
            (tab, self.scrape_data_for(tab))
            for tab in ['top_gainers', 'top_losers']
        )
        self.redis_store.set('nse:stock_info', json.dumps(data))

    @contextmanager
    def wait_for_page_load(self, id, timeout=30):
        yield WebDriverWait(self.chrome, timeout).until(
            expected_conditions.visibility_of_element_located((By.ID, id))
        )
