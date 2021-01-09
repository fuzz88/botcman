import pytest
from unittest.mock import patch, mock_open

from fastapi import FastAPI


def test_init():
    # check if main returns "no errors"
    from app import main
    assert isinstance(main(), FastAPI) is True


@patch("builtins.open", new_callable=mock_open, read_data="data")
def test_with_mock(mock_open):
    pass
