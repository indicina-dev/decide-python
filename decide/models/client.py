import os
import urllib.parse
from typing import Union, Any

import requests
from requests import Response

from ..globals import BASE_URL
from decide.auth import Auth
from .error import DecideException, IllegalAssignmentException


class DecideClient:
	def __init__(self, path: str, content_type: str) -> None:
		self.path = path
		self.content_type = content_type

		self.auth = Auth()

	def _req(self, method: str, **kwargs) -> Response:
		url = BASE_URL
		full_path = urllib.parse.urljoin(url, self.path)
		response = requests.request(method, full_path, headers=self.headers, **kwargs)
		if response.status_code == 401:
			self.auth.refresh()  # refresh token
			return requests.request(method, full_path, headers=self.headers, **kwargs)
		if response.status_code != 200:
			raise DecideException(response_code=response.status_code, message=response.text)
		return response

	@property
	def headers(self):
		return {
			"Authorization": f"Bearer {self.auth.code}"
		}

	@headers.setter
	def headers(self, headers):
		raise IllegalAssignmentException("You cannot assign a value to the headers.")

	def get(self, **kwargs) -> Union[list, dict, Response]:
		response = self._req(method="get", **kwargs)
		return response.json()

	def post(self, body: Any) -> Union[list, dict, Response]:
		if self.content_type == "application/json":
			response = self._req(method="post", json=body)
		elif self.content_type == "multipart/form-data":
			if "pdf" in self.path:
				file_name = body.pop("pdf")		# PDF
				response = self._req(method="post", data=body, files={"pdf": open(file_name, "rb")})
			elif "bsp/file" in self.path:
				file_name = body.pop("file_statement")		# CSV
				response = self._req(method="post", data=body, files={"file_statement": open(file_name, "rb")})
			else:
				response = None
		else:
			response = None
		return response.json()

	def put(self, **kwargs) -> Union[list, dict, Response]:
		response = self._req(method="put", **kwargs)
		return response.json()
