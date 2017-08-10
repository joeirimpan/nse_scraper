# -*- coding: utf-8 -*-
"""
    scraper.py

    :copyright: (c) 2017 by Joe Paul.
    :license: see LICENSE for details.
"""
import os
import json

from redis import Redis


class NSEScraper(object):
    """NSE Scraper class
    """

    def __init__(self, *args, **kwargs):
        self.url = 'https://www.nseindia.com/live_market/dynaContent/live_analysis/%s/%s.json'  # noqa
        self.redis_store = self.get_redis_client()

    def get_redis_client(self):
        """Return redis client instance
        """
        return Redis(
            host=os.environ.get('REDIS_HOST', 'localhost'),
            port=os.environ.get('REDIS_PORT', 6379),
            db=os.environ.get('REDIS_DB', 0)
        )

    def get_stocks_data(self, type='gainers'):
        """Utility method to fetch data from stocks JSON source

        :param type: The type of the data we need to fetch (gainers, losers)
        """
        pass

    @property
    def data_key(self):
        """Return the data key
        """
        return 'nse:stock_info'

    def store_now(self):
        """Persist data onto redis
        """
        data = dict(
            (type, self.get_stocks_data(type))
            for type in ['gainers', 'losers']
        )
        self.redis_store.set(self.data_key, json.dumps(data))
