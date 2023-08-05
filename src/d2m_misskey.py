import requests
from typing import Any

from d2m_misskey_dataclass import *
from d2m_exception import MisskeyApiError

class d2mMisskey:
    def __init__(self, host: str = "https://localhost", token: str = "") -> None:
        self.host = host[:-1] if host[-1] == '/' else host
        self.token = token

    def notes_create(self, data: CreatableNote) -> dict[str, Any]:
        if data.i is None:
            data.i = self.token
        return self._post(endpoint="notes/create", params=dataclasses.asdict(data))

    def _post(self, endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
        response = requests.post(self.host + "/api/" + endpoint, json={k: v for k, v in params.items() if v is not None})
        result = response.json()
        if type(result.get("error")) is dict:
            raise MisskeyApiError(url=response.url, status_code=response.status_code, result=result)
        elif type(result.get("error")) is str:
            response.raise_for_status()
        return result
