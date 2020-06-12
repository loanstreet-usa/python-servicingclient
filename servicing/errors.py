class ServicingClientError(Exception):
    pass


class ServicingApiError(ServicingClientError):
    """Error raised when API does not send the expected response."""

    def __init__(self, message, response):
        msg = f"{message}\nThe server responded with: [{response.status}] {response}"
        self.response = response
        super(ServicingClientError, self).__init__(msg)


class ServicingRequestError(ServicingClientError):
    """Error raised when there's a problem with the request that's being submitted.
    """

    pass


class ServicingObjectFormationError(ServicingClientError):
    """Error raised when a constructed object is not valid/malformed"""

    pass


class ServicingInvalidPathParamError(ServicingClientError):
    pass
