def access_nested_map(nested_map, path):
    """Access a nested map using a list of keys"""
    for key in path:
        if not isinstance(nested_map, dict):
            # If current level is not a dict, key cannot be found
            raise KeyError(key)
        if key not in nested_map:
            raise KeyError(key)
        nested_map = nested_map[key]
    return nested_map
