# -*- coding: utf-8 -*-
"""
    extensions.py

    :copyright: (c) 2017 by Joe Paul.
    :license: see LICENSE for details.
"""
import os

from redis import Redis


redis_store = Redis.from_url(url=os.environ['REDIS_URL'])
