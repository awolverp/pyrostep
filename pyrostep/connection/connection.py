from pyrogram.connection import Connection
from pyrogram.session import Session, auth

import logging

from pyrogram.connection import Connection
import typing

log = logging.getLogger(__name__)

def connection_max_retries(max_retries:int=None) -> typing.Optional[int]:
    """
    Change connection max retries. (default 3)

    retries message:
        Unable to connect due to network issues: ...

    Return:
        returns MAX_RETRIES if max_retries is None
    """
    if not isinstance(max_retries, int):
        return Connection.MAX_RETRIES

    Connection.MAX_RETRIES = max_retries

def invoke_max_retries(max_retries:int=None) -> typing.Optional[int]:
    """
    Change invoke max retries. (default 5)

    retries message:
        [...] Waiting for ... seconds before continuing (required by "...")
    
    Return:
        returns MAX_RETRIES if max_retries is None
    """
    if not isinstance(max_retries, int):
        return Session.MAX_RETRIES

    Session.MAX_RETRIES = max_retries

def session_start_timeout(timeout: int = None) -> typing.Optional[int]:
    """
    Change start timeout. (default 1)

    Return:
        returns START_TIMEOUT if timeout is None. 
    """
    if not isinstance(timeout, int):
        return Session.START_TIMEOUT

    Session.START_TIMEOUT = timeout

def session_max_retries(max_retries: int) -> None:
    """
    Change session max retries.

    retries message:
        Connection failed! Trying again...
    """
    auth.Auth.MAX_RETRIES = max_retries-1
