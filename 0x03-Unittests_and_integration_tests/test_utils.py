#!/usr/bin/env python3
"""
Unit tests for `utils.py` module.
"""
import unittest
from typing import Mapping, Sequence, Any, Dict
from parameterized import parameterized

from utils import access_nested_map

from unittest.mock import patch, Mock
from utils import get_json

from utils import memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    Test suite for the `access_nested_map` function.
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
        self,
        nested_map: Mapping,
        path: Sequence,
        expected: Any
    ) -> None:
        """
        Tests `access_nested_map` for expected output with valid inputs.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(
        self,
        nested_map: Mapping,
        path: Sequence,
        expected_exception: Exception
    ) -> None:
        """
        Tests that `access_nested_map` raises a KeyError for invalid paths.
        """
        with self.assertRaises(expected_exception):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    Test suite for the `get_json` function.
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(
        self,
        test_url: str,
        test_payload: Dict,
        mock_get: Mock
    ) -> None:
        """
        Tests that `get_json` returns the expected result by mocking
        HTTP calls.
        """
        # Configure the mock's return value
        mock_get.return_value.json.return_value = test_payload

        # Call the function under test
        result = get_json(test_url)

        # Assert that the mocked get method was called once with the correct URL
        mock_get.assert_called_once_with(test_url)

        # Assert that the output of get_json is equal to the test_payload
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Test suite for the `memoize` decorator.
    """
    def test_memoize(self) -> None:
        """
        Tests that the `memoize` decorator caches the result of a method,
        ensuring the underlying method is called only once.
        """
        class TestClass:
            """A test class to demonstrate memoization."""

            def a_method(self):
                """A simple method that returns a fixed value."""
                return 42

            @memoize
            def a_property(self):
                """A property that uses memoization to cache a_method's result."""
                return self.a_method()

        with patch.object(
            TestClass,
            'a_method',
            return_value=42
        ) as mock_a_method:
            test_instance = TestClass()

            # Access the property twice
            self.assertEqual(test_instance.a_property, 42)
            self.assertEqual(test_instance.a_property, 42)

            # Assert that the mocked method was called only once
            mock_a_method.assert_called_once()