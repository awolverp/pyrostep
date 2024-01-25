import pyrogram.connection.connection
import pyrogram.session.session
import pyrogram.session.auth

import logging
import typing

log = logging.getLogger(__name__)


def connection_max_retries(max_retries: typing.Optional[int] = None) -> typing.Optional[int]:
    """
    Change connection max retries. (default 3)

    retries message:
        Unable to connect due to network issues: ...

    Return:
        returns MAX_RETRIES if max_retries is None
    """
    _attr = (
        "MAX_RETRIES"
        if hasattr(pyrogram.connection.connection.Connection, "MAX_RETRIES")
        else "MAX_CONNECTION_ATTEMPTS"
    )
    if not isinstance(max_retries, int):
        return getattr(pyrogram.connection.connection.Connection, _attr)

    setattr(pyrogram.connection.connection.Connection, _attr, max_retries)


def invoke_max_retries(max_retries: typing.Optional[int] = None) -> typing.Optional[int]:
    """
    Change invoke max retries. (default 5)

    retries message:
        [...] Waiting for ... seconds before continuing (required by "...")

    Return:
        returns MAX_RETRIES if max_retries is None
    """
    if not isinstance(max_retries, int):
        return pyrogram.session.session.Session.MAX_RETRIES

    pyrogram.session.session.Session.MAX_RETRIES = max_retries  # type: ignore


def session_start_timeout(timeout: typing.Optional[int] = None) -> typing.Optional[int]:
    """
    Change start timeout. (default 1)

    Return:
        returns START_TIMEOUT if timeout is None.
    """
    if not isinstance(timeout, int):
        return pyrogram.session.session.Session.START_TIMEOUT

    pyrogram.session.session.Session.START_TIMEOUT = timeout  # type: ignore


def session_max_retries(max_retries: typing.Optional[int]) -> typing.Optional[int]:
    """
    Change session max retries.

    retries message:
        Connection failed! Trying again...
    """
    if not isinstance(max_retries, int):
        return pyrogram.session.auth.Auth.MAX_RETRIES

    pyrogram.session.auth.Auth.MAX_RETRIES = max_retries - 1  # type: ignore
