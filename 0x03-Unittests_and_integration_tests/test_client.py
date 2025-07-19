#!/usr/bin/env python3
"""
Unit tests for the `client.GithubOrgClient` class.
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from typing import Dict
import requests

from unittest.mock import PropertyMock

from fixtures import TEST_PAYLOAD


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

    def test_public_repos_url(self) -> None:
        """
        Tests that `_public_repos_url` property returns the correct URL
        by mocking the `org` property.
        """
        known_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }
        with patch.object(
            GithubOrgClient,
            'org',
            new_callable=PropertyMock,
            return_value=known_payload
        ) as mock_org:
            client = GithubOrgClient("google")
            result = client._public_repos_url

            # Assert that the result is the expected URL from the payload
            self.assertEqual(result, known_payload["repos_url"])

            # Assert that the 'org' property was accessed
            mock_org.assert_called_once()

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: Mock) -> None:
        """
        Tests the `public_repos` method by mocking `get_json` and
        `_public_repos_url`.
        """
        # Define a sample payload for the repos API call
        repos_payload = [
            {"name": "repo-one"},
            {"name": "repo-two"},
            {"name": "repo-three"},
        ]
        # Configure the mock for get_json to return the sample payload
        mock_get_json.return_value = repos_payload

        # Define the expected list of repository names
        expected_repos = ["repo-one", "repo-two", "repo-three"]
        # Define a known URL for the public repos
        known_repos_url = "https://api.github.com/orgs/test/repos"

        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock,
            return_value=known_repos_url
        ) as mock_public_repos_url:

            client = GithubOrgClient("test")
            result = client.public_repos()

            # Assert the result is the expected list of repo names
            self.assertEqual(result, expected_repos)

            # Assert the mocked property and get_json were called once
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(known_repos_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(
        self,
        repo: Dict,
        license_key: str,
        expected: bool
    ) -> None:
        """
        Tests the `has_license` static method with different inputs to
        verify its boolean logic.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test suite for the `GithubOrgClient` class, using fixtures.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up the class by patching `requests.get` to return fixture data.
        """
        # Define the side effect for requests.get based on the URL
        def requests_get_side_effect(url: str):
            """
            Side effect function to mock `requests.get`.
            Returns a mock response with a json method that provides the
            appropriate fixture payload based on the requested URL.
            """
            # The URL for the repos payload is within the org_payload fixture
            repos_url = cls.org_payload.get("repos_url", "")

            # Determine which payload to return based on the URL
            if url.endswith("/orgs/google"):
                payload = cls.org_payload
            elif url == repos_url:
                payload = cls.repos_payload
            else:
                # Default to an empty dictionary if URL doesn't match
                payload = {}

            # Create a mock response object
            mock_response = Mock()
            mock_response.json.return_value = payload
            return mock_response

        # Start the patcher for requests.get
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()
        mock_get.side_effect = requests_get_side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Tear down the class by stopping the patcher.
        """
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """
        Integration test for the `public_repos` method.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """
        Integration test for `public_repos` with a license filter.
        """
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
    
