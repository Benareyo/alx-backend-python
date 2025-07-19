#!/usr/bin/env python3
"""Utils module"""

def access_nested_map(nested_map, path):
    """Access nested map using keys in path"""
    current = nested_map
    for key in path:
        current = current[key]
    return current
