import time
import pytest
import socket

from app.event_bus.wires import RedisWires

TEST_REDIS = {"host": "localhost", "port": 8091, "db": 0}


def is_redis_up(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
    except Exception:
        return False
    return True


@pytest.fixture(scope="session")
def redis_service():
    for _ in range(10):
        if is_redis_up(TEST_REDIS["host"], TEST_REDIS["port"]):
            return f"redis://{TEST_REDIS['host']}:{TEST_REDIS['port']}/{TEST_REDIS['db']}"
        time.sleep(0.1)
    pytest.exit("you need to start test_redis service to perform test")


def test_redis_wires_instantiation():
    wires = RedisWires()
    assert isinstance(wires, RedisWires) is True


def test_redis_wires_pub_sub_threaded(redis_service, reraise):
    wires = RedisWires()
    wires.connect(redis_service)

    def my_handler(message):
        with reraise:
            assert message["data"] == b"event1"

    wires.subscribe({"test_chan:1": my_handler})
    wires.start()
    wires.publish("test_chan:1", "event1")
    time.sleep(0.1)
    wires.stop()
