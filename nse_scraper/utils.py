# -*- coding: utf-8 -*-
"""
    utils.py

    :copyright: (c) 2017 by Joe Paul.
    :license: see LICENSE for details.
"""
import os


def fp(rel_path):
    "Return the full path of given rel_path"
    return os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            rel_path
        )
    )
