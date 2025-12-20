import asyncio
import importlib
from pyrogram import idle
from pyrogram.types import BotCommand
from pytgcalls.exceptions import NoActiveGroupCall
import config
from ShrutiMusic import LOGGER, app, userbot
from ShrutiMusic.core.call import Nand
from ShrutiMusic.misc import sudo
from ShrutiMusic.plugins import ALL_MODULES
from ShrutiMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS
import signal

stop_event = asyncio.Event()

def stop_signal_handler(*_):
    LOGGER("ShrutiMusic").info("🛑 Stop signal received. Shutting down...")
    stop_event.set()

async def setup_bot_commands():
    try:
        await app.set_bot_commands(COMMANDS)
        LOGGER("ShrutiMusic").info("Bot commands set successfully!")
    except Exception as e:
        LOGGER("ShrutiMusic").error(f"Failed to set bot commands: {str(e)}")

async def init():
    # Register signals
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, stop_signal_handler)
    loop.add_signal_handler(signal.SIGTERM, stop_signal_handler)

    if not any([config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5]):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        return

    await sudo()

    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass

    await app.start()
    await setup_bot_commands()

    for all_module in ALL_MODULES:
        importlib.import_module("ShrutiMusic.plugins" + all_module)

    LOGGER("ShrutiMusic.plugins").info("Successfully Imported Modules...")

    await userbot.start()
    await Nand.start()

    try:
        await Nand.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("ShrutiMusic").error(
            "Please turn on the videochat of your log group/channel.\n\nStopping Bot..."
        )
        return
    except:
        pass

    await Nand.decorators()

    LOGGER("ShrutiMusic").info(
        "Shruti Music Started Successfully.\n\nDon't forget to visit @ShrutiBots"
    )

    # Wait until stop signal
    await stop_event.wait()

    # Stop everything cleanly
    await app.stop()
    await userbot.stop()
    LOGGER("ShrutiMusic").info("Stopping Shruti Music Bot...🥺")

if __name__ == "__main__":
    asyncio.run(init())
