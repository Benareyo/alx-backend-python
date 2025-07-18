#!/usr/bin/env python3
"""Utils module"""

import requests
from functools import wraps


def get_json(url):
    """Get JSON from a URL"""
    response = requests.get(url)
    return response.json()


def access_nested_map(nested_map, path):
    """Access a nested map using a list of keys"""
    for key in path:
        if not isinstance(nested_map, dict):
            raise KeyError(key)
        if key not in nested_map:
            raise KeyError(key)
        nested_map = nested_map[key]
    return nested_map


def memoize(method):
    """Memoize decorator to cache method results per instance"""
    attr_name = f"_memoized_{method.__name__}"

    @wraps(method)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return property(wrapper)
