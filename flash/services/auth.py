"""Mix-in classes for implementing service authentication."""
# pylint: disable=too-few-public-methods

from collections import OrderedDict


class TokenAuthMixin:
    """Mix-in class for implementing token authentication."""

    def __init__(self, *, api_token, **kwargs):
        self.api_token = api_token
        super().__init__(**kwargs)


class UrlParamMixin(TokenAuthMixin):
    """Mix-in class for implementing URL parameter authentication.

    Attributes:
      AUTH_PARAM (:py:class:`str`): The name of the URL parameter to
        supply the token as.

    """

    def url_builder(self, endpoint, params=None, url_params=None):
        """Add authentication URL parameter."""
        if url_params is None:
            url_params = OrderedDict()
        url_params[self.AUTH_PARAM] = self.api_token
        return super().url_builder(endpoint, params, url_params)


class HeaderMixin(TokenAuthMixin):
    """Mix-in class for implementing header authentication.

    Attributes:
      AUTH_HEADER: (:py:class:`str`) The name of the request header to
        supply the token as.

    """

    @property
    def headers(self):
        """Add authentication header."""
        return {self.AUTH_HEADER: self.api_token}
