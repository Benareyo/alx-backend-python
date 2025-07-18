#!/usr/bin/env python3
"""Unit and Integration tests for GithubOrgClient"""

import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from typing import ClassVar, List, Dict, Any

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google", {"repos_url": "https://api.github.com/orgs/google/repos"}),
        ("abc", {"repos_url": "https://api.github.com/orgs/abc/repos"}),
    ])
    @patch('client.requests.get')
    def test_org(self, org_name, expected, mock_get):
        """Test that org property returns correct data"""
        mock_get.return_value.json.return_value = expected
        mock_get.return_value.raise_for_status = Mock()

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @patch('client.requests.get')
    def test_public_repos(self, mock_get):
        """Test public_repos method returns repo names list"""
        fake_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get.return_value.json.return_value = fake_repos_payload
        mock_get.return_value.raise_for_status = Mock()

        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = "https://api.github.com/orgs/fakeorg/repos"

            client = GithubOrgClient("fakeorg")
            repos = client.public_repos()
            self.assertEqual(repos, ["repo1", "repo2", "repo3"])

            mock_public_repos_url.assert_called_once()
            mock_get.assert_called_once_with("https://api.github.com/orgs/fakeorg/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct bool"""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


payload = TEST_PAYLOAD[0]

@parameterized_class([
    {
        "org_payload": payload["org_payload"],
        "repos_payload": payload["repos_payload"],
        "expected_repos": payload["expected_repos"],
        "apache2_repos": payload["apache2_repos"],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    org_payload: ClassVar[Dict[str, Any]]
    repos_payload: ClassVar[List[Dict[str, Any]]]
    expected_repos: ClassVar[List[str]]
    apache2_repos: ClassVar[List[str]]

    @classmethod
    def setUpClass(cls):
        """Patch requests.get to mock GitHub API calls"""
        cls.get_patcher = patch('client.requests.get')
        mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            if url == cls.org_payload["repos_url"]:
                mock_resp = Mock()
                mock_resp.json.return_value = cls.repos_payload
                mock_resp.raise_for_status = Mock()
                return mock_resp
            elif url == f"https://api.github.com/orgs/{cls.org_payload['login']}":
                mock_resp = Mock()
                mock_resp.json.return_value = cls.org_payload
                mock_resp.raise_for_status = Mock()
                return mock_resp
            else:
                raise ValueError(f"Unexpected URL: {url}")

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repo names"""
        client = GithubOrgClient(self.org_payload["login"])
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test filtering repos with 'apache-2.0' license"""
        client = GithubOrgClient(self.org_payload["login"])
        apache2_repos = [
            repo["name"] for repo in self.repos_payload
            if GithubOrgClient.has_license(repo, "apache-2.0")
        ]
        self.assertEqual(apache2_repos, self.apache2_repos)
