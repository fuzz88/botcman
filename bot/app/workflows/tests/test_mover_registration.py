import pytest
from unittest.mock import patch, mock_open
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

@patch("builtins.open", new_callable=mock_open, read_data="data")
def test_mover_registration_pipeline_process_code(mock_open):

    user_id = 55667788

    chat = ChatStub()

    registrations = {}

    current_registration = registrations[user_id] = MoverRegistration(chat, {})

    assert current_registration.state == "lets_ask_code"

    current_registration.start()

    assert current_registration.state == "waiting_code"

    current_registration.process_code(5)

    assert current_registration.state == "code_received"

    current_registration.user = {"fullname": "test"}

    current_registration.good_code()

    assert current_registration.state == "finished"


@patch("builtins.open", new_callable=mock_open, read_data="data")
def test_mover_registration_pipeline_bad_code(mock_open):

    user_id = 55667788

    chat = ChatStub()

    registrations = {}

    current_registration = registrations[user_id] = MoverRegistration(chat, {})

    assert current_registration.state == "lets_ask_code"

    current_registration.start()

    assert current_registration.state == "waiting_code"

    current_registration.process_code(5)

    assert current_registration.state == "code_received"

    current_registration.user = {"fullname": "test"}

    current_registration.bad_code()

    assert current_registration.state == "finished"
