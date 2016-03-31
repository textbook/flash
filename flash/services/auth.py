class UrlParamMixin:

    def _url_builder(self, endpoint, params=None, url_params=None):
        if url_params is None:
            url_params = {}
        url_params['api_key'] = self.api_token
        return super()._url_builder(endpoint, params, url_params)


class HeaderMixin:

    @property
    def headers(self):
        return {self.AUTH_HEADER: self.api_token}
