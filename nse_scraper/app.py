# -*- coding: utf-8 -*-
"""
    app.py

    :copyright: (c) 2017 by Joe Paul.
    :license: see LICENSE for details.
"""
import json

import cherrypy
from cherrypy.process.plugins import BackgroundTask

from .scraper import NSEScraper
from .utils import fp


class App(object):
    """Cherrypy Application
    """

    def __init__(self, *args, **kwargs):
        self.scraper = NSEScraper()
        # Start the cherrypy background cron-like task
        BackgroundTask(
            interval=5 * 60,
            function=self.scraper.store_now,
            bus=cherrypy.engine
        ).start()

    @cherrypy.expose
    def index(self):
        return file(fp('templates/index.html'))

    @cherrypy.expose(['stocks_info.json'])
    @cherrypy.tools.json_out()
    def get_stocks_info(self):
        """JSON endpoint which returns the stocks info
        """
        data = self.scraper.redis_store.get(
            self.scraper.data_key
        )
        return json.loads(data)
