# -*- coding: utf-8 -*-
"""
    serve.py

    :copyright: (c) 2017 by Joe Paul.
    :license: see LICENSE for details.
"""
import cherrypy

from nse_scraper.app import App


if __name__ == '__main__':
    app = App()
    cherrypy.tree.mount(
        root=app,
        script_name='/',
    )
    # Lets start the cherrypy engine so everything works
    cherrypy.engine.start()
    # Run the engine main loop
    cherrypy.engine.block()
