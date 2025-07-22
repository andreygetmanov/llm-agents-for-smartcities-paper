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
    Represents an API endpoint capable of validating parameters, formatting URLs, and executing HTTP requests.

    Class Methods:
    - __init__
    - _check_params
    - _parse_url_params
    - __call__
    - _execute_request

    Attributes:
    - url
    - param_names

    The class initializes with a URL (potentially with placeholders) and an optional collection of parameter names. Methods enable validation of these parameters, parsing and formatting the URL with parameters, executing HTTP requests, and returning JSON responses.
    """

    def __init__(self, url: str, param_names: Collection[str] = None):
        """
        Sets up the instance by storing the given URL, processing any provided parameter names, and preparing an internal generator to extract parameter fields from the URL pattern.

        Args:
            url: The URL string to be used, which may contain placeholders.
            param_names: An optional collection of parameter names to associate with the URL placeholders.

        Returns:
            None. Initializes instance attributes related to the URL and its parameters.
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
        Checks that the given parameters match the expected names by identifying any missing or unexpected entries, and raises an informative error if discrepancies are found.

        Checks if the given parameters dictionary contains all required keys and does not contain any unexpected keys. Raises a ValueError if required parameters are missing or if extra parameters are provided.

        Args:
            params: A dictionary containing parameters to validate against the expected parameter names.

        Returns:
            None. Raises a ValueError if the parameters are invalid.
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
        Extracts and inserts relevant values from the input parameters into the URL template, returning the formatted URL along with any remaining parameters.

        This method extracts parameters required for URL formatting from the provided params
        dictionary, formats the URL accordingly, and returns the formatted URL along with
        the remaining parameters.

        Args:
            params: Dictionary of parameters that may include values for URL formatting.
                Required URL parameters will be extracted and removed from this dictionary.

        Returns:
            tuple: A tuple containing the formatted URL (str) and the remaining parameters
                (dict) after extracting URL parameters.
        """

        url_params = {fname: params.pop(fname) for fname in self.url_params}
        url = self.url
        if url_params:
            url = self.url.format(**url_params)
        return url, params

    def __call__(self, **params) -> Any:
        """
        Invokes the endpoint with specified parameters, handling parameter validation, request preparation, execution, error logging, and returning the parsed JSON response.

        Args:
            **params: Arbitrary keyword arguments representing parameters to include in the request.

        Returns:
            Any: The parsed JSON response from the executed request.

        Raises:
            RequestException: If the HTTP response status code is not 200.
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
    Handles HTTP GET requests to specified API endpoints and manages request parameters and responses.

    Class Methods:
    - _execute_request:
    """

    def _execute_request(self, url: str, params: Dict[str, Any]) -> requests.Request:
        return requests.get(url, params=params, headers={"accept": "application/json"})


class PostEndpoint(Endpoint):
    """
    Handles HTTP POST requests to a specified endpoint.

    Attributes:
        url: The endpoint URL to send POST requests to.
        headers: Optional dictionary of HTTP headers to include in the request.
        timeout: Timeout duration for the request.

    Methods:
    - _execute_request
    - set_headers
    - set_timeout
    - post

    The methods allow configuring headers and timeout, and sending POST requests with specified parameters. Attributes store configuration for each request.
    """

    def _execute_request(self, url: str, params: Dict[str, Any]) -> requests.Request:
        """
        Submits data to the designated URL using a POST request and returns the server's response in JSON format.

        Args:
            url: The URL to which the request will be sent.
            params: The data to include in the body of the POST request.

        Returns:
            requests.Request: The response object from the POST request.
        """

        return requests.post(url, data=params, headers={"accept": "application/json"})
