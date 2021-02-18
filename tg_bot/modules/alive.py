from tg_bot import SUDO_USERS, OWNER_ID, tg_bot
from tg_bot.events import register


@register(pattern="^/alive")
async def alive(event):
    if event.sender_id == OWNER_ID:
        await event.reply("I'm Alive Master")
    elif event.sender_id in DEV_USERS:
        await event.reply("I'm Alive Co-Master")
    elif event.sender_id in SUDO_USERS:
        await event.reply("I'm Alive Pro!")
    elif event.sender_id not in SUDO_USERS:
        await event.reply("✰彡[Black Legend]彡✰")
