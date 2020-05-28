import unittest
from uuid import uuid4

from servicing.web.base_client import BaseClient


class BaseClientTests(unittest.TestCase):
    def test_encodes_uuid(self):
        try:
            BaseClient()._dumps(uuid4())
        except TypeError as e:
            self.fail(str(e))
