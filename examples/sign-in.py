import asyncio
import pyrostep
pyrostep.install()

import functools
from pyrogram import Client, filters, types

app = Client(...)
app.listen(filters=~filters.command("cancel"))

VALID_USERNAME = "awolverp"
VALID_PASSWORD = "none"

@app.on_message(filters.command("start"))
async def start(_, msg: types.Message):
    await msg.reply(
        "Hi Welcome To My Pyrostep test.\n"
        "Send /step to see step handling, or send /ask to see ask handling."
    )

@app.on_message(filters.command("cancel"))
async def cancel(_, msg: types.Message):
    await app.unregister_steps(msg.from_user.id)

""" Step Handling Example """

@app.on_message(filters.command("step"))
async def step_handling(_, msg: types.Message):
    await msg.reply(
        "🔖 What's your username? (cancel with /cancel)"
    )

    await app.register_next_step(msg.from_user.id, get_username)

async def get_username(_, msg: types.Message):
    username = msg.text

    await msg.reply(
        "🏦 And password? (cancel with /cancel)"
    )

    await app.register_next_step(
        msg.from_user.id,
        functools.partial(get_password, username=username)
    )

async def get_password(_, msg: types.Message, username: str):
    password = msg.text

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        await msg.reply(
            "Successfuly signed in."
        )
        return
    
    await msg.reply(
        "Invalid password or username! (send /step to try again)"
    )

""" Ask Handling Example """

@app.on_message(filters.command("ask"))
async def ask_handling(_, msg: types.Message):

    await msg.reply(
        "🔖 What's your username? (cancel with /cancel)"
    )
    try:
        username: str = (await app.wait_for(msg.from_user.id)).text
    except asyncio.CancelledError:
        await msg.reply(
            "Operation cancelled."
        )

    await msg.reply(
        "🏦 And password? (cancel with /cancel)"
    )
    try:
        password: str = (await app.wait_for(msg.from_user.id)).text
    except asyncio.CancelledError:
        await msg.reply(
            "Operation cancelled."
        )

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        await msg.reply(
            "Successfuly signed in."
        )
        return
    
    await msg.reply(
        "Invalid password or username! (send /ask to try again)"
    )

async def main():
    await app.start()
    
    # Recommended use this instead of idle when using pyrostep.
    await pyrostep.safe_idle()
    await app.stop()

app.run(main())
