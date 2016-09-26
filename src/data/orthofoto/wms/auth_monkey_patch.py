import requests
import owslib.util

from owslib.etree import etree, ParseError
from owslib.util import ResponseWrapper, ServiceException
from owslib.util import openURL


class AuthMonkeyPatch:
    def __init__(self, auth):
        self.auth = auth
        self._set_monkey_patch(auth)

    def _set_monkey_patch(self, auth):
        if auth is not None:
            owslib.util.openURL = self._open_url
        else:
            owslib.util.openURL = openURL

    def _open_url(self, url_base, data=None, method='Get', cookies=None, username=None, password=None, timeout=30,
                  headers=None):
        headers = headers if headers is not None else {}
        kwargs = dict(timeout=timeout)

        kwargs['auth'] = self.auth

        method = method.split("}")[-1]

        if method.lower() == 'post':
            try:
                _ = etree.fromstring(data)
                headers['Content-Type'] = 'text/xml'
            except (ParseError, UnicodeEncodeError):
                pass

            kwargs['data'] = data

        elif method.lower() == 'get':
            kwargs['params'] = data

        else:
            raise ValueError("Unknown method ('%s'), expected 'get' or 'post'" % method)

        if cookies is not None:
            kwargs['cookies'] = cookies

        req = requests.request(method.upper(), url_base, headers=headers, **kwargs)

        if req.status_code in [400, 401]:
            raise ServiceException(req.text)

        if req.status_code in [404]:  # add more if needed
            req.raise_for_status()

        if 'Content-Type' in req.headers and req.headers['Content-Type'] in ['text/xml', 'application/xml']:
            se_tree = etree.fromstring(req.content)
            serviceException = se_tree.find('{http://www.opengis.net/ows}Exception')
            if serviceException is None:
                serviceException = se_tree.find('ServiceException')
            if serviceException is not None:
                raise ServiceException(str(serviceException.text).strip())

        return ResponseWrapper(req)
