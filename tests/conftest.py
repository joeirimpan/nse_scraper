# -*- coding: utf-8 -*-
import vcr
import pytest

from nse_scraper.nse_api import NSE


nse_vcr = vcr.VCR(
    filter_headers=[
        'Authorization',
    ]
)


@pytest.fixture
def nse_api():
    return NSE()
