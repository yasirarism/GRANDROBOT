import random

from telegram import Bot, Update, MessageEntity
from telegram.ext import Filters, run_async

from tg_bot import dispatcher
from tg_bot.modules.disable import DisableAbleCommandHandler, DisableAbleRegexHandler, DisableAbleMessageHandler
from tg_bot.modules.sql import afk_sql as sql
from tg_bot.modules.users import get_user_id

AFK_GROUP = 7
AFK_REPLY_GROUP = 8


@run_async
def afk(bot: Bot, update: Update):
    args = update.effective_message.text.split(None, 1)
    reason = args[1] if len(args) >= 2 else ""
    sql.set_afk(update.effective_user.id, reason)
    update.effective_message.reply_text(
        f"{update.effective_user.first_name} sekarang AFK!"
    )


@run_async
def no_longer_afk(bot: Bot, update: Update):
    user = update.effective_user

    if not user:
        return

    if res := sql.rm_afk(user.id):
        options = [
            '{} disini!',
            '{} kembali!',
            '{} sekarang dichat!',
            '{} sudah bangun!',
            '{} kembali online!',
            '{} akhirnya disini!',
            'Selamat datang kembali!, {}',
            'Dimanakah {}?\nOh di chat itu!'
        ]
        chosen_option = random.choice(options)
        update.effective_message.reply_text(chosen_option.format(update.effective_user.first_name))


@run_async
def reply_afk(bot: Bot, update: Update):
    message = update.effective_message
    entities = message.parse_entities([MessageEntity.TEXT_MENTION, MessageEntity.MENTION])

    if message.entities and entities:
        for ent in entities:
            if ent.type == MessageEntity.TEXT_MENTION:
                user_id = ent.user.id
                fst_name = ent.user.first_name

            elif ent.type == MessageEntity.MENTION:
                user_id = get_user_id(message.text[ent.offset:ent.offset + ent.length])
                if not user_id:
                    return
                chat = bot.get_chat(user_id)
                fst_name = chat.first_name

            else:
                return

            if sql.is_afk(user_id):
                valid, reason = sql.check_afk_status(user_id)
                if valid:
                    if not reason:
                        res = f"── 「 AFK MODE 」 ──\n\nSssttt! {fst_name} lagi AFK, jangan diganggu!"
                    else:
                        res = f"── 「 AFK MODE 」 ──\n\nSssttt! {fst_name} lagi AFK, jangan diganggu!!\n➸ Alasan:\n{reason}"
                    message.reply_text(res)


def __gdpr__(user_id):
    sql.rm_afk(user_id)


__help__ = """
 - /afk <reason>: menandai kamu sedang AFK(away from keyboard).
 - brb <reason>: sama kayak perintah AFK - tapi bukan sebuah command.
Ketika ditandai AFK, semua mention akan dibalas dengan pesan bahwa kamu sedang AFK!
"""

AFK_HANDLER = DisableAbleCommandHandler("afk", afk)
AFK_REGEX_HANDLER = DisableAbleRegexHandler(r"(?i)brb", afk, friendly="afk")
NO_AFK_HANDLER = DisableAbleMessageHandler(Filters.all & Filters.group, no_longer_afk, friendly="afk")
AFK_REPLY_HANDLER = DisableAbleMessageHandler((Filters.entity(MessageEntity.MENTION) | Filters.entity(MessageEntity.TEXT_MENTION)) & Filters.group, reply_afk, friendly="afk")

dispatcher.add_handler(AFK_HANDLER, AFK_GROUP)
dispatcher.add_handler(AFK_REGEX_HANDLER, AFK_GROUP)
dispatcher.add_handler(NO_AFK_HANDLER, AFK_GROUP)
dispatcher.add_handler(AFK_REPLY_HANDLER, AFK_REPLY_GROUP)

__mod_name__ = "AFK"
__command_list__ = ["afk"]
__handlers__ = [(AFK_HANDLER, AFK_GROUP), (AFK_REGEX_HANDLER, AFK_GROUP), (NO_AFK_HANDLER, AFK_GROUP),
                (AFK_REPLY_HANDLER, AFK_REPLY_GROUP)]
