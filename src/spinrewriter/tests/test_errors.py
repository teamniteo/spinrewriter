# -*- coding: utf-8 -*-
from spinrewriter import Api
from spinrewriter import exceptions as ex
import unittest2 as unittest


class TestErrors(unittest.TestCase):

    def setUp(self):
        """Utility code shared among all tests."""
        self.api = Api('foo@bar.com', 'test_api_key')

    def test_parsing_error_messages(self):
        """Go through all possible error messages and see that they are parsed
        correctly.
        """

        msg = u'Authentication with Spin Rewriter API failed.'
        with self.assertRaises(ex.AuthenticationError) as cm:
            self.api._raise_error(
                {'response': 'Authentication failed. Unique API key is not '
                             'valid for this user.'})
        self.assertEqual(msg, str(cm.exception))

        with self.assertRaises(ex.AuthenticationError) as cm:
            self.api._raise_error(
                {'response': 'Authentication failed. No user with this email '
                             'address found.'})
        self.assertEqual(msg, str(cm.exception))

        with self.assertRaises(ex.AuthenticationError) as cm:
            self.api._raise_error(
                {'response': 'This user does not have a valid Spin Rewriter '
                             'subscription.'})
        self.assertEqual(msg, str(cm.exception))

        msg = u'Quota limit for API calls reached.'
        with self.assertRaises(ex.QuotaLimitError) as cm:
            self.api._raise_error(
                {'response': 'API quota exceeded. You can make 50 requests '
                             'per day.'})
        self.assertEqual(msg, str(cm.exception))

        msg = u'Not enough time passed since last API request.'
        with self.assertRaises(ex.UsageFrequencyError) as cm:
            self.api._raise_error(
                {'response': 'You can only submit entirely new text for '
                             'analysis once every 5 seconds.'})
        self.assertEqual(msg, str(cm.exception))

        msg = u'Unknown API action requested.'
        with self.assertRaises(ex.UnknownActionError) as cm:
            self.api._raise_error(
                {'response': 'Requested action does not exist. Please refer '
                             'to the Spin Rewriter API documentation.'})
        self.assertEqual(msg, str(cm.exception))

        msg = u'Required parameter not present in API request.'
        with self.assertRaises(ex.MissingParameterError) as cm:
            self.api._raise_error(
                {'response': 'Email address and unique API key are both '
                             'required. At least one is missing.'})
        self.assertEqual(msg, str(cm.exception))

        msg = u'Invalid parameter value passed to API.'
        with self.assertRaises(ex.ParamValueError) as cm:
            self.api._raise_error(
                {'response': 'Original text too short.'})
        self.assertEqual(msg, str(cm.exception))

        with self.assertRaises(ex.ParamValueError) as cm:
            self.api._raise_error(
                {'response': 'Original text too long. '
                             'Text can have up to 4,000 words.'})
        self.assertEqual(msg, str(cm.exception))

        with self.assertRaises(ex.ParamValueError) as cm:
            self.api._raise_error(
                {'response': 'Original text after analysis too long. '
                             'Text can have up to 4,000 words.'})
        self.assertEqual(msg, str(cm.exception))

        with self.assertRaises(ex.ParamValueError) as cm:
            self.api._raise_error(
                {'response': 'Spinning syntax invalid. With this action you '
                             'should provide text with existing valid '
                             '{first option|second option} spintax.'})
        self.assertEqual(msg, str(cm.exception))

        with self.assertRaises(ex.ParamValueError) as cm:
            self.api._raise_error(
                {'response': 'The {first|second} spinning syntax invalid. '
                             'Re-check the syntax, i.e. '
                             'curly brackets and pipes.'})
        self.assertEqual(msg, str(cm.exception))

        with self.assertRaises(ex.ParamValueError) as cm:
            self.api._raise_error(
                {'response': 'Spinning syntax invalid.'})
        self.assertEqual(msg, str(cm.exception))

        msg = u'Internal error occured on API server when processing request.'
        with self.assertRaises(ex.InternalApiError) as cm:
            self.api._raise_error(
                {'response': 'Analysis of your text failed. '
                             'Please inform us about this.'})
        self.assertEqual(msg, str(cm.exception))

        with self.assertRaises(ex.InternalApiError) as cm:
            self.api._raise_error(
                {'response': 'Synonyms for your text could not be loaded. '
                             'Please inform us about this.'})
        self.assertEqual(msg, str(cm.exception))

        with self.assertRaises(ex.InternalApiError) as cm:
            self.api._raise_error(
                {'response': 'Unable to load your new analyzed project.'})
        self.assertEqual(msg, str(cm.exception))

        with self.assertRaises(ex.InternalApiError) as cm:
            self.api._raise_error(
                {'response': 'Unable to load your existing analyzed project.'})
        self.assertEqual(msg, str(cm.exception))

        with self.assertRaises(ex.InternalApiError) as cm:
            self.api._raise_error(
                {'response': 'Unable to find your project in the database.'})
        self.assertEqual(msg, str(cm.exception))

        with self.assertRaises(ex.InternalApiError) as cm:
            self.api._raise_error(
                {'response': 'Unable to load your analyzed project.'})
        self.assertEqual(msg, str(cm.exception))

        with self.assertRaises(ex.InternalApiError) as cm:
            self.api._raise_error(
                {'response': 'One-Click Rewrite failed.'})
        self.assertEqual(msg, str(cm.exception))

        msg = u'Unrecognized API error message received: foo'
        with self.assertRaises(ex.UnknownApiError) as cm:
            self.api._raise_error(
                {'response': 'foo'})
        self.assertEqual(msg, str(cm.exception))
