#!/usr/bin/env python3
"""GithubOrgClient module"""

import requests


class GithubOrgClient:
    """GithubOrgClient to interact with GitHub API"""

    def __init__(self, org_name: str) -> None:
        self.org_name = org_name

    @property
    def org(self) -> dict:
        """Fetch org info from GitHub"""
        url = f"https://api.github.com/orgs/{self.org_name}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    @property
    def _public_repos_url(self) -> str:
        """Get public repos URL from org info"""
        url = self.org.get("repos_url")  # Removed explicit Optional[str] here
        if not isinstance(url, str):
            raise ValueError("repos_url not found or not a string in org response")
        return url

    def public_repos(self) -> list[str]:
        """List public repo names"""
        url = self._public_repos_url
        response = requests.get(url)
        response.raise_for_status()
        repos = response.json()
        return [repo.get("name") for repo in repos]

    @staticmethod
    def has_license(repo: dict, license_key: str) -> bool:
        """Check if repo has the given license key"""
        license_info = repo.get("license")
        if not license_info:
            return False
        return license_info.get("key") == license_key
