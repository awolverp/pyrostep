from pyrogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
)
from pyrogram.client import (
    Client
)
from pyrogram.enums import (
    ChatMemberStatus
)
from pyrogram.errors import (
    UserNotParticipant
)

import typing

def split_list(lst: list, rows: int) -> list:
    """
    split_list splites lst list.

    Parameters:
        lst (``list``):
            list.
        
        rows (``int``):
            count of rows.
    
    Example:
        >>> split_list([1, 2, 3, 4, 5, 6], 2) # [[1, 2], [3, 4], [5, 6]]
        >>> split_list([1, 2, 3], 2) # [[1, 2], [3]]
    """
    return [ lst[i:i+rows] for i in range(0, len(lst), rows) ]

def keyboard(lst: typing.List[typing.List[typing.List[str]]], **kwargs) -> ReplyKeyboardMarkup:
    """
    keyboard creates ReplyKeyboardMarkup from your list.

    Parameters:
        lst (``list[list[list]]``):
            your list.
        
        resize_keyboard (``bool``, *optional*):
            Requests clients to resize the keyboard vertically for optimal fit (e.g., make the keyboard smaller if
            there are just two rows of buttons). Defaults to false, in which case the custom keyboard is always of
            the same height as the app's standard keyboard.

        one_time_keyboard (``bool``, *optional*):
            Requests clients to hide the keyboard as soon as it's been used. The keyboard will still be available,
            but clients will automatically display the usual letter-keyboard in the chat – the user can press a
            special button in the input field to see the custom keyboard again. Defaults to false.

        selective (``bool``, *optional*):
            Use this parameter if you want to show the keyboard to specific users only. Targets:
            1) users that are @mentioned in the text of the Message object;
            2) if the bot's message is a reply (has reply_to_message_id), sender of the original message.
            Example: A user requests to change the bot's language, bot replies to the request with a keyboard to
            select the new language. Other users in the group don't see the keyboard.

        placeholder (``str``, *optional*):
            The placeholder to be shown in the input field when the keyboard is active; 1-64 characters.

    Example::
        buttons = [
            [
                ["Top Left"], ["Top Right"]
            ],
            [
                ["Bottom | Request Contact", True, "request_contact"]
            ]
        ]
        utils.keyboard(buttons)
    """
    return ReplyKeyboardMarkup([ [button(*kb) for kb in line] for line in lst ], **kwargs)

def inlinekeyboard(lst: typing.List[typing.List[typing.List[str]]]) -> InlineKeyboardMarkup:
    """
    inlinekeyboard creates InlineKeyboardMarkup from your list.

    Parameters:
        lst (``list[list[list]]``):
            your list.
    
    Example:
        buttons = [
            [
                ["Top Left", "data_1"], ["Top Right", "data_2"]
            ],
            [
                ["Bottom", "Your URL", "url"]
            ]
        ]
        utils.inlienkeyboard(buttons)
    """
    return InlineKeyboardMarkup([ [inline_button(*kb) for kb in line] for line in lst ])

def button(text: str, value = None, _type: str = "request_contact") -> KeyboardButton:
    """
    button returns KeyboardButton
    """
    return KeyboardButton(text) if value == None else KeyboardButton(text, **{_type:value})

def inline_button(text: str, value = None, _type: str = "callback_data") -> InlineKeyboardButton:
    """
    inline_button returns InlineKeyboardButton
    """
    return InlineKeyboardButton(text) if value == None else InlineKeyboardButton(text, **{_type:value})

async def validation_channels(
    app: Client, id: int, channels: typing.Iterable[typing.Union[int, str]],
    invite_func: typing.Callable[[Client, int, typing.Iterable[typing.Union[int, str]]], typing.Coroutine] = None
) -> bool:
    """
    validation_channels checks user already in channels or not.

    Parameters:
        app (`pyrogram.Client`):
            client.
        
        id (`int | str`):
            user id or username.
        
        channels (`list[int | str]`):
            list of channels id or username.

        invite_func (`(Client, int, list[int | str]) -> None`, `optional`):
            validation_channels calls it when user not member of channels. (before return False)
    
    Returns:
        returns True if user already in channels, returns False otherwise.
    
    Example::

        user_id = 56392019
        channels = [-102792837, -10823823, 'channel_username']

        is_joined = await validation_channels(app, user_id, channels)

        # ...

        async def invite(app, id, channels) -> None:
            print("User %d is not member of channels (%s)" % (id, str(channels)))
        
        is_joined = await validation_channels(app, user_id, channels, invite_func=invite)
    """
    for ch in channels:
        try:
            status = await app.get_chat_member(ch, id)
        except UserNotParticipant:
            if invite_func: await invite_func(app, id, channels)
            return False
        
        if status.status == ChatMemberStatus.LEFT:
            if invite_func: await invite_func(app, id, channels)
            return False
    
    return True
