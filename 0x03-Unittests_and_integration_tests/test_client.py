#!/usr/bin/env python3
"""Integration test for GithubOrgClient"""

import unittest
from unittest.mock import patch, Mock
from client import GithubOrgClient

class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class without parameterized_class decorator"""

    @classmethod
    def setUpClass(cls):
        cls.org = "test-org"
        cls.org_payload = {"login": "test-org", "repos_url": "https://api.github.com/orgs/test-org/repos"}
        cls.repos_payload = [{"name": "repo1"}, {"name": "repo2"}]
        cls.expected_repos = ["repo1", "repo2"]

        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            if url == f'https://api.github.com/orgs/{cls.org}':
                response = Mock()
                response.json.return_value = cls.org_payload
                return response
            elif url == cls.org_payload["repos_url"]:
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
