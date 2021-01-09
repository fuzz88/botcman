import logging
import asyncio
import functools

from transitions import Machine
from aiotg import Chat

from models import TelegramUser

from .utils import emojize, выполнить_регистрацию_пользователя, escape_markdown
from .data.loader import load


log = logging.getLogger(__name__)


def init(bot):

    current_registrations = {}
    # словарь в пространстве init.
    # хранит состояние текущих активных регистраций
    # например, сейчас:
    # True для любой регистрации, которая не завершена.
    # когда регистрация доходит до состояния finish,
    # она сама вычёркивает себя из этого словаря.

    @bot.command("/register")
    async def on_register(chat: Chat, match):
        if chat.is_group():
            return
        # используется так
        if current_registrations.get(chat.id, None) is not None:
            chat.send_text("Вы уже в процессе регистрации. Невозможно выполнить команду.")
            return
        # так
        current_registrations[chat.id] = True

        MoverRegistration(chat, current_registrations).стартуем()


class MoverRegistration(object):
    # описывает конечный автомат, который производит диалог с пользователем при регистрации (получении /register).
    # TODO: can be a bit translated into russian. ^_^ just kiddin.
    states = ["начало", "ожидаем_регистрационный_код", "code_received", "success_reg", "fail_reg", "finished"]

    transitions = [
        ["стартуем", "начало", "ожидаем_регистрационный_код"],
        ["process_code", "ожидаем_регистрационный_код", "code_received", None, None, None, "on_code_received"],
        ["good_code", "code_received", "success_reg"],
        ["bad_code", "code_received", "fail_reg"],
        ["finish", "*", "finished"],
    ]

    def __init__(self, chat: Chat, current_registrations: dict):

        self.chat = chat
        self.send_md_text = functools.partial(self.chat.send_text, **{"parse_mode": "MarkdownV2"})
        self.current_registrations = current_registrations

        self.machine = Machine(
            model=self,
            states=MoverRegistration.states,
            transitions=MoverRegistration.transitions,
            initial="начало",
        )
        self.machine.on_enter_ожидаем_регистрационный_код("on_init")
        self.machine.on_enter_success_reg("on_success_reg")
        self.machine.on_enter_fail_reg("on_fail_reg")
        self.machine.on_enter_finished("on_finish")

    def on_init(self):
        self.send_md_text(escape_markdown(emojize(load("messages/waiting_code.md"))))
        # add message handler in aiotg.Bot:
        self.chat.bot._commands.append(
            (
                r"^[0-9]{9}$",
                self.on_code,
            )
        )

    def on_code_received(self, code):
        def check_user(future):
            self.user = future.result()
            if self.user is None:
                self.bad_code()
            else:
                self.good_code()

        loop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(
            выполнить_регистрацию_пользователя(int(code), int(self.chat.id)), loop
        ).add_done_callback(check_user)

        # remove message handler in aiotg.Bot
        self.chat.bot._commands.remove(
            (
                r"^[0-9]{9}$",
                self.on_code,
            )
        )

    def on_success_reg(self):
        self.send_md_text(
            escape_markdown(emojize(load("messages/good_code.md").format(name=self.user.get("fullname"))))
        )
        self.finish()

    def on_fail_reg(self):
        # отправляем примерно такое:
        #
        # | Неправильный код. ::confused::
        # |
        # | /register
        #
        # приглашая к новой регистрации.

        self.send_md_text(escape_markdown(emojize(load("messages/bad_code.md"))))
        self.finish()

    def on_finish(self):
        (lambda: self.current_registrations.pop(self.chat.id, None))()  # или так

    def on_code(self, chat: Chat, match):
        # обработчик сообщений, передаваемый интерфейсу бота. коллбэк.

        # вызывает переход process_code, обрабатывающий полученный код.

        # "match" seems to be re.Match, see aiotg docs
        self.process_code(match.group(0))
