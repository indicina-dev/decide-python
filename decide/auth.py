import logging
import os
from typing import Optional

import requests
from requests.adapters import HTTPAdapter, Retry

from decide.globals import MAX_RETRIES, LOGIN_URL
from decide.models.error import IllegalAssignmentException, DecideException

retries = Retry(
    total=MAX_RETRIES, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retries)
logger = logging.getLogger(__name__)


def _fetch_auth_code(url) -> Optional[str]:
    client_id = os.getenv("INDICINA_CLIENT_ID")
    client_secret = os.getenv("INDICINA_CLIENT_SECRET")

    if not client_id or not client_secret:
        logger.error(
            "Both INDICINA_CLIENT_ID and INDICINA_CLIENT_SECRET must be set as environment variables."
        )
        raise DecideException(
            message="Both INDICINA_CLIENT_ID and INDICINA_CLIENT_SECRET must be set as environment variables.",
            status_code=400,
        )

    payload = {"client_id": client_id, "client_secret": client_secret}

    logger.info("Fetching authorization token...")
    try:
        with requests.Session() as session:
            session.mount(url, adapter)
            response = session.post(url=url, data=payload)

            response.raise_for_status()
            response_json = response.json()

            try:
                return response_json["data"]["token"]
            except KeyError:
                raise DecideException(
                    "Token not found in the response.",
                    response.status_code,
                    url,
                    payload,
                    response.headers,
                ) from None
    except requests.exceptions.HTTPError as errh:
        logger.error("HTTP Error: %s", errh)
        error_message = f"HTTP Error: {errh}"
        status_code = errh.response.status_code
        endpoint = url
        response_headers = response.headers
        raise DecideException(
            error_message, status_code, endpoint, payload, response_headers
        ) from errh
    except requests.exceptions.ConnectionError as errc:
        logger.error("Connection Error: %s", errc)
        raise DecideException(
            f"Connection Error: {errc}", request_payload=payload
        ) from errc
    except requests.exceptions.Timeout as errt:
        logger.error("Timeout Error: %s", errt)
        raise DecideException(
            f"Timeout Error: {errt}", request_payload=payload
        ) from errt
    except requests.exceptions.RequestException as err:
        logger.error("Request Exception: %s", err)
        raise DecideException(
            f"Request Exception: {err}", request_payload=payload
        ) from err


class Auth:
    """
    Singleton class for authorization.
    Do not use this class directly.
    """

    __instance = None
    _code = None

    def __new__(cls) -> "Auth":
        if not cls.__instance:
            cls.__instance = super(Auth, cls).__new__(cls)
        return cls.__instance

    def refresh(self):
        """Used to refresh token"""
        self._code = _fetch_auth_code(LOGIN_URL)

    @property
    def code(self) -> str:
        """code property"""
        if not self._code:
            self._code = _fetch_auth_code(LOGIN_URL)
        return self._code

    @code.setter
    def code(self, code):
        raise IllegalAssignmentException("You cannot set this value.")
