import asyncio
import typing
import functools

from pyrogram.client import Client as _Client
from pyrogram import ContinuePropagation
from pyrogram.handlers.message_handler import MessageHandler
from pyrogram.filters import Filter
from pyrogram.types import Update


_MT = typing.Union[asyncio.Future, typing.Callable]


class MetaStore:
    async def set_item(self, key: int, value: _MT) -> None:
        """
        Stores key-value.
        """
        raise NotImplementedError

    async def pop_item(self, key: int) -> _MT:
        """
        Gives stored key-value.

        raise KeyError if not found.
        """
        raise NotImplementedError

    async def clear(self) -> typing.AsyncGenerator[_MT, None]:
        """
        Gives and clears all stored key-value.
        """
        raise NotImplementedError


class _RootStore(MetaStore, dict):
    def __init__(self, *args, **kwargs) -> None:
        self._event = asyncio.Event()
        self._event.set()
        super().__init__(*args, **kwargs)

    async def set_item(self, key: int, value: _MT) -> None:
        await self._event.wait()
        self[key] = value

    async def pop_item(self, key: int) -> _MT:
        await self._event.wait()
        return self.pop(key)

    async def clear(self) -> typing.AsyncGenerator[_MT, None]:
        try:
            self._event.clear()
            for k in tuple(self.keys()):
                yield self.pop(k)
        finally:
            self._event.set()


root = _RootStore()


def change_root_store(store: MetaStore) -> None:
    """
    changes root store.
    """
    global root
    root = store


async def listening_handler(_c, _u, store: typing.Optional[MetaStore] = None):
    """
    listen function for steps.

    If you aren't using plugins, use `.listen()` function.

    supported handlers:
        - `MessageHandler`
        - `CallbackQueryHandler`
        - `ChatJoinRequestHandler`
        - `ChatMemberUpdatedHandler`
        - `ChosenInlineResultHandler`
        - `EditedMessageHandler`
        - `InlineQueryHandler`

    Example::

        # plugin file
        @Client.on_message()
        async def listening(client, message):
            await pyrostep.listening_handler(client, message)
    """
    store = store or root

    fn = None

    try:
        fn = await root.pop_item(_u.from_user.id)
    except (KeyError, AttributeError):
        try:
            fn = await root.pop_item(_u.chat.id)
        except (KeyError, AttributeError):
            pass

    if fn is not None:
        if isinstance(fn, asyncio.Future):
            fn.set_result(_u)
            return

        await fn(_c, _u)
        return

    raise ContinuePropagation


def listen(
    app: _Client,
    store: typing.Optional[MetaStore] = None,
    handler: typing.Any = MessageHandler,
    filters: typing.Optional[Filter] = None,
    group: int = 0,
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

        if fn is not None:
            if isinstance(fn, asyncio.Future):
                fn.set_result(_u)
                return

            await fn(_c, _u)
            return

        raise ContinuePropagation

    app.add_handler(handler(_listen_wrapper, filters), group=group)


async def register_next_step(
    id: int,
    _next: typing.Any,
    store: typing.Optional[MetaStore] = None,
    *,
    args: tuple = (),
    kwargs: dict = {},
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
    if args or kwargs:
        _next = functools.partial(_next, *args, **kwargs)

    await (store or root).set_item(id, _next)


async def unregister_steps(id: int, store: typing.Optional[MetaStore] = None) -> None:
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


async def _wait_future(id: int, timeout: typing.Optional[float], store: MetaStore) -> Update:
    fn = asyncio.get_event_loop().create_future()

    await store.set_item(id, fn)

    try:
        return await asyncio.wait_for(fn, timeout)
    finally:
        await unregister_steps(id, store)


async def wait_for(id: int, timeout: typing.Optional[float] = None, store: typing.Optional[MetaStore] = None) -> Update:
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
                # operation was cancelled by `unregister_steps`
                return

            await answer.reply_text(f"Your Name Is: {answer.text}")
    """
    try:
        return await _wait_future(id, timeout, store or root)
    except asyncio.TimeoutError:
        raise TimeoutError


async def clear(store: typing.Optional[MetaStore] = None) -> None:
    """
    Clears all registered key-value's.

    Blocks listener until complete clearing.
    """
    async for i in (store or root).clear(): # type: ignore
        if isinstance(i, asyncio.Future):
            i.cancel()
