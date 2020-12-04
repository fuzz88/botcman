import asyncio
from transitions import Machine
from aiotg import Chat

from models import TelegramUser
from data.loader import load
from workflows.utils import get_user_data_from_api, emojize


active_registrations = {}


def init(bot):
    @bot.command("/register")
    async def on_register(chat: Chat, match):
        if chat.is_group():
            return

        if active_registrations.get(chat.id, None) is not None:
            chat.send_text("already in process", **{"parse_mode": "MarkdownV2"})
            return

        user = await get_user_data_from_api(chat.bot, chat.id)

        active_registrations[chat.id] = True

        registration = MoverRegistration(chat, user, active_registrations)
        registration.start()


class MoverRegistration(object):

    states = ["lets_ask_code", "waiting_code", "code_received", "success_reg", "fail_reg", "finished"]

    transitions = [
        ["start", "lets_ask_code", "waiting_code"],
        ["process_code", "waiting_code", "code_received", None, None, None, "on_code_received"],
        ["good_code", "code_received", "success_reg"],
        ["bad_code", "code_received", "fail_reg"],
        ["finish", "*", "finished"],
    ]

    def __init__(self, chat: Chat, user: TelegramUser, active_registrations: dict):

        self.chat = chat
        self.user = user
        self.active_registrations = active_registrations

        self.machine = Machine(
            model=self,
            states=MoverRegistration.states,
            transitions=MoverRegistration.transitions,
            initial="lets_ask_code",
        )
        self.machine.on_exit_lets_ask_code("on_init")
        self.machine.on_enter_waiting_code("on_waiting_code")
        self.machine.on_enter_success_reg("on_success_reg")
        self.machine.on_enter_fail_reg("on_fail_reg")
        self.machine.on_enter_finished("on_finish")

    def on_init(self):
        self.chat.bot._commands.append(
            (
                r"^[0-9]{12}$",
                self.on_code,
            )
        )

    def on_waiting_code(self):
        self.chat.send_text("please send me code", **{"parse_mode": "MarkdownV2"})
        self.chat.send_text("i am waiting", **{"parse_mode": "MarkdownV2"})

    def on_code(self, chat: Chat, match):
        self.process_code(match.group(0))

    def on_code_received(self, code=None):
        if int(code) == 123456123654:
            self.good_code()
        else:
            self.bad_code()

    def on_success_reg(self):
        self.chat.send_text(
            emojize(load("./data/messages/good_code.md").format(name="Ivan")), **{"parse_mode": "MarkdownV2"}
        )
        self.chat.bot._commands.remove(
            (
                r"^[0-9]{12}$",
                self.on_code,
            )
        )
        self.finish()

    def on_fail_reg(self):
        self.chat.send_text(
            emojize(load("./data/messages/bad_code.md")), **{"parse_mode": "MarkdownV2"}
        )
        self.chat.bot._commands.remove(
            (
                r"^[0-9]{12}$",
                self.on_code,
            )
        )
        self.finish()

    def on_finish(self):
        self.active_registrations.pop(self.chat.id, None)
