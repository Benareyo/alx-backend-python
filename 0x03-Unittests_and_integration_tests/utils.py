#!/usr/bin/env python3
"""Utils module"""

import requests


def access_nested_map(nested_map, path):
    """
    Access a nested map (dictionary) using a sequence of keys.

    Args:
        nested_map (dict): The dictionary to access.
        path (tuple): A tuple of keys to traverse the nested map.

    Returns:
        The value found by traversing the nested map using the keys in path.

    Raises:
        KeyError: If a key in the path is not found or
                  if the current value is not a dictionary when expecting one.
    """
    for key in path:
        if not isinstance(nested_map, dict):
            raise KeyError(key)
        nested_map = nested_map[key]
    return nested_map


def get_json(url):
    """
    Make an HTTP GET request to the specified URL and return the JSON response.

    Args:
        url (str): URL to make the GET request to.

    Returns:
        dict: JSON response from the URL.
    """
    response = requests.get(url)
    return response.json()


def memoize(method):
    """
    Memoization decorator to cache a method's result.

    Args:
        method (function): The instance method to memoize.

    Returns:
        property: A property that caches the result of the method call.
    """
    attr_name = f"_{method.__name__}"

    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return property(wrapper)
