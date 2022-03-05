import asyncio
import logging
import traceback
from concurrent.futures import ThreadPoolExecutor

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, scoped_session

from errors import InvalidDataError, InternalError
from schema import metadata, Comment

logger = logging.getLogger(__name__)


class Worker:
    def __init__(self, engine: Engine):
        self._engine = engine
        metadata.create_all(engine)
        self._session = scoped_session(sessionmaker(engine))
        self._executor = ThreadPoolExecutor()

    def add_comment(self, data: dict) -> dict:
        assert "author" in data
        assert "text" in data
        comment = Comment(author=data['author'], text=data['text'])
        self._session.add(comment)
        self._session.commit()
        return dict(result="ok")

    async def do_stuff(self, data: dict) -> dict:
        loop = asyncio.get_event_loop()
        try:
            if self._engine.name != 'sqlite':
                return await loop.run_in_executor(self._executor, self.add_comment, data)
            else:  # создается новая база в каждом треде, все запускаем в основном потоке.
                self.add_comment(data)
        except AssertionError as e:
            logger.error(traceback.format_exc())
            raise InvalidDataError() from e
        except Exception as e:
            logger.error(traceback.format_exc())
            raise InternalError() from e
