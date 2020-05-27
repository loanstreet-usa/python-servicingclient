import logging
from typing import Optional
from ..errors import ServicingApiError


class ServicingResponse(object):
    def __init__(
        self, *, method: str, url: str, data: Optional[dict], headers: dict, status: int
    ):
        self.method = method
        self.url = url
        self.data = data
        self.headers = headers
        self.status = status
        self.__logger = logging.getLogger(__name__)

    def __str__(self):
        """Return the Response data if object is converted to a string."""
        return f"{self.data}"

    def __getitem__(self, key):
        """Retrieves any key from the data store."""
        return self.data.get(key, None)

    def get(self, key, default=None):
        """Retrieves any key from the response data."""
        return self.data.get(key, default)

    def validate(self):
        """Check if the response from Servicing API was successful."""
        if self.__logger.level <= logging.DEBUG:
            self.__logger.debug(
                "Received the following response - "
                f"status: {self.status}, "
                f"headers: {dict(self.headers)}, "
                f"body: {self.data}"
            )

        if 200 <= self.status < 300:
            return self

        msg = "The request to the Servicing API failed."
        raise ServicingApiError(message=msg, response=self)
