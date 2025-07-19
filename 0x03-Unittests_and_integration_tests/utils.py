#!/usr/bin/env python3
"""Integration test for GithubOrgClient"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos

@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "org": "test-org"
    },
    {
        "org_payload": org_payload,
        "repos_payload": apache2_repos,
        "expected_repos": ["apache2"],
        "org": "apache2"
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class using parameterized_class and fixtures"""

    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            org_url = f'https://api.github.com/orgs/{cls.org}'
            repos_url = cls.org_payload["repos_url"]

            if url == org_url:
                response = Mock()
                response.json.return_value = cls.org_payload
                return response
            elif url == repos_url:
                response = Mock()
                response.json.return_value = cls.repos_payload
                return response
            return None

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient(self.org)
        self.assertEqual(client.public_repos(), self.expected_repos)
