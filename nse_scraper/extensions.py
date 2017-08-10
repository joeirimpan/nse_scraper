# -*- coding: utf-8 -*-
"""
    extensions.py

    :copyright: (c) 2017 by Joe Paul.
    :license: see LICENSE for details.
"""
import os

from redis import Redis


# TODO Use REDIS_URL if deploying on heroku
redis_store = Redis(
    host=os.environ.get('REDIS_HOST', 'localhost'),
    port=os.environ.get('REDIS_PORT', 6379),
    db=os.environ.get('REDIS_DB', 0)
)
