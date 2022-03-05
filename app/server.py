import asyncio
import json
import logging
import traceback
from asyncio import Future

from aiohttp import web
from aiohttp.web_request import Request

from errors import InvalidDataError
from logic import Worker

logger = logging.getLogger(__name__)


class Server:
    def __init__(self, worker: Worker):
        self._worker = worker
        self._app = web.Application(logger=logger)
        self._app.add_routes([web.post('/comment', self.comment)])
        self._runner = web.AppRunner(self._app)
        self._stop_flag = Future()

    async def serve(self, interface: str, port: int) -> None:
        logger.info(f"starting site on {interface}:{port}")
        await self._runner.setup()
        site = web.TCPSite(self._runner, interface, port)
        await site.start()
        while not self._stop_flag.done():
            await asyncio.sleep(1)
        await self._runner.cleanup()
        logger.info("cleanup complete")

    def stop(self, *_):
        logger.info(f"stopping server")
        self._stop_flag.set_result(True)

    async def comment(self, request: Request):
        raw_data: bytes = await request.read()
        try:
            decoded_data = raw_data.decode('utf-8')
            data: dict = json.loads(decoded_data)
        except ValueError as e:
            logger.error(traceback.format_exc())
            raise InvalidDataError() from e

        response: dict = await self._worker.do_stuff(data)
        response_str: str = json.dumps(response)
        return web.Response(text=response_str)
