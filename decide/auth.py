import logging
import os
from typing import Optional

import requests
from requests.adapters import HTTPAdapter

from decide.globals import MAX_RETRIES, LOGIN_URL
from decide.models.error import IllegalAssignmentException, DecideException

adapter = HTTPAdapter(max_retries=MAX_RETRIES)
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

            if response.status_code != 200:
                logger.error("Unable to fetch auth code.")
                return None
            response = response.json()
            if response["status"] != "success":
                logger.error("Unable to fetch auth code.")
                return None
            return response["data"]["token"]
    except ConnectionError as error:
        logger.error("Unable to connect to Decide API. %s", error)
        DecideException("Unable to reach Decide server. Check connection.")
        return None


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
