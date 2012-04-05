# -*- coding: utf-8 -*-
from spinrewriter import Api

import unittest2 as unittest
import mock


class TestApi(unittest.TestCase):

    def setUp(self):
        """Utility code shared among all tests."""
        self.api = Api('foo@bar.com', 'my_api_key')

    @mock.patch('spinrewriter.urllib2')
    def test_api_quota_call(self, urllib2):
        """Test if Api.api_quota() correctly parses the response it gets from
        SpinRewriter API.
        """

        # mock response from urllib2
        mocked_response = u"""{
            "status":"OK",
            "response":"You made 19 API requests in the last 24 hours. 81 still available.",
            "api_requests_made":19,"api_requests_available":81
        }"""
        urllib2.urlopen.return_value.read.return_value = mocked_response

        # call API
        result = self.api.api_quota()

        # test responses
        self.assertEquals(result['status'], u'OK')
        self.assertEquals(result['api_requests_made'], 19)
        self.assertEquals(result['api_requests_available'], 81)
        self.assertEquals(result['response'], u'You made 19 API requests in the last 24 hours. 81 still available.')

    @mock.patch('spinrewriter.urllib2')
    def test_text_with_spintax_call(self, urllib2):
        """Test if Api.text_with_spintax() correctly parses the response it gets
        from SpinRewriter API.
        """

        # mock response from urllib2
        mocked_response = u"""{
            "status":"OK",
            "response":"This is my {pet|animal|dog|cat} food.",
            "api_requests_made":20,
            "api_requests_available":80,
            "protected_terms":"food, cat",
            "nested_spintax":"false",
            "confidence_level":"medium"
        }"""
        urllib2.urlopen.return_value.read.return_value = mocked_response

        # call API
        result = self.api.text_with_spintax(
            text="This is my pet food.",
            protected_terms=['food', 'cat']
        )

        # test results
        self.assertEquals(result['status'], u'OK')
        self.assertEquals(result['api_requests_made'], 20)
        self.assertEquals(result['api_requests_available'], 80)
        self.assertEquals(result['protected_terms'], u"food, cat")
        self.assertEquals(result['nested_spintax'], u"false")
        self.assertEquals(result['confidence_level'], u"medium")
        self.assertEquals(result['response'], u"This is my {pet|animal|dog|cat} food.")

    @mock.patch('spinrewriter.urllib2')
    def test_unique_variation_call(self, urllib2):
        """Test if Api.unique_variation() correctly parses the response it gets
        from SpinRewriter API.
        """

        # mock response from urllib2
        mocked_response = u"""{
            "status":"OK",
            "response":"This is my animal food.",
            "api_requests_made":21,
            "api_requests_available":79,
            "protected_terms":"food, cat",
            "nested_spintax":"false",
            "confidence_level":"medium"
        }"""
        urllib2.urlopen.return_value.read.return_value = mocked_response

        # call API
        result = self.api.unique_variation(
            text="This is my pet food.",
            protected_terms=['food', 'cat']
        )

        # test results
        self.assertEquals(result['status'], u'OK')
        self.assertEquals(result['api_requests_made'], 21)
        self.assertEquals(result['api_requests_available'], 79)
        self.assertEquals(result['protected_terms'], u"food, cat")
        self.assertEquals(result['nested_spintax'], u"false")
        self.assertEquals(result['confidence_level'], u"medium")
        self.assertEquals(result['response'], u"This is my animal food.")

    @mock.patch('spinrewriter.urllib2')
    def test_transform_plain_text_call(self, urllib2):
        """Test if Api.transform_plain_text() correctly parses the response it
        gets from SpinRewriter API. This method is used by unique_variation()
        and text_with_spintax().
        """

        # mock response from urllib2
        mocked_response = u"""{
            "status":"OK",
            "response":"This is my animal food.",
            "api_requests_made":22,
            "api_requests_available":78,
            "protected_terms":"",
            "nested_spintax":"false",
            "confidence_level":"medium"
        }"""
        urllib2.urlopen.return_value.read.return_value = mocked_response

        # call API
        result = self.api._transform_plain_text(
            action=Api.ACTION.unique_variation,
            text="This is my pet food.",
            protected_terms=[],
            confidence_level=Api.CONFIDENCE_LVL.medium,
            nested_spintax=False,
            spintax_format=Api.SPINTAX_FORMAT.pipe_curly,
        )

        # test results
        self.assertEquals(result['status'], u'OK')
        self.assertEquals(result['api_requests_made'], 22)
        self.assertEquals(result['api_requests_available'], 78)
        self.assertEquals(result['protected_terms'], u"")
        self.assertEquals(result['nested_spintax'], u"false")
        self.assertEquals(result['confidence_level'], u"medium")
        self.assertEquals(result['response'], u"This is my animal food.")

    @mock.patch('spinrewriter.Api._send_request')
    def test_protected_terms_transformation(self, _send_request):
        """Test that protected_terms are correctly transformed into a string."""
        # prepare arguments for calling _transform_plain_text
        args = dict(
            action=Api.ACTION.unique_variation,
            text="This is my pet food.",
            protected_terms=['food', 'cat'],
            confidence_level=Api.CONFIDENCE_LVL.medium,
            nested_spintax=False,
            spintax_format=Api.SPINTAX_FORMAT.pipe_curly,
        )

        # we don't care what the response is
        _send_request.return_value = None

        # call it
        self.api._transform_plain_text(**args)

        # now test that protected_terms are in correct format
        _send_request.assert_called_with((
            ('email_address', 'foo@bar.com'),
            ('api_key', 'my_api_key'),
            ('action', 'unique_variation'),
            ('text', 'This is my pet food.'),
            ('protected_terms', 'food\ncat'),  # This is the only line we are interested in here, it needs to be newline-separated
            ('confidence_level', 'medium'),
            ('nested_spintax', False),
            ('spintax_format', '{|}'),
        ))

    @mock.patch('spinrewriter.Api._send_request')
    def test_protected_terms_empty(self, _send_request):
        """Test that correct default value is set for protected_terms if the
        list is empty."""
        # prepare arguments for calling _transform_plain_text
        args = dict(
            action=Api.ACTION.unique_variation,
            text="This is my pet food.",
            protected_terms=[],
            confidence_level=Api.CONFIDENCE_LVL.medium,
            nested_spintax=False,
            spintax_format=Api.SPINTAX_FORMAT.pipe_curly,
        )

        # we don't care what the response is
        _send_request.return_value = None

        # call it
        self.api._transform_plain_text(**args)

        # now test that protected_terms are in correct format
        _send_request.assert_called_with((
            ('email_address', 'foo@bar.com'),
            ('api_key', 'my_api_key'),
            ('action', 'unique_variation'),
            ('text', 'This is my pet food.'),
            ('protected_terms', ''),  # This is the only line we are interested in here, it needs to be an empty string, not an empty list
            ('confidence_level', 'medium'),
            ('nested_spintax', False),
            ('spintax_format', '{|}'),
        ))
