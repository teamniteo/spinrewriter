# -*- coding: utf-8 -*-


class SpinRewriterApiError(Exception):
    """Base class for exceptions in Spin Rewriter module."""
    def __init__(self, api_error_msg):
        #api_error_msg respresents raw error string as returned by API server
        super(SpinRewriterApiError, self).__init__()
        self.api_error_msg = api_error_msg


class AuthenticationError(SpinRewriterApiError):
    """Raised when authentication error occurs."""
    def __str__(self):
        return u"Authentication with Spin Rewriter API failed."


class QuotaLimitError(SpinRewriterApiError):
    """Raised when API quota limit is reached."""
    def __str__(self):
        return u"Quota limit for API calls reached."


class UsageFrequencyError(SpinRewriterApiError):
    """Raised when subsequent API requests are made in a too short time interval."""
    def __str__(self):
        return u"Not enough time passed since last API request."


class UnknownActionError(SpinRewriterApiError):
    """Raised when unknown API action is requested."""
    def __str__(self):
        return u"Unknown API action requested."


class MissingParameterError(SpinRewriterApiError):
    """Raised when required parameter is not provided."""
    def __str__(self):
        return u"Required parameter not present in API request."


class ParamValueError(SpinRewriterApiError):
    """Raised when parameter passed to API call has an invalid value."""
    def __str__(self):
        return u"Invalid parameter value passed to API."


class InternalApiError(SpinRewriterApiError):
    """Raised when unexpected error occurs on the API server when processing a request."""
    def __str__(self):
        return u"Internal error occured on API server when processing request."


class UnknownApiError(SpinRewriterApiError):
    """Raised when API call results in an unrecognized error."""
    def __str__(self):
        return u"Unknown Api Message: {0}".format(self.api_error_msg)
