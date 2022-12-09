import logging

from .client import DecideClient
from .base import BaseModel

logger = logging.getLogger(__name__)


class DecideTaggedStatement(BaseModel):  # pylint: disable=too-few-public-methods
    """
    This class handles Decide Tagged Statements
    ...

    Methods
    -------
    get()
        Gets a tagged statement from Decide mapped to a request_id
    """

    def __init__(self, request_id: str):
        """
        Parameters
        ----------
        request_id : str
            A string of the request_id of the analysis
        """
        self.request_id = request_id
        self.status = ""
        self.client = DecideClient(
            path=f"analysis/{request_id}/tagged_transactions",
            content_type="application/json",
        )
        self.data = None

    def get(self):
        """This method gets tagged statements"""
        json_response = self.client.get()
        self.status = json_response["status"]
        self.data = json_response["data"]
        super().__init__(data=json_response["data"])

        return self.status

    def __repr__(self):
        return f"DecideTaggedStatement(request_id={self.request_id})"
