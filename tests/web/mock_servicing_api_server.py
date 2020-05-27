import json
import logging
import re
import threading
from http import HTTPStatus
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Type
from unittest import TestCase
from urllib.parse import urlparse, parse_qs

from ..helpers import folder_path


class MockHandler(SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    default_request_version = "HTTP/1.1"
    logger = logging.getLogger(__name__)

    pattern_for_language = re.compile("python/(\\S+)", re.IGNORECASE)
    pattern_for_package_identifier = re.compile("servicingclient/(\\S+)")

    def is_valid_user_agent(self):
        user_agent = self.headers["User-Agent"]
        return self.pattern_for_language.search(user_agent) \
               and self.pattern_for_package_identifier.search(user_agent)

    def is_valid_token(self):
        return "Authorization" in self.headers \
               and str(self.headers["Authorization"]).startswith("Bearer")

    def set_common_headers(self):
        self.send_header("content-type", "application/json")
        self.send_header("connection", "close")
        self.end_headers()

    def _handle(self):
        try:
            if self.is_valid_token() and self.is_valid_user_agent():
                parsed_path = urlparse(self.path)

                len_header = self.headers.get('Content-Length') or 0
                content_len = int(len_header)
                post_body = self.rfile.read(content_len)

                if post_body:
                    json.loads(post_body.decode("utf-8"))

                header = self.headers["authorization"]
                pattern = str(header).split(" ", 1)[1].strip()

                with folder_path(__file__).parent.joinpath("data", f"servicing_response_{pattern}.json").open() as f:
                    body = json.load(f)
                    status = HTTPStatus.OK
            else:
                body = None
                status = HTTPStatus.UNAUTHORIZED

            self.send_response(status)
            self.set_common_headers()
            if body:
                self.wfile.write(json.dumps(body).encode("utf-8"))

        except Exception as e:
            self.logger.error(str(e), exc_info=True)
            raise

    def do_GET(self):
        self._handle()

    def do_POST(self):
        self._handle()


class MockServerThread(threading.Thread):

    def __init__(self, test: TestCase, handler: Type[SimpleHTTPRequestHandler] = MockHandler):
        threading.Thread.__init__(self)
        self.handler = handler
        self.test = test

    def run(self):
        self.server = HTTPServer(('localhost', 8888), self.handler)
        self.test.server_url = "http://localhost:8888"
        self.test.host, self.test.port = self.server.socket.getsockname()
        self.test.server_started.set()  # threading.Event()

        self.test = None
        try:
            self.server.serve_forever(0.05)
        finally:
            self.server.server_close()

    def stop(self):
        self.server.shutdown()
        self.join()


def setup_mock_servicing_api_server(test: TestCase):
    test.server_started = threading.Event()
    test.thread = MockServerThread(test)
    test.thread.start()
    test.server_started.wait()


def cleanup_mock_servicing_api_server(test: TestCase):
    test.thread.stop()
    test.thread = None
