import datetime
import json
import logging
import time
from contextlib import suppress
from typing import Optional

import toml
from dotenv import load_dotenv
from fastapi import Request

load_dotenv()


def load_config(fname: str):
    """
    Initialize Python logging config from a TOML file.
    """

    with open(fname, "r") as file:
        config = toml.load(file)

    logging.config.dictConfig(config)


#: A tuple of types ``json.JSONEncoder`` can natively encode.
JSONABLE_TYPES = (dict, list, tuple, str, int, float, bool, type(None))


class UniversalJSONEncoder(json.JSONEncoder):
    """
    A JSON encoder that tries to convert everything.
    """

    def default(self, obj):
        if isinstance(obj, JSONABLE_TYPES):
            pass

        # Try str() and repr(). If both fail (they shouldn't), return a string indicating that:

        with suppress(Exception):
            return str(obj)

        with suppress(Exception):
            return repr(obj)

        return "<incomprehensible>"


class JSONFormatter(logging.Formatter):
    """
    Formatter that writes messages as JSON lines.
    """

    def format(self, record: logging.LogRecord):
        """
        Format the specified record as a JSON.
        """

        super().format(record)

        json_msg = {
            "message": record.msg,
            "app_time_utc": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            # "env": Config.ENVIRONMENT,
            # "client_id": config.AUTH0_CLIENTID_FC
            # "user_id": ...,
            "name": record.name,
            "levelname": record.levelname,
            "pathname": record.pathname,
            "exc_info": record.exc_info,
            "lineno": record.lineno,
        }

        return json.dumps(json_msg, cls=UniversalJSONEncoder)


class JSONFileHandler(logging.handlers.RotatingFileHandler):
    """
    Handler for logging to a set of JSON Lines [1] files, which switches from one file
    to the next when the current file reaches a certain size. It also configures some
    sane defaults.

    [1]: https://jsonlines.org/
    """

    def __init__(  # noqa: WPS211
        self,
        filename: str,
        mode: str = "a",
        maxBytes: int = 1024 * 1024,  # noqa: N803
        backupCount: int = 3,
        encoding: Optional[str] = None,
        delay: int = False,
        **kwargs,
    ):
        super().__init__(
            filename,
            mode=mode,
            maxBytes=maxBytes,
            backupCount=backupCount,
            encoding=encoding,
            delay=delay,
            **kwargs,
        )
        self.formatter = JSONFormatter()


server_access_logger = logging.getLogger(f"{__name__}.server_access_logger")

async def server_access_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    time_elapsed = (time.time() - start_time) * 1000

    server_access_logger.info(
        " ".join([
            f"[@{start_time:.0f}]",
            request.url.path,
            f"time_elapsed={time_elapsed:.2f}ms",
            f"status_code={response.status_code}",
        ]),
    )

    return response
