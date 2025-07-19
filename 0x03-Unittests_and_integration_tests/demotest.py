#!/usr/bin/env python3
"""
Unit tests for `utils.py` module.
"""
import unittest
from typing import Mapping, Sequence, Any
from parameterized import parameterized

from utils import access_nested_map


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