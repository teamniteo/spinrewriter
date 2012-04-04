# -*- coding: utf-8 -*-

import json
import urllib
import urllib2

from collections import namedtuple


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class AuthenticationError(Error):  # TODO: needed?
    """
    Raised when authentication error encountered
    """
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __str__(self):
        return u"Could not authenticate with username: %s and password: %s." % (self.username, self.password)  # TODO: change


class QuotaUsedError(Error):  # TODO: needed?
    """
    Raised when API quota limit reached (250 queries per day)
    """
    def __str__(self):
        return u"The Best Spinner API query limit has been reached for today (250 queries per day)."  # TODO: change


#TODO: get list of error messages so that we know, what to handle ...


class Api(object):
    """
    A class representing the Spin Rewriter API (http://www.spinrewriter.com/)
    """
    _tmp_list = ['api_quota', 'text_with_spintax', 'unique_variation', 'unique_variation_from_spintax']
    ACTION = namedtuple('ACTION', _tmp_list)(*_tmp_list)
    """
    collection of possible values for the action parameter
    """

    CONFIDENCE_LEVEL = namedtuple('CONFIDENCE_LEVEL', ['low', 'medium', 'high'])(*range(3))
    """
    collection of possible values for the confidence_level parameter
    """

    SPINTAX_FORMAT = namedtuple('SPINTAX_FORMAT', ['pipe_curly', 'tilde_curly', 'pipe_square', 'spin_tag'])(*['{|}', '{~}', '[|]', '[spin]'])
    """
    collection of possible values for the spintax_format parameter
    """

    _tmp_list = ['email_address', 'api_key', 'action', 'text', 'protected_terms',
                 'confidence_level', 'nested_spintax', 'spintax_format']
    REQ_P_NAMES = namedtuple('REQ_P_NAMES', _tmp_list)(*_tmp_list)
    """ collection of all request parameters' names """

    _tmp_list = ['status', 'response', 'api_requests_made', 'api_requests_available', 'protected_terms', 'confidence_level']
    RESP_P_NAMES = namedtuple('RESP_P_NAMES', _tmp_list)(*_tmp_list)
    """ collection of all response fields' names """

    def __init__(self, email_address, api_key):
        self.url = 'http://www.spinrewriter.com/action/api'
        self.email_address = email_address
        self.api_key = api_key

    def _send_request(self, params):
        """ Invoke Spin Rewriter API with given parameters and return its response .

            :param params: parameters to pass along with the request
            :type params: tuple of 2-tuples

            :return: API's response (already JSON-decoded)
            :rtype: dictionary
        """
        con = urllib2.urlopen(self.url, urllib.urlencode(params))
        response = con.read()
        return json.loads(response)

    def api_quota(self):
        """ Return the number of made and remaining API calls for the 24-hour period.

            :return: remaining API quota
            :rtype: dictionary
        """
        params = (
            (self.REQ_P_NAMES.email_address, self.email_address),
            (self.REQ_P_NAMES.api_key, self.api_key),
            (self.REQ_P_NAMES.action, self.ACTION.api_quota),
        )
        response = self._send_request(params)
        return response

    def text_with_spintax(self, text, protected_terms=None, confidence_level=CONFIDENCE_LEVEL.medium,
                          nested_spintax=False, spintax_format=SPINTAX_FORMAT.pipe_curly):
        """ Return processed spun text with spintax.

            :param text: original text that needs to be changed
            :type text: string
            :param protected_terms: (optional) keywords and key phrases that should be left intact
            :type protected_terms: list of strings
            :param confidence_level: (optional) the confidence level of the One-Click Rewrite process
            :type confidence_level: string
            :param nested_spintax: (optional) whether or not to also spin single words inside already spun phrases
            :type nested_spintax: boolean
            :param spintax_format: (optional) spintax format to use in returned text
            :type spintax_format: string

            :return: processed text and some other meta info
            :rtype: dictionary
        """
        response = self._get_plain_text_transformed(self.ACTION.text_with_spintax, text, protected_terms, confidence_level,
                                                    nested_spintax, spintax_format)
        return response

    def unique_variation(self, text, protected_terms=None, confidence_level=CONFIDENCE_LEVEL.medium,
                         nested_spintax=False, spintax_format=SPINTAX_FORMAT.pipe_curly):
        """ Return a unique variation of the given text.

            :param text: original text that needs to be changed
            :type text: string
            :param protected_terms: (optional) keywords and key phrases that should be left intact
            :type protected_terms: list of strings
            :param confidence_level: (optional) the confidence level of the One-Click Rewrite process
            :type confidence_level: string
            :param nested_spintax: (optional) whether or not to also spin single words inside already spun phrases
            :type nested_spintax: boolean
            :param spintax_format: (optional) (probably not relevant here? But API documentation not clear here ...)
            :type spintax_format: string

            :return: processed text and some other meta info
            :rtype: dictionary
        """
        response = self._get_plain_text_transformed(self.ACTION.unique_variation, text, protected_terms, confidence_level,
                                                    nested_spintax, spintax_format)
        return response

    def _get_plain_text_transformed(self, action, text, protected_terms, confidence_level,
                                    nested_spintax, spintax_format):
        """ Pack parameters into format as expected by the _send_request method invoke that method.

            :param action: name of the action that will be requestd from API
            :type action: string
            :param text: text to process
            :type text: string
            :param protected_terms: keywords and key phrases that should be left intact
            :type protected_terms: list of strings
            :param confidence_level: the confidence level of the One-Click Rewrite process
            :type confidence_level: string
            :param nested_spintax: whether or not to also spin single words inside already spun phrases
            :type nested_spintax: boolean
            :param spintax_format: spintax format to use in returned text
            :type spintax_format: string

            :return: processed text and some other meta info
            :rtype: dictionary
        """
        #NOTE: this could be improved to conditionally include some optional params (their default values would be None),
        #but it's only a minor optimization and would make code a bit more complicated
        protected_terms = "\n".join(protected_terms) if protected_terms else []

        params = (
            (self.REQ_P_NAMES.email_address, self.email_address),
            (self.REQ_P_NAMES.api_key, self.api_key),
            (self.REQ_P_NAMES.action, action),
            (self.REQ_P_NAMES.text, text),
            (self.REQ_P_NAMES.protected_terms, protected_terms),
            (self.REQ_P_NAMES.confidence_level, confidence_level),
            (self.REQ_P_NAMES.nested_spintax, nested_spintax),
            (self.REQ_P_NAMES.spintax_format, spintax_format),
        )
        return self._send_request(params)

    def unique_variation_from_spintax(self, text, nested_spintax=False, spintax_format=SPINTAX_FORMAT.pipe_curly):
        """ Return a unique variation of an already spun text.

            :param text: text to process
            :type text: string
            :param nested_spintax: whether or not to also spin single words inside already spun phrases
            :type nested_spintax: boolean
            :param spintax_format: (probably not relevant here? But API documentation not clear here ...)
            :type spintax_format: string

            :return: processed text and some other meta info
            :rtype: dictionary
        """
        params = (
            (self.REQ_P_NAMES.email_address, self.email_address),
            (self.REQ_P_NAMES.api_key, self.api_key),
            (self.REQ_P_NAMES.action, self.ACTION.unique_variation_from_spintax),
            (self.REQ_P_NAMES.text, text),
            (self.REQ_P_NAMES.nested_spintax, nested_spintax),
            (self.REQ_P_NAMES.spintax_format, spintax_format),
        )
        response = self._send_request(params)
        return response
