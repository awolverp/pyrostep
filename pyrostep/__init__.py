"""
A Python library to handle steps in pyrogram framework.
"""
__author__ = "aWolver"
__version__ = "2.10.8"

__all__ = [
    "change_root_store", "listen", "register_next_step", "unregister_steps",
    "_wait_future", "wait_for", "clear", "safe_idle",
    "shortcuts",
]

from .steps import (
    MetaStore, change_root_store, listen, register_next_step, unregister_steps,
    _wait_future, wait_for, clear
)

from . import (
    shortcuts,
    connection,
)

from ._idle import (
    safe_idle
)

from ._install import (
    install
)
