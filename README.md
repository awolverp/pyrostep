# pyrostep
[![Downloads](https://static.pepy.tech/personalized-badge/pyrostep?period=total&units=abbreviation&left_color=red&right_color=grey&left_text=Downloads)](https://pepy.tech/project/pyrostep)

You can implement conversation in your project based on pyrogram very easy with **pyrostep**.

**Features**:
- Full type hint
- Support step handling
- Support asking
- Change core settings of pyrogram

**Installing**
```bash
pip3 install -U pyrostep
```

**Content**
- [tutorial](#tutorial)
    - [step handling](#step-handling)
    - [wait for method](#wait-for-method)
    - [plugins](#plugins)
- [shortcuts](#shortcuts)
- [connection package](#connection-package)

## Tutorial
Use `pyrostep.listen()` to start listening on your client:
```python
from pyrogram import Client
import pyrostep

# ...

client = Client("myaccount")
pyrostep.listen(client)
```

> [!NOTE]\
> Always use `pyrostep.listen()` before adding your handlers.

After that, we have two ways to make conversation: [wait_for method](#wait-for-method) or [step handling](#step-handling)

-----

### Wait for method
⏰ In this way we can use `pyrostep.wait_for` function, that waits for an update (e.g message) from your target.

```python
client = Client("myaccount")
pyrostep.listen(client)

# ...

@client.on_message()
async def get_name(_, message):
    await message.reply("Send your name?")
    
    answer = await pyrostep.wait_for(message.from_user.id)
    await message.reply(f"Your name is {answer.text}")
```

> [!TIP]\
> You can specify how long it will wait with `timeout` parameter. see this example:

```python
client = Client("myaccount")
pyrostep.listen(client)

# ...

@client.on_message()
async def get_name(_, message):
    await message.reply("Send your name?")

    try:
        answer = await pyrostep.wait_for(message.from_user.id, timeout=10)
    except TimeoutError:
        await message.reply("Timed out")
    else:
        await message.reply(f"Your name is {answer.text}")
```

🔗 **Related functions:**
- `clear()`: remove all registered steps (and cancels all wait_for's).

------

### Step handling
🎯 In this way we will use this functions:
- `pyrostep.register_next_step()`

We will specify a function that should process the next update from the target with `pyrostep.register_next_step()`.

> [!IMPORTANT]\
> In this way we cannot specify a timeout.

```python
client = Client("myaccount")
pyrostep.listen(client)

# ...

@client.on_message()
async def get_name(_, message):
    await message.reply("Send your name?")
    await pyrostep.register_next_step(
        message.from_user.id, get_age
    )

async def get_age(_, message):
    await message.reply("OK, Send your age?")
    await pyrostep.register_next_step(
        message.from_user.id,
        say_info,
        kwargs={"name": message.text}
    )

async def say_info(_, message, name: str = None):
    await message.reply(f"Name: {name} - Age: {message.text}")
```

🔗 **Related functions:**
- `unregister_steps(id)`: remove registered step for *id*.
- `clear()`: remove all registered steps (and cancels all wait_for's).

-------

### Plugins
📁 If you're using plugins in pyrogram, maybe you cannot use `pyrostep.listen()`, so you can use `pyrostep.listening_handler` function.

How? there's an example:
```python
# plugin file
from pyrogram import Client
import pyrostep

Client.on_message()
async def stephandler(client, message):
    await pyrostep.listening_handler(client, message)

# your other handlers
```

> [!WARNING]\
> We didn't test it completely.

## Shortcuts
✂️ **pyrostep** have some shortcuts and shorthands for you.

#### pyrostep.shortcuts.split_list()
split_list splites your list.

example:
```python
>>> from pyrostep import shortcuts
>>> split_list([1, 2, 3, 4, 5, 6], 2)
[[1, 2], [3, 4], [5, 6]]
>>> split_list([1, 2, 3], 2)
[[1, 2], [3]]
```


#### pyrostep.shortcuts.keyboard()
keyboard creates ReplyKeyboardMarkup from your list.

example:
```python
>>> from pyrostep import shortcuts
>>> buttons = [
...     [["Top Left"], ["Top Right"]],
...     [["Bottom | Request Contact", True, "request_contact"]]
... ]
>>> shortcuts.keyboard(buttons)
ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Top Left'), KeyboardButton(text='Top Right')], [KeyboardButton(text='Bottom | Request Contact', request_contact=True)]])
```

#### pyrostep.shortcuts.inlinekeyboard()
inlinekeyboard creates InlineKeyboardMarkup from your list.

example:
```python
>>> from pyrostep import shortcuts
>>> buttons = [
...     [["Top Left", "data_1"], ["Top Right", "data_2"]],
...     [["Bottom", "Your URL", "url"]]
... ]
>>> shortcuts.inlinekeyboard(buttons)
InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Top Left', callback_data='data_1'), InlineKeyboardButton(text='Top Right', callback_data='data_2')], [InlineKeyboardButton(text='Bottom', url='Your URL')]])
```

#### pyrostep.shortcuts.validation_channels()
validation_channels checks user is already in channels or not.
returns `True` if user is already in channels, returns `False` otherwise.

example:
```python
>>> from pyrostep import shortcuts
>>> user_id = 56392019
>>> channels = [-10279279837, -10823827873, 'channel_username']
>>> await validation_channels(app, user_id, channels)
True
```

## connection package
This package helps you to change *pyrogram connection* settings.

> [!NOTE]\
> All of these functions should be used before importing pyrogram

#### pyrostep.connection.connection_max_retries()
How many times does it try to connect (to proxy or telegram)?

-----

#### pyrostep.connection.invoke_max_retries()
How many times does it try to invoke a method?

-----

#### pyrostep.connection.session_start_timeout()
How many seconds to wait for connection?

-----

#### pyrostep.connection.session_max_retries()
How many times does it try to authenticate?

-----

Example:
```python
from pyrostep import connection
connection.connection_max_retries(3)
connection.invoke_max_retries(3)
connection.session_start_timeout(20)
connection.session_max_retries(2)

from pyrogram import Client
# code ...
```


