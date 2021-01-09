import config

from .utils import (
    получить_инфу_об_отправителе_от_апи_телеграмма,
    сохранить_инфу_о_пользователе_в_базу_данных,
    есть_ли_у_нас_в_базе_такой_пользователь,
    escape_markdown,
    emojize,
)
from .data.loader import load


def init(bot):
    @bot.command(r"/start")
    async def приветствуем_пользователя_и_сохраняем_в_базу_если_он_новый(chat, match):
        await chat.send_text(escape_markdown(emojize(load("messages/on_start.md"))), **{"parse_mode": "MarkdownV2"})

        if await есть_ли_у_нас_в_базе_такой_пользователь(chat.sender["id"]) is False:
            await сохранить_инфу_о_пользователе_в_базу_данных(
                await получить_инфу_об_отправителе_от_апи_телеграмма(bot, chat.sender["id"])
            )
