from flask import Flask
from flask_caching import Cache

cache = Cache()


def register_cache(app: Flask):
    cache.init_app(app, config={"CACHE_TYPE": "SimpleCache"})
