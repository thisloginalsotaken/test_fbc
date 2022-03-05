import argparse
import asyncio
import logging
import signal
import sys

from sqlalchemy import create_engine

from logic import Worker
from server import Server

logger = logging.getLogger('main')


async def main(db_connection_string: str, interface: str, port: int) -> int:
    engine = create_engine(db_connection_string)
    logger.info(f"using {engine.name} engine")
    worker = Worker(engine=engine)
    server = Server(worker=worker)
    signal.signal(signal.SIGINT, server.stop)
    signal.signal(signal.SIGTERM, server.stop)
    await server.serve(interface=interface, port=port)
    return 0


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logging.getLogger('sqlalchemy').setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('--connection-string', default='sqlite://')
    parser.add_argument('--interface', default='0.0.0.0', type=str)
    parser.add_argument('--port', default=8080, type=int)
    args = parser.parse_args()

    return_status = asyncio.run(
        main(db_connection_string=args.connection_string, port=args.port, interface=args.interface))
    sys.exit(return_status)
