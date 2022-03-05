from aiohttp.web_exceptions import HTTPException


class InternalError(HTTPException):
    status_code = 500


class InvalidDataError(HTTPException):
    status_code = 400
