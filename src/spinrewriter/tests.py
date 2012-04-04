# -*- coding: utf-8 -*-
from spinrewriter import Api

import unittest2 as unittest
import mock


class TestApi(unittest.TestCase):

    @mock.patch('spinrewriter.urllib2')
    def test_api_quota(self, urllib2):
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
        api = Api('foo@bar.com', 'my_api_key')
        result = api.api_quota()

        # test responses
        self.assertEquals(result['status'], u'OK')
        self.assertEquals(result['api_requests_made'], 19)
        self.assertEquals(result['api_requests_available'], 81)
        self.assertEquals(result['response'], u'You made 19 API requests in the last 24 hours. 81 still available.')

    @mock.patch('spinrewriter.urllib2')
    def text_with_spintax(self, urllib2):
        """Test if Api.text_with_spintax() correctly parses the response it gets
        from SpinRewriter API.
        """

        # mock response from urllib2
        mocked_response = u"""{
            "status":"OK",
            "response":"This is my {little|limited|minimal} {pet|animal|dog|cat} {who|that} {read|checked out|reviewed|went over|went through|studied} {an article|a write-up|a post|a blog|a piece} {about|regarding|concerning|pertaining to|relating to} {animal|cat|pet} food.",
            "api_requests_made":20,
            "api_requests_available":80,
            "protected_terms":"food, cat",
            "nested_spintax":"false",
            "confidence_level":"medium"
        }"""
        urllib2.urlopen.return_value.read.return_value = mocked_response

        # call API
        api = Api('foo@bar.com', 'my_api_key')
        result = api.text_with_spintax(
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
    def unique_variation(self, urllib2):
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
        api = Api('foo@bar.com', 'my_api_key')
        result = api.unique_variation(
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
