from pyrogram import idle

async def safe_idle() -> None:
    await idle()
