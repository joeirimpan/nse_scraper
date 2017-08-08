# -*- coding: utf-8 -*-
"""
    app.py

    :copyright: (c) 2017 by Joe Paul.
    :license: see LICENSE for details.
"""
import os
import json

import cherrypy
from cherrypy.process.plugins import BackgroundTask

from .scraper import NSEScraper


def fp(rel_path):
    "Return the full path of given rel_path"
    return os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            rel_path
        )
    )


class App(object):
    """Cherrypy Application
    """

    def __init__(self, *args, **kwargs):
        self.scraper = NSEScraper()
        # Start the cherrypy background cron-like task
        BackgroundTask(
            interval=20,
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


if __name__ == '__main__':
    app = App()
    config = {
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': fp('static'),
            'tools.staticdir.index': 'index.html'
        }
    }
    cherrypy.tree.mount(
        root=app,
        script_name='/',
        config=config
    )
    # Lets start the cherrypy engine so everything works
    cherrypy.engine.start()
    # Run the engine main loop
    cherrypy.engine.block()
