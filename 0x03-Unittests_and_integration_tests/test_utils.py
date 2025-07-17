"""Unit tests for utility functions in utils.py"""

import unittest
from unittest.mock import patch
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    def test_access_nested_map(self):
        self.assertEqual(
            access_nested_map({"a": {"b": 2}}, ["a", "b"]),
            2
        )

    def test_access_nested_map_with_key_error(self):
        with self.assertRaises(KeyError):
            access_nested_map({}, ["a"])

        with self.assertRaises(KeyError):
            access_nested_map({"a": 1}, ["a", "b"])


class TestGetJson(unittest.TestCase):
    @patch("utils.requests.get")
    def test_get_json(self, mock_get):
        mock_get.return_value.json.return_value = {"payload": True}
        result = get_json("http://example.com")
        self.assertEqual(result, {"payload": True})
        mock_get.assert_called_once_with("http://example.com")


class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        class TestClass:
            def __init__(self):
                self.call_count = 0

            @memoize
            def a_method(self):
                self.call_count += 1
                return 42

        obj = TestClass()

        first_call = obj.a_method()
        second_call = obj.a_method()

        self.assertEqual(first_call, 42)
        self.assertEqual(second_call, 42)
        self.assertEqual(obj.call_count, 1)
