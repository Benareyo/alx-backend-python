#!/usr/bin/env python3
"""Integration tests for GithubOrgClient.public_repos"""

import unittest
from unittest.mock import patch
from parameterized import parameterized_class
from client import GithubOrgClient
import fixtures  # This is your fixtures.py file with org_payload, repos_payload, etc.
from typing import ClassVar, List, Dict, Any
class MockResponse:
    """Mock requests.Response to mimic .json() and .raise_for_status()"""
    def __init__(self, json_data):
        self._json = json_data

    def json(self):
        return self._json

    def raise_for_status(self):
        pass  # Assume always OK for tests



@parameterized_class([
    {
        "org_payload": fixtures.org_payload,
        "repos_payload": fixtures.repos_payload,
        "expected_repos": fixtures.expected_repos,
        "apache2_repos": fixtures.apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    org_payload: ClassVar[Dict[str, Any]]
    repos_payload: ClassVar[List[Dict[str, Any]]]
    expected_repos: ClassVar[List[str]]
    apache2_repos: ClassVar[List[str]]

    @classmethod
    def setUpClass(cls):
        # Start patching requests.get and assign to cls.get_patcher
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            if url == f"https://api.github.com/orgs/{cls.org_payload['login']}":
                return MockResponse(cls.org_payload)
            elif url == cls.org_payload.get("repos_url"):
                return MockResponse(cls.repos_payload)
            return MockResponse({})

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        # Stop patching requests.get
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        client = GithubOrgClient(self.org_payload["login"])
        filtered = [repo for repo in self.repos_payload
                    if repo.get("license") and repo["license"].get("key") == "apache-2.0"]
        apache2_names = [repo["name"] for repo in filtered]
        self.assertEqual(apache2_names, self.apache2_repos)
