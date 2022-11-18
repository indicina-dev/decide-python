import json
import re

name_pattern = re.compile(r"(.)([A-Z][a-z]+)")
snake_pattern = re.compile(r"([a-z0-9])([A-Z])")


def convert_to_camel(name: str) -> str:
    return ''.join(word.title() for word in name.split('_'))


class BaseModel(object):
    def __init__(self, data: dict, **kwargs) -> None:
        self.id = None
        self._data = {**data, **kwargs}
        self._json = self._jsond(data)

        for key, value in self._data.items():
            if key == "status":
                continue
            if isinstance(value, dict):
                setattr(self, key, self.build_dict_values(key, value))
            else:
                setattr(self, key, value)

    def _jsond(self, json_data: dict) -> str:
        return json.dumps(json_data)

    def _jsonl(self, data: str) -> dict:
        return json.loads(data)

    def build_dict_values(self, key, value):
        raise NotImplementedError
