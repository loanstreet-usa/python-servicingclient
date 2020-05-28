import json
import logging
import platform
from http.client import HTTPResponse
from ssl import SSLContext
from typing import Optional, Dict
from urllib.error import HTTPError
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen
from uuid import UUID

import sys

from ..errors import ServicingRequestError
from ..version import __version__
from .servicing_response import ServicingResponse


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


class BaseClient:
    BASE_URL = "https://api.loan-street.com:8443/"

    def __init__(
        self,
        token=None,
        base_url=BASE_URL,
        headers: Optional[dict] = None,
        ssl: Optional[SSLContext] = None,
    ):
        self.token = None if token is None else token.strip()
        self.base_url = base_url
        self.headers = headers or {}
        self.ssl = ssl
        self.__logger = logging.getLogger(__name__)

    def api_call(
        self,
        *,
        method: str,
        path: str,
        token: Optional[str] = None,
        query_params: Optional[Dict[str, str]] = None,
        data: Optional[dict] = None,
        additional_headers: Optional[Dict[str, str]] = None,
    ):
        if additional_headers is None:
            additional_headers = {}

        url = self.__get_url(path)

        if self.__logger.level <= logging.DEBUG:

            def convert_params(values: dict) -> dict:
                if not values or not isinstance(values, dict):
                    return {}
                return {
                    k: ("(bytes)" if isinstance(v, bytes) else v)
                    for k, v in values.items()
                }

            headers = {
                k: "(redacted)" if k.lower() == "authorization" else v
                for k, v in additional_headers.items()
            }

            self.__logger.debug(
                f"Sending a request - url: {url}, "
                f"query_params: {convert_params(query_params)}, "
                f"data: {data}, "
                f"headers: {headers}"
            )

        headers = self.__build_urllib_request_headers(
            token=token or self.token, additional_headers=additional_headers
        )

        if query_params:
            q = urlencode(query_params)
            url = f"{url}&{q}" if "?" in url else f"{url}?{q}"

        (status, headers, body) = self.__perform_urllib_http_request(
            method, url, data, headers
        )

        return ServicingResponse(
            method=method,
            url=url,
            data=json.loads(body) if body else None,
            headers=headers,
            status=status,
        )

    def __perform_urllib_http_request(
        self, method: str, url: str, data: Optional[dict], headers: dict
    ):
        if data:
            body = self._dumps(data).encode("utf-8")
            headers["Content-Type"] = "application/json;charset=utf-8"
        else:
            body = None

        try:
            if url.lower().startswith("http"):
                req = Request(method=method, url=url, data=body, headers=headers)
                resp: HTTPResponse = urlopen(req, context=self.ssl)
                return resp.status, resp.headers, resp.read().decode("utf-8")
            raise ServicingRequestError(f"Invalid URL detected: {url}")
        except HTTPError as e:
            return e.code, e.headers, e.read().decode("utf-8")
        except Exception as err:
            self.__logger.error(f"Failed to send a request to Servicing API: {err}")
            raise err

    def __build_urllib_request_headers(self, token: str, additional_headers: dict):
        headers = {"User-Agent": self._get_user_agent()}

        headers.update(self.headers)
        headers.update({"Authorization": f"Bearer {token}"})

        if additional_headers:
            headers.update(additional_headers)

        return headers

    def __get_url(self, path: str):
        """Joins the base URL and a path to form an absolute URL."""
        return urljoin(self.base_url, path)

    @staticmethod
    def _get_user_agent():
        """Construct the user-agent header with the package info,
        Python version and OS version.
        Returns:
            The user agent string.
            e.g. 'Python/3.6.7 servicingclient/2.0.0 Darwin/17.7.0'
        """
        # __name__ returns all classes, we only want the client
        client = f"servicingclient/{__version__}"
        python_version = "Python/{v.major}.{v.minor}.{v.micro}".format(
            v=sys.version_info
        )
        system_info = f"{platform.system()}/{platform.release()}"
        return " ".join([python_version, client, system_info])

    @staticmethod
    def _dumps(value):
        return json.dumps(value, cls=JSONEncoder)
