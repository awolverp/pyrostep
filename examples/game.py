import random
import pyrostep

from pyrogram import Client, filters, types, idle

app = Client(...)
pyrostep.listen(app)


@app.on_message(filters.command("start"))
async def start(_, msg: types.Message):
    await msg.reply(
        "Hi Welcome To My Pyrostep test.\n"
        "Send /game_ask to start game (with ask handling) or /game_step (with step handling)."
    )


""" Step Handling Example """


@app.on_message(filters.command("game_step"))
async def step_handling(_, msg: types.Message):
    num = random.choice([1, 2, 3, 4, 5])

    await msg.reply("Ok, I made my choice, guess it:")

    await pyrostep.register_next_step(msg.from_user.id, user_choice, kwargs={"num": num})


async def user_choice(_, msg: types.Message, num: int = None):
    try:
        choose = int(msg.text)
    except ValueError:
        await msg.reply("Please send number!")
        # loop on this step
        await pyrostep.register_next_step(msg.from_user.id, user_choice, kwargs={"num": num})
        return

    if choose == num:
        await msg.reply("Oh you guess my choice! you win!")
        return

    await msg.reply("No, Your choice is %s, try again:" % ("small", "big")[choose > num])

    # loop on this step
    await pyrostep.register_next_step(msg.from_user.id, user_choice, kwargs={"num": num})


""" Ask Handling Example """


@app.on_message(filters.command("game_ask"))
async def ask_handling(_, msg: types.Message):
    num = random.choice([1, 2, 3, 4, 5])

    await msg.reply("Ok, I made my choice, guess it:")

    while True:
        answer = await pyrostep.wait_for(msg.from_user.id)

        try:
            choose = int(answer.text)
        except ValueError:
            await msg.reply("Please send number!")
            continue

        if choose == num:
            await msg.reply("Oh you guess my choice! you win!")
            break

        await msg.reply("No, Your choice is %s, try again:" % ("small", "big")[choose > num])


async def main():
    await app.start()
    await idle()
    await app.stop()


app.run(main())
