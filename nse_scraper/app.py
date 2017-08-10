# -*- coding: utf-8 -*-
"""
    app.py

    :copyright: (c) 2017 by Joe Paul.
    :license: see LICENSE for details.
"""
import json

import cherrypy
from cherrypy.process.plugins import BackgroundTask

from .nse_api import NSE
from .extensions import redis_store
from .utils import fp


class App(object):
    """Cherrypy Application
    """

    def __init__(self, *args, **kwargs):
        self.nse = NSE()
        # Start the cherrypy background cron-like task
        BackgroundTask(
            interval=5 * 60,
            function=self.store_now,
            bus=cherrypy.engine
        ).start()

    @property
    def stock_data_key(self):
        """Return the stock data key
        """
        return 'nse:stock_info'

    def store_now(self):
        """Persist data onto redis
        """
        data = {}
        for type in ['gainers', 'losers']:
            # Serialize list of dict to string
            data[type] = json.dumps(self.nse.get_stocks_data(type))

        # Store as hashmap datastructure to improve memory usage
        redis_store.hmset(self.stock_data_key, data)

    @cherrypy.expose
    def index(self):
        return file(fp('templates/index.html'))

    @cherrypy.expose(['stocks_info.json'])
    @cherrypy.tools.json_out()
    def get_stocks_info(self):
        """JSON endpoint which returns the stocks info
        """
        data = redis_store.hgetall(self.stock_data_key)
        # De-serialiaze the values
        for key, value in data.iteritems():
            data[key] = json.loads(value)
        return data
