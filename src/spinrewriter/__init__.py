class SpinRewriter(object):
    """TODO"""

    def __init__(self, username, api_key, url=None):
        """Initialization of the SpinRewriter API bindings.

        :param username: Your SpinRewriter username.
        :type properties: string

        :param api_key: Your SpinRewriter API key.
        :type properties: string
        """

        self.url = url or 'http://www.spinrewriter.com/action/api'
        self.username = username
        self.api_key = api_key

    def api_quota(self):
        """Return number of API requests left for today for this user.

        :returns: Number of API requests left for today.
        :rtype: int
        """

    def text_with_spintax(text):
        raise NotImplemented

    def unique_variation(text):
        raise NotImplemented
