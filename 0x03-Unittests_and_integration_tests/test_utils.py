#!/usr/bin/env python3
"""
Unit tests for utils.py functions and decorators
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test correct access of nested values."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError)
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_exception):
        """Test KeyError raised for invalid paths."""
        with self.assertRaises(expected_exception):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Tests for get_json function."""

    @patch('utils.requests.get')
    def test_get_json(self, mock_get):
        """Test that get_json returns correct JSON."""
        test_url = "http://example.com"
        expected_payload = {"payload": True}
        mock_get.return_value.json.return_value = expected_payload

        result = get_json(test_url)
        self.assertEqual(result, expected_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Tests for the memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches method results."""
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        obj = TestClass()

        # First call - calls a_method and caches result
        first_call = obj.a_property
        # Second call - should return cached result
        second_call = obj.a_property

        self.assertEqual(first_call, 42)
        self.assertEqual(second_call, 42)
        self.assertIs(first_call, second_call)


if __name__ == '__main__':
    unittest.main()
