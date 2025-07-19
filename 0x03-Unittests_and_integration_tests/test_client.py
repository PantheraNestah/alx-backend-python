#!/usr/bin/env python3
"""
Unit tests for the `client.GithubOrgClient` class.
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient
from typing import Dict


class TestGithubOrgClient(unittest.TestCase):
    """
    Test suite for the `GithubOrgClient` class.
    """
    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch('client.get_json')
    def test_org(
        self,
        org_name: str,
        expected_payload: Dict,
        mock_get_json: Mock
    ) -> None:
        """
        Tests that `GithubOrgClient.org` returns the correct value and
        that `get_json` is called exactly once with the expected URL.
        """
        # Configure the mock to return the predefined payload
        mock_get_json.return_value = expected_payload

        # Instantiate the client
        client = GithubOrgClient(org_name)

        # Call the property under test
        result = client.org

        # Assert that the result matches the expected payload
        self.assertEqual(result, expected_payload)

        # Construct the expected URL and assert get_json was called with it
        expected_url = GithubOrgClient.ORG_URL.format(org=org_name)
        mock_get_json.assert_called_once_with(expected_url)