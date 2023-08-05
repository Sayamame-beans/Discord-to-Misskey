from typing import Any

class d2mError(Exception):
    "Discord-to-Misskey固有の処理で発生するエラー"


class MisskeyApiError(d2mError):
    "Misskey API上のエラー"
    def __init__(self, url: str, status_code: int, result: dict[str, Any],) -> None:
        detail = result["error"]
        self.message = detail.get("message")
        self.code = detail.get("code")
        self.id = detail.get("id")
        self.kind = detail.get("kind")
        self.httpStatusCode = status_code
        self.info = detail.get("info")

        super().__init__(f"{status_code} : {detail} on {url}")
