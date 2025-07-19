#!/usr/bin/env python3
"""Integration test for GithubOrgClient"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized_class
from client import GithubOrgClient


@parameterized_class([
    {
        "org_payload": {"login": "test-org", "repos_url": "https://api.github.com/orgs/test-org/repos"},
        "repos_payload": [{"name": "repo1"}, {"name": "repo2"}],
        "expected_repos": ["repo1", "repo2"],
        "org": "test-org"
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class using parameterized_class"""

    @classmethod
    def setUpClass(cls):
        """Set up mocks"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            org_url = f'https://api.github.com/orgs/{cls.org}'  # type: ignore[attr-defined]
            repos_url = cls.org_payload["repos_url"]  # type: ignore[attr-defined]

            if url == org_url:
                response = Mock()
                response.json.return_value = cls.org_payload  # type: ignore[attr-defined]
                return response
            elif url == repos_url:
                response = Mock()
                response.json.return_value = cls.repos_payload  # type: ignore[attr-defined]
                return response
            return None

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Tear down mocks"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos method returns expected repo names"""
        client = GithubOrgClient(self.org)  # type: ignore[attr-defined]
        self.assertEqual(client.public_repos(), self.expected_repos)  # type: ignore[attr-defined]
