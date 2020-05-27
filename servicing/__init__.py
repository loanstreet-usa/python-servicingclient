import logging
from logging import NullHandler

from .web.client import ServicingClient  # noqa

logging.getLogger(__name__).addHandler(NullHandler())
