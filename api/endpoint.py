import abc
import json
import logging
from string import Formatter
from typing import Any, Collection, Dict

import requests
from requests import RequestException


logger = logging.getLogger(__name__)


class Endpoint(abc.ABC):
    """
    Represents an HTTP endpoint with parameterized URLs, supporting validation and dynamic invocation of web requests.

    Methods:
    - __init__
    - _check_params
    - _parse_url_params
    - __call__
    - _execute_request

    Attributes:
    - url
    - param_names

    The methods handle initialization, parameter validation, URL parsing, executing HTTP requests, and invoking the endpoint as a function. The attributes store the endpoint's URL template and the expected parameter names.
    """

    def __init__(self, url: str, param_names: Collection[str] = None):
        """
        Constructs an instance by setting the URL, handling optional parameter names, and preparing an iterable to extract named placeholders from the URL pattern.

        Args:
            url: The URL template, which may contain placeholders for parameters.
            param_names: A collection of parameter names to be used with the URL, or None to use default behavior.

        Returns:
            None. This method initializes instance attributes related to the URL and its parameters.
        """

        if param_names is not None:
            param_names = tuple(param_names)
        self.url = url
        self.param_names = param_names
        self.url_params = (
            fname for _, fname, _, _ in Formatter().parse(self.url) if fname
        )

    def _check_params(self, params: Dict[str, Any]) -> None:
        """
        Checks whether the given parameters align with the defined set for this endpoint, raising an error if there are missing or unexpected entries.

        Checks for any missing or unexpected parameters based on the expected parameter names. If discrepancies are found, raises a ValueError detailing the issues.

        Args:
            params: A dictionary containing the parameters to be checked.

        Returns:
            None. Raises a ValueError if the parameters do not match the expected names.
        """

        if self.param_names is None:
            return

        missing_params = set(self.param_names).difference(set(params))
        extra_params = set(params).difference(set(self.param_names))

        error_msg = f"{self.__class__.__name__} {self.url}."
        is_error = False

        if missing_params:
            error_msg += f'\nMissing params: ({", ".join(missing_params)}).'
            is_error = True

        if extra_params:
            error_msg += f'\nUnexpected params: ({", ".join(extra_params)}).'
            is_error = True

        if is_error:
            raise ValueError(error_msg)

    def _parse_url_params(self, params):
        """
        Extracts parameters required by the endpoint from the input dictionary, formats the URL accordingly, and returns the updated URL along with remaining parameters.

        Extracts relevant URL parameters from the input dictionary and uses them to format the URL. Returns the updated URL and the remaining parameters.

        Args:
            params: Dictionary of input parameters, potentially containing URL formatting values.

        Returns:
            tuple: A tuple containing the formatted URL and a dictionary of the remaining parameters.
        """

        url_params = {fname: params.pop(fname) for fname in self.url_params}
        url = self.url
        if url_params:
            url = self.url.format(**url_params)
        return url, params

    def __call__(self, **params) -> Any:
        """
        Validates input parameters, constructs and formats the request payload, sends the request to the specified endpoint, handles error responses, and returns the parsed JSON result.

        Args:
            params: Arbitrary keyword arguments representing the parameters to include in the request.

        Returns:
            Any: The JSON-decoded response from the HTTP request.
        """

        self._check_params(params)
        url, params = self._parse_url_params(params)
        params = json.dumps(
            params, ensure_ascii=False
        )  # This is needed to transform None into null in the payload
        result = self._execute_request(url, params)
        if result.status_code != 200:
            logger.error(f"url: {url}")
            logger.error(f"params: {params}")
            raise RequestException(result.status_code)
        return result.json()

    @abc.abstractmethod
    def _execute_request(url: str, params: Dict[str, Any]) -> requests.Request:
        raise NotImplementedError()


class GetEndpoint(Endpoint):
    """
    Handles HTTP GET requests to a specified endpoint URL.

    Attributes:
        url: The endpoint URL for the GET request.
        params: Query parameters to be included in the request.

    Methods:
        _execute_request
        execute

    The methods send GET requests using provided parameters and retrieve responses from the specified URL. The attributes store the endpoint and query parameters.
    """

    def _execute_request(self, url: str, params: Dict[str, Any]) -> requests.Request:
        return requests.get(url, params=params, headers={"accept": "application/json"})


class PostEndpoint(Endpoint):
    """
    Handles HTTP POST requests to specified API endpoints.

    Class Methods:
    - _execute_request
    - send

    Attributes:
    - base_url
    - headers

    Methods Summary:
    - _execute_request: Sends a POST request to a provided URL with parameters and returns the server's response.
    - send: Constructs the full endpoint URL, prepares request parameters and headers, and dispatches the POST request.

    Attributes Summary:
    - base_url: The root URL used to compose endpoint addresses for HTTP requests.
    - headers: A dictionary of HTTP headers to include in each POST request.
    """

    def _execute_request(self, url: str, params: Dict[str, Any]) -> requests.Request:
        """
        Submits data to a specified URL using a POST request and returns the response object.

        Args:
            url: The endpoint URL to which the request is sent.
            params: The dictionary of parameters to include in the POST request body.

        Returns:
            requests.Request: The response returned from the POST request.
        """

        return requests.post(url, data=params, headers={"accept": "application/json"})
