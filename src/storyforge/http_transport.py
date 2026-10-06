import json
from urllib.request import Request, urlopen


def json_post_transport(endpoint: str, payload: dict, headers: dict[str, str]) -> dict:
    request = Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))
