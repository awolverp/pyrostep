"""
A Python library to handle steps in pyrogram framework.
"""
__author__ = "aWolver"
__version__ = "2.10.10"

__all__ = [
    "change_root_store", "listen", "register_next_step", "unregister_steps", "wait_for", "clear", "shortcuts",
]

from .steps import (
    MetaStore as MetaStore,
    change_root_store as change_root_store,
    listen as listen,
    register_next_step as register_next_step,
    unregister_steps as unregister_steps,
    wait_for as wait_for,
    clear as clear,
)

from . import (
    shortcuts as shortcuts,
    connection as connection,
)

from ._idle import safe_idle as safe_idle
from ._install import install as install
