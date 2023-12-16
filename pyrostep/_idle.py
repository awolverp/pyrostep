from pyrogram import idle

async def safe_idle() -> None:
    import warnings
    warnings.warn(
        "This function is deprecated, use pyrogram.idle instead of this.", category=DeprecationWarning
    )

    await idle()
