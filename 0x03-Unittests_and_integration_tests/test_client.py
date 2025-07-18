#!/usr/bin/env python3
"""Test for GithubOrgClient"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns correct data,
        and get_json is called once with the correct URL.
        """

        # Mocked JSON response for the org
        expected_payload = {"login": org_name, "id": 1234}

        # Setup mock to return expected_payload without calling real get_json
        mock_get_json.return_value = expected_payload

        # Create a GithubOrgClient instance with the org name
        client = GithubOrgClient(org_name)

        # Call the .org property/method
        result = client.org

        # Assert .org returns the mocked data
        self.assertEqual(result, expected_payload)

        # Assert get_json was called once with the correct GitHub API URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
