from __future__ import unicode_literals

import json

import requests

from chive import exceptions

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

class Base(object):
    def __init__(self, base_url='https://api.coin-hive.com/',
                 verify=True, timeout=30, proxies=None,
                 allow_redirects=True, session=None):

        if not session:
            session = requests.Session()

        self.allow_redirects = allow_redirects
        self.session = session

        self._base_url = base_url
        self._kwargs = {
            'verify': verify,
            'timeout': timeout,
            'proxies': proxies,
        }
    def read(self, path, wrap_ttl=None):
        """
        GET /<path>
        """
        try:
            return self._get('{0}'.format(path), wrap_ttl=wrap_ttl).json()
        except exceptions.InvalidPath:
            return None

    def close(self):
        """
        Close the underlying Requests session
        """
        self.session.close()

    def _get(self, url, **kwargs):
        return self.__request('get', url, **kwargs)

    def _post(self, url, **kwargs):
        return self.__request('post', url, **kwargs)

    def _put(self, url, **kwargs):
        return self.__request('put', url, **kwargs)

    def _delete(self, url, **kwargs):
        return self.__request('delete', url, **kwargs)

    def __request(self, method, url, headers=None, **kwargs):
        url = urljoin(self._base_url, url)

        if not headers:
            headers = {}

        wrap_ttl = kwargs.pop('wrap_ttl', None)

        _kwargs = self._kwargs.copy()
        _kwargs.update(kwargs)

        response = self.session.request(method, url, headers=headers,
                                        allow_redirects=False, **_kwargs)

        while response.is_redirect and self.allow_redirects:
            url = urljoin(self._base_url, response.headers['Location'])
            response = self.session.request(method, url, headers=headers,
                                            allow_redirects=False, **_kwargs)

        if response.status_code >= 400 and response.status_code < 600:
            text = errors = None
            if response.headers.get('Content-Type') == 'application/json':
                errors = response.json().get('errors')
            if errors is None:
                text = response.text
            self.__raise_error(response.status_code, text, errors=errors)

        return response

    def __raise_error(self, status_code, message=None, errors=None):
        if status_code == 400:
            raise exceptions.InvalidRequest(message, errors=errors)
        elif status_code == 401:
            raise exceptions.Unauthorized(message, errors=errors)
        elif status_code == 403:
            raise exceptions.Forbidden(message, errors=errors)
        elif status_code == 404:
            raise exceptions.InvalidPath(message, errors=errors)
        elif status_code == 429:
            raise exceptions.RateLimitExceeded(message, errors=errors)
        elif status_code == 500:
            raise exceptions.InternalServerError(message, errors=errors)
        elif status_code == 501:
            raise exceptions.VaultNotInitialized(message, errors=errors)
        elif status_code == 503:
            raise exceptions.VaultDown(message, errors=errors)
        else:
            raise exceptions.UnexpectedError(message)

class Stats(Base):
    def __init__(self, secret, **kwargs):
        self._secret = secret
        super(Stats, self).__init__(**kwargs)

    def payout(self):
        '''Return the pure JSON-parsed object from requesting payout
        '''
        try:
            return self._get('stats/payout', params={
                'secret': self._secret
            }).json()
        except exceptions.InvalidPath:
            return None

    def site(self):
        '''Return the pure JSON-parsed object from requesting site status
        '''
        try:
            return self._get('stats/site', params={
                'secret': self._secret
            }).json()
        except exceptions.InvalidPath:
            return None
