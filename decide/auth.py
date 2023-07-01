import logging
import os
from typing import Optional

import requests
from requests.adapters import HTTPAdapter, Retry

from decide.globals import MAX_RETRIES, LOGIN_URL
from decide.models.error import IllegalAssignmentException, DecideException

retries = Retry(total=MAX_RETRIES, backoff_factor=1, status_forcelist=[ 429, 500, 502, 503, 504 ])
adapter = HTTPAdapter(max_retries=retries)
logger = logging.getLogger(__name__)    


def _fetch_auth_code(url) -> Optional[str]:
    client_id = os.getenv("INDICINA_CLIENT_ID")
    client_secret = os.getenv("INDICINA_CLIENT_SECRET")

    print("Fetching authorization token...")
    try:
        with requests.Session() as session:
            session.mount(url, adapter)
            response = session.post(url=url, data={
                "client_id": client_id,
                "client_secret": client_secret
            })

            response.raise_for_status()
            response = response.json()

            return response["data"]["token"]
    except requests.exceptions.HTTPError as errh:
        logger.error("HTTP Error: %s", errh)
        raise DecideException("Unable to fetch auth code due to HTTP error.")
    except requests.exceptions.ConnectionError as errc:
        logger.error("Connection error: %s", errc)
        raise DecideException("Unable to connect to the Decide API.")
    except requests.exceptions.Timeout as errt:
        logger.error("Timeout Error: %s", errt)
        raise DecideException("Timeout occurred while fetching auth code.")
    except requests.exceptions.RequestException as err:
        logger.error("Request Exception: %s", err)
        raise DecideException("An error occurred while fetching auth code.")


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
