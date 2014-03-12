# -*- coding: utf-8 -*-
from spinrewriter import Api
from spinrewriter import SpinRewriter
from spinrewriter import exceptions as ex

import unittest2 as unittest
import mock


class TestApi(unittest.TestCase):

    def setUp(self):
        """Utility code shared among all tests."""
        self.sr = SpinRewriter('foo@bar.com', 'test_api_key')

    def test_init(self):
        """Test initialization of SpinRewriter.

        SpinRewriter is initialized on every test run and stored as self.sr.
        We need to test for stored values and if underlying Api class was
        also initialized correctly.
        """
        self.assertEquals(self.sr.email_address, 'foo@bar.com')
        self.assertEquals(self.sr.api_key, 'test_api_key')
        self.assertIsInstance(self.sr.api, Api)

    @mock.patch('spinrewriter.urllib2')
    def test_unique_variation_default_call(self, urllib2):
        """Test call of unique_variation() with default values."""
        # mock response from SpinRewriter
        mocked_response = u"""{
            "status":"OK",
            "response":"This is my pet.",
            "api_requests_made":1,
            "api_requests_available":99,
            "protected_terms":"",
            "nested_spintax":"false",
            "confidence_level":"medium"
        }"""
        urllib2.urlopen.return_value.read.return_value = mocked_response

        # test call
        self.assertEquals(
            self.sr.unique_variation('This is my dog.'),
            'This is my pet.',
        )

    @mock.patch('spinrewriter.urllib2')
    def test_text_with_spintax_default_call(self, urllib2):
        """Test call of text_with_spintax_call() with default values."""
        # mock response from SpinRewriter
        mocked_response = u"""{
            "status":"OK",
            "response":"This is my {dog|pet|animal}.",
            "api_requests_made":2,
            "api_requests_available":98,
            "protected_terms":"",
            "nested_spintax":"false",
            "confidence_level":"medium"
        }"""
        urllib2.urlopen.return_value.read.return_value = mocked_response

        # test call
        self.assertEquals(
            self.sr.text_with_spintax('This is my dog.'),
            'This is my {dog|pet|animal}.',
        )

    @mock.patch('spinrewriter.urllib2')
    def test_text_with_spintax_error(self, urllib2):
        # mock response from SpinRewriter
        mocked_response = u"""{"status":"ERROR", "response":"Authentication failed. Unique API key is not valid for this user."}"""  # noqa
        urllib2.urlopen.return_value.read.return_value = mocked_response

        # test call
        with self.assertRaises(ex.AuthenticationError):
            self.sr.text_with_spintax('This is my dog.')

    @mock.patch('spinrewriter.urllib2')
    def test_unique_variation_error(self, urllib2):
        # mock response from SpinRewriter
        mocked_response = u"""{"status":"ERROR", "response":"Authentication failed. Unique API key is not valid for this user."}"""  # noqa
        urllib2.urlopen.return_value.read.return_value = mocked_response

        # test call
        with self.assertRaises(ex.AuthenticationError):
            self.sr.unique_variation('This is my dog.')
