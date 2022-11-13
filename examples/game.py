import functools
import random
import pyrostep

from pyrogram import Client, filters, types

app = Client(...)
pyrostep.listen(app, filters=~filters.command("cancel"))

@app.on_message(filters.command("start"))
async def start(_, msg: types.Message):
    await msg.reply(
        "Hi Welcome To My Pyrostep test.\n"
        "Send /game_ask to start game (with ask handling) or /game_step (with step handling)."
    )

@app.on_message(filters.command("cancel"))
async def cancel(_, msg: types.Message):
    await pyrostep.unregister_steps(msg.from_user.id)
    await msg.reply(
        "Operation Cancelled."
    )

""" Step Handling Example """

@app.on_message(filters.command("game_step"))
async def step_handling(_, msg: types.Message):
    
    num = random.choice([1, 2, 3, 4, 5])

    await msg.reply(
        "Ok, I made my choice, guess it:"
    )

    await pyrostep.register_next_step(
        msg.from_user.id,
        functools.partial(user_choice, num=num)
    )

async def user_choice(_, msg: types.Message, num=None):
    try:
        choose = int(msg.text)
    except ValueError:
        await msg.reply(
            "Please send number!"
        )
        # loop on this step
        await pyrostep.register_next_step(
            msg.from_user.id,
            functools.partial(user_choice, num=num)
        )
        return

    if choose == num:
        await msg.reply(
            "Oh you guess my choice! you win!"
        )
        return
    
    await msg.reply(
        "No, Your choice is %s, try again:" % ("small", "big")[choose > num]
    )

    # loop on this step
    await pyrostep.register_next_step(
        msg.from_user.id,
        functools.partial(user_choice, num=num)
    )

""" Ask Handling Example """

@app.on_message(filters.command("game_ask"))
async def ask_handling(_, msg: types.Message):

    num = random.choice([1, 2, 3, 4, 5])

    await msg.reply(
        "Ok, I made my choice, guess it:"
    )

    while True:

        answer = await pyrostep.wait_for(msg.from_user.id)

        try:
            choose = int(answer.text)
        except ValueError:
            await msg.reply(
                "Please send number!"
            )
            continue
    
        if choose == num:
            await msg.reply(
                "Oh you guess my choice! you win!"
            )
            break
        
        await msg.reply(
            "No, Your choice is %s, try again:" % ("small", "big")[choose > num]
        )

async def main():
    await app.start()
    print("started")
    
    await pyrostep.safe_idle()
    await app.stop()

app.run(main())
