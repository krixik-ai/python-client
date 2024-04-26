import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException


class MockedRequestException(RequestException):
    def __init__(self, message, status_code, text=None):
        super().__init__(message)
        self.response = requests.Response()
        self.response.status_code = status_code
        if text is not None:
            self.response._content = text.encode("utf-8")


class MockedHTTPError(HTTPError):
    def __init__(self, message, status_code, text=None):
        super().__init__(message)
        self.response = requests.Response()
        self.response.status_code = status_code
        if text is not None:
            self.response._content = text.encode("utf-8")


class MockedConnectionError(ConnectionError):
    def __init__(self, message, status_code, text=None):
        super().__init__(message)
        self.response = requests.Response()
        self.response.status_code = status_code
        if text is not None:
            self.response._content = text.encode("utf-8")


class MockedTimeoutError(Timeout):
    def __init__(self, message, status_code, text=None):
        super().__init__(message)
        self.response = requests.Response()
        self.response.status_code = status_code
        if text is not None:
            self.response._content = text.encode("utf-8")
