import time
import pytest
import socket
import aioredis

from app.event_bus.wires import RedisWires

TEST_REDIS = {"host": "localhost", "port": 8091}


@pytest.mark.asyncio
async def test_redis_wires_instantiation():
    wires = RedisWires()
    assert isinstance(wires, RedisWires) is True
    del wires


def is_redis_up(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
    except Exception:
        return False
    return True


@pytest.fixture(scope="session")
def redis_service():
    while True:
        if is_redis_up(TEST_REDIS["host"], TEST_REDIS["port"]):
            return
        time.sleep(1)


@pytest.mark.asyncio
async def test_redis_wires_connect(redis_service):
    wires = RedisWires()
    await wires._connect(TEST_REDIS["host"], TEST_REDIS["port"])

    assert isinstance(wires._pub, aioredis.RedisConnection) is True
    assert isinstance(wires._sub, aioredis.RedisConnection) is True


@pytest.mark.asyncio
async def test_redis_wires_pub_sub(redis_service):
    wires = RedisWires()
    await wires._connect(TEST_REDIS["host"], TEST_REDIS["port"])

    class Success(Exception):
        pass

    async def my_recv_callback(data):
        assert data == b"event"
        raise Success

    await wires._register_receiver_callback(my_recv_callback)
    await wires._subscribe([b"test_chan:1"])
    await wires._publish(b"test_chan:1", b"event")
    with pytest.raises(Success):
        await wires._receiver(num=1)
