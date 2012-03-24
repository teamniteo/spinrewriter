class SpinRewriter(object):
    """TODO"""

    def __init__(self, username, api_key, url=None):

        self.url = url or 'http://www.spinrewriter.com/action/api'
        self.username = username
        self.api_key = api_key

    def text_with_spintax(text):
        raise NotImplemented

    def unique_variation(text):
        raise NotImplemented
