#!/usr/bin/env python3
"""Client module for GithubOrgClient"""

import requests


def get_json(url):
    """Fetch JSON data from a URL"""
    response = requests.get(url)
    return response.json()


class GithubOrgClient:
    """GitHub Organization Client"""

    def __init__(self, org_name):
        self.org_name = org_name

    @property
    def org(self):
        """Get the org details"""
        url = f"https://api.github.com/orgs/{self.org_name}"
        return get_json(url)

    @property
    def _public_repos_url(self):
        """Get public repos URL from org data"""
        return self.org.get("repos_url")

    def public_repos(self):
        """Return list of public repo names"""
        url = self._public_repos_url
        repos = get_json(url)
        return [repo["name"] for repo in repos]
