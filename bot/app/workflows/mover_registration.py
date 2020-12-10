import asyncio
from transitions import Machine
from aiotg import Chat
import functools

from models import TelegramUser
from data.loader import load
from workflows.utils import get_user_data_from_api, emojize, perform_registration, escape_markdown


active_registrations = {}


def init(bot):
    @bot.command("/register")
    async def on_register(chat: Chat, match):
        if chat.is_group():
            return

        if active_registrations.get(chat.id, None) is not None:
            chat.send_text("Вы уже в процессе регистрации. Невозможно выполнить команду.", **{"parse_mode": "MarkdownV2"})
            return

        active_registrations[chat.id] = True

        registration = MoverRegistration(chat, active_registrations)
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

    def __init__(self, chat: Chat, active_registrations: dict):

        self.chat = chat
        self.send_md_text = functools.partial(self.chat.send_text, **{"parse_mode": "MarkdownV2"})
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
                r"^[0-9]{9}$",
                self.on_code,
            )
        )

    def on_waiting_code(self):
        self.send_md_text(escape_markdown(emojize(load("./data/messages/waiting_code.md"))))

    def on_code(self, chat: Chat, match):
        self.process_code(match.group(0))

    def on_code_received(self, code=None):
        if code is not None:
            loop = asyncio.get_event_loop()
            user = asyncio.run_coroutine_threadsafe(perform_registration(int(code), int(self.chat.id)), loop)

            def check_user(fut):
                self.user = fut.result()
                if self.user is not None:
                    self.good_code()
                else:
                    self.bad_code()

            user.add_done_callback(check_user)

    def on_success_reg(self):
        self.send_md_text(
            escape_markdown(emojize(load("./data/messages/good_code.md").format(name=self.user.get("fullname"))))
        )
        self.finish()

    def on_fail_reg(self):
        self.send_md_text(escape_markdown(emojize(load("./data/messages/bad_code.md"))))
        self.finish()

    def on_finish(self):
        self.chat.bot._commands.remove(
            (
                r"^[0-9]{9}$",
                self.on_code,
            )
        )
        self.active_registrations.pop(self.chat.id, None)
