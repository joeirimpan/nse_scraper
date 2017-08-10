# -*- coding: utf-8 -*-
"""
    scraper.py

    :copyright: (c) 2017 by Joe Paul.
    :license: see LICENSE for details.
"""
import requests
from requests.exceptions import HTTPError

from .exceptions import NSEException


class NSE(object):
    """NSE Api wrapper class
    """

    def __init__(self, *args, **kwargs):
        self.url = 'https://www.nseindia.com/live_market/dynaContent/live_analysis/%s/%s.json'  # noqa

    def get_stocks_data(self, type='gainers'):
        """Utility method to fetch data from stocks JSON source

        :param type: The type of the data we need to fetch (gainers, losers)
        """
        file_name = 'nifty%s1' % type.capitalize()
        res = requests.get(self.url % (type, file_name))
        try:
            res.raise_for_status()
        except HTTPError, e:
            raise NSEException(
                '%s:%s' % (str(e.response.status_code), str(e.message))
            )
        return res.json().get('data')
