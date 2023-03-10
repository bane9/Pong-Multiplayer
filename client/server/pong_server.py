"""_summary_
"""

import requests
from global_config import GlobalConfig


class PongServer:
    SERVER_ADDRESS = f"http://{GlobalConfig.SERVER_HOST}:{GlobalConfig.SERVER_PORT}"
    TIMEOUT = 1000

    @classmethod
    def login(cls, username: str, password: str) -> tuple[bool, str]:
        data = {"username": username, "password": password}
        resp = requests.post(cls.SERVER_ADDRESS + "/login", json=data, timeout=cls.TIMEOUT)

        return resp.status_code == 200, resp.text

    @classmethod
    def register(cls, username: str, password: str) -> tuple[bool, str]:
        data = {"username": username, "password": password}
        resp = requests.post(cls.SERVER_ADDRESS + "/register", json=data, timeout=cls.TIMEOUT)

        return resp.status_code == 200, resp.text

    @classmethod
    def new_session(cls, host_username: str = "") -> tuple[bool, dict[str, str or int]]:
        data = {"host_username": host_username}
        resp = requests.get(cls.SERVER_ADDRESS + "/new_session", json=data, timeout=cls.TIMEOUT)

        return resp.status_code == 200, resp.json()

    @classmethod
    def get_session(cls, session: str) -> tuple[bool, str]:
        data = {"session": session}
        resp = requests.get(cls.SERVER_ADDRESS + "/get_session", json=data, timeout=cls.TIMEOUT)

        return resp.status_code == 200, resp.text
