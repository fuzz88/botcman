import pytest
from types import SimpleNamespace

from workflows.mover_registration import MoverRegistration

from models import TelegramUser


class ChatStub:
    def __init__(self):
        self.bot = SimpleNamespace()
        self.bot.send_text = self.send_text
        self.bot._commands = []
        self.id = 0

    def send_text(self, message, **options):
        pass


def test_mover_registration_pipeline_process_code():

    user_id = 55667788

    chat = ChatStub()

    user = TelegramUser(username="test_user", last_name="Bin", first_name="Mr", chat_id=user_id)

    registrations = {}

    current_registration = registrations[user_id] = MoverRegistration(chat, user, {})

    assert current_registration.state == "lets_ask_code"

    current_registration.start()

    assert current_registration.state == "waiting_code"

    current_registration.process_code(7)

    assert current_registration.state == "finished"


def test_mover_registration_pipeline_bad_code():

    user_id = 55667788

    chat = ChatStub()

    user = TelegramUser(username="test_user", last_name="Bin", first_name="Mr", chat_id=user_id)

    registrations = {}

    current_registration = registrations[user_id] = MoverRegistration(chat, user, {})

    assert current_registration.state == "lets_ask_code"

    current_registration.start()

    assert current_registration.state == "waiting_code"

    current_registration.process_code(5)

    assert current_registration.state == "finished"
