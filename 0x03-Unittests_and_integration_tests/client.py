#!/usr/bin/env python3
"""Client module"""

def get_json(url):
    """Function that fetches JSON from URL (mocked in tests)."""
    # In real, this fetches from internet.
    return {}

class GithubOrgClient:
    """Github organization client"""

    def __init__(self, org_name):
        self.org_name = org_name

    @property
    def org(self):
        url = f"https://api.github.com/orgs/{self.org_name}"
        return get_json(url)
