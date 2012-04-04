# -*- coding: utf-8 -*-

import json
import urllib
import urllib2

from collections import namedtuple


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class AuthenticationError(Error): #TODO: needed?
    """
    Raised when authentication error encountered
    """
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __str__(self):
        return u"Could not authenticate with username: %s and password: %s." % (self.username, self.password) #TODO: change


class QuotaUsedError(Error):  #TODO: needed?
    """
    Raised when API quota limit reached (250 queries per day)
    """
    def __str__(self):
        return u"The Best Spinner API query limit has been reached for today (250 queries per day)." #TODO: change

#TODO: get list of error messages so that we know, what to handle ...


class Api(object):
    """
    A class to use Spin Rewriter API (http://www.spinrewriter.com/)
    """

    _tmp_list = ['api_quota', 'text_with_spintax', 'unique_variation', 'unique_variation_from_spintax']
    ACTION = namedtuple('ACTION', _tmp_list)(*_tmp_list)
    """
    collection of all service names (passed as the "action" parameter upon service invocation)
    """

    CONFIDENCE_LEVEL = namedtuple('CONFIDENCE_LEVEL', ['low', 'medium', 'high'])(*range(3))
    """
    TODO: describe
    """

    SPINTAX_FORMAT = namedtuple('SPINTAX_FORMAT', ['pipe_curly', 'tilde_curly', 'pipe_square', 'spin_tag'])(*['{|}', '{~}', '[|]', '[spin]'])
    """
    TODO: describe
    """

    _tmp_list = ['email_address', 'api_key', 'action', 'text', 'protected_terms',
                 'confidence_level', 'nested_spintax', 'spintax_format']
    REQ_P_NAMES = namedtuple('REQ_P_NAMES', _tmp_list)(*_tmp_list)
    """ email_address:
        api_key:
        action : ACTION
        text:
        protected_terms:
        confidence_level: CONFIDENCE_LEVEL
        nested_spintax: (default false)
        spintax_format: SPINTAX_FORMAT
    """

    _tmp_list = ['status', 'response', 'api_requests_made', 'api_requests_available', 'protected_terms', 'confidence_level']
    RESP_P_NAMES = namedtuple('RESP_P_NAMES', _tmp_list)(*_tmp_list)
    """ status:
        response:
        api_requests_made:
        api_requests_available:
        protected_terms:
        confidence_level:
    """

    def __init__(self, email_address, api_key):
        self.url = 'http://www.spinrewriter.com/action/api'
        self.email_address = email_address
        self.api_key = api_key


    def _send_request(self, params):
        """
        TODO:
        params:
        type: ReqParams
        """
        #TODO: try-except ...
        #The urllib.urlencode() function takes a mapping or sequence of 2-tuples
        con = urllib2.urlopen(self.url, urllib.urlencode(params))  #TODO: this urlencode OK? or convert to anonymous tuple or something?
        response = con.read() #con is a file-like object

        #TODO: json decode response and return it as a dict or smth
        return json.loads(response)


    def api_quota(self):
        """ Return number of API requests left for today for this user.

            :returns: Number of API requests left for today.
            :rtype: int

            TODO: docstring and error handling
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
        """ TODO: docstring and error handling

        """
        response = self._get_plain_text_transformed(self.ACTION.text_with_spintax, text, protected_terms, confidence_level,
                                                    nested_spintax, spintax_format)
        return response


    def unique_variation(self, text, protected_terms=None, confidence_level=CONFIDENCE_LEVEL.medium,
                         nested_spintax=False, spintax_format=SPINTAX_FORMAT.pipe_curly):
        """ TODO: docstring and error handling

        """
        response = self._get_plain_text_transformed(self.ACTION.unique_variation, text, protected_terms, confidence_level,
                                                    nested_spintax, spintax_format)
        return response


    def _get_plain_text_transformed(self, action, text, protected_terms, confidence_level,
                                    nested_spintax, spintax_format):
        """ TODO: helper function

        """
        #NOTE: could be improved to optionally include some optional params (if not set ... default would be None),
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
        """ TODO: docstring and error handling

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
