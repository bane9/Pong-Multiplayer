"""_summary_
"""

from aiohttp import web


class GlobalConfig:
    web_server: web.Application

    SQL_HOST = "127.0.0.1"
    SQL_USERNAME = "root"
    SQL_PASSWORD = "root"
    SQL_PORT = 3306

    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 8080
