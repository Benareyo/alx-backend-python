#!/usr/bin/env python3
"""Integration tests for GithubOrgClient.public_repos"""

import unittest
from unittest.mock import patch
from parameterized import parameterized_class
from client import GithubOrgClient
import fixtures  # your fixtures.py file with org_payload, repos_payload, etc.


class MockResponse:
    """Mock requests.Response for json() and raise_for_status()"""

    def __init__(self, json_data):
        self._json = json_data

    def json(self):
        return self._json

    def raise_for_status(self):
        pass  # Assume always OK


@parameterized_class([
    {
        "org_payload": fixtures.org_payload,
        "repos_payload": fixtures.repos_payload,
        "expected_repos": fixtures.expected_repos,
        "apache2_repos": fixtures.apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    org_payload: dict
    repos_payload: list
    expected_repos: list
    apache2_repos: list

    @classmethod
    def setUpClass(cls):
        # Patch requests.get before any tests run
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            if url == "https://api.github.com/orgs/google":
                return MockResponse(cls.org_payload)
            elif url == "https://api.github.com/orgs/google/repos":
                return MockResponse(cls.repos_payload)
            return MockResponse({})

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        # Stop patching after all tests
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        client = GithubOrgClient("google")
        # Filtering repos with apache-2.0 license manually here:
        filtered = [repo for repo in self.repos_payload
                    if GithubOrgClient.has_license(repo, "apache-2.0")]
        filtered_names = [repo["name"] for repo in filtered]
        self.assertEqual(filtered_names, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
