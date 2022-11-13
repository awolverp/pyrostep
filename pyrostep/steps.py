import asyncio
import typing

from pyrogram.client import Client as _Client
from pyrogram import ContinuePropagation
from pyrogram.handlers import MessageHandler
from pyrogram.filters import Filter
from pyrogram.types import Update

class MetaStore:
    def set_item(self, key: int, value: typing.Union[asyncio.Future, typing.Callable]) -> None:
        """
        Stores key-value.
        """
        pass

    def pop_item(self, key: int) -> typing.Union[asyncio.Future, typing.Callable]:
        """
        Gives stored key-value.

        raise KeyError if not found.
        """
        pass

    def clear(self) -> typing.Iterable[typing.Union[asyncio.Future, typing.Callable]]:
        """
        Gives and clears all stored key-value.
        """
        pass

loop = asyncio.get_event_loop()

class _RootStore(MetaStore, dict):
    def __init__(self, *args, **kwargs) -> None:
        self._event = asyncio.Event()
        self._event.set()
        super().__init__(*args, **kwargs)

    async def set_item(self, key: int, value: typing.Union[asyncio.Future, typing.Callable]) -> None:
        await self._event.wait()
        self[key] = value
    
    async def pop_item(self, key: int) -> typing.Union[asyncio.Future, typing.Callable]:
        await self._event.wait()
        return self.pop(key)
    
    async def clear(self) -> typing.Iterable[typing.Union[asyncio.Future, typing.Callable]]:
        try:
            await self._event.clear()
            return tuple(self.popitem() for i in range(len(self)))
        finally:
            await self._event.set()

root = _RootStore() # type: MetaStore

def change_root_store(store: MetaStore) -> None:
    """
    changes root store.
    """
    global root
    root = store

def listen(
    app: _Client, store: MetaStore = None, exclude: typing.List[str] = None,
    handler: typing.Any = MessageHandler, filters: Filter = None, group: int = 0
) -> None:
    """
    listen client for steps.

    supported handlers:
        - `MessageHandler`
        - `CallbackQueryHandler`
        - `ChatJoinRequestHandler`
        - `ChatMemberUpdatedHandler`
        - `ChosenInlineResultHandler`
        - `EditedMessageHandler`
        - `InlineQueryHandler`
    
    Example::

        app = Client(...)
        pyrostep.listen(app)
    """
    store = store or root

    async def _listen_wrapper(_c, _u):
        fn = None

        try:
            fn = await store.pop_item(_u.from_user.id)
        except (KeyError, AttributeError):
            
            try:
                fn = await store.pop_item(_u.chat.id)
            except (KeyError, AttributeError):
                pass

        if not (fn is None):
            if isinstance(fn, asyncio.Future):
                fn.set_result(_u)
                return
            
            await fn(_c, _u)
            return
        
        raise ContinuePropagation
    
    app.add_handler(handler(_listen_wrapper, filters), group=group)

async def register_next_step(
    id: int, _next: typing.Any, store: MetaStore = None
) -> None:
    """
    register next step for user/chat.

    Example::

        async def step1(client, msg):
            # code ...
            register_next_step(msg.from_user.id, step2)
        
        async def step2(client, msg):
            # code ...
    """
    await (store or root).set_item(id, _next)

async def unregister_steps(id: int, store: MetaStore = None) -> None:
    """
    unregister steps for `id`.

    if step is `asyncio.Future`, cancels that.
    """
    try:
        u = await (store or root).pop_item(id)
    except KeyError:
        return
    else:
        if isinstance(u, asyncio.Future):
            u.cancel("cancelled")

async def _wait_future(id: int, timeout: float, store: MetaStore) -> Update:
    fn = loop.create_future()

    await store.set_item(id, fn)

    try:
        return await asyncio.wait_for(fn, timeout)
    finally:
        await unregister_steps(id, store)

async def wait_for(
    id: int, timeout: float = None, store: MetaStore = None
) -> Update:
    """
    wait for update which comming from id.

    raise TimeoutError if timed out.

    Example::

        async def hello(_, message: Message):
            await message.reply_text("What's your name?")
            try:
                answer: Message = await pyrostep.wait_for(message.from_user, timeout=20)
            except TimeoutError:
                return
            
            except asyncio.CancelledError:
                # operation cancelled by `unregister_steps`
                return
            
            await answer.reply_text(f"Your Name Is: {answer.text}")
    """
    try:
        return await _wait_future(id, timeout, store or root)
    except asyncio.CancelledError as e:
        if str(e) == "cancelled":
            raise e from None

async def clear(store: MetaStore = None) -> None:
    """
    Clears all registered key-value's.

    Blocks listener until complete clearing.
    """
    async for i in (store or root).clear():
        if isinstance(i, asyncio.Future):
            i.cancel("cancelled")
