from __future__ import annotations
from typing import TYPE_CHECKING
import paho.mqtt.client as mqtt
from threading import Thread
from database.Log import log

if TYPE_CHECKING:
    from typing import Callable


class Client():
    _id: str
    _host: str
    _port: int
    _topic: str
    _custom_on_message: Callable

    def __init__(self, id: str, host: str, port: int, topic: str, on_message: Callable) -> None:
        self._id = id
        self._host = host
        self._port = port
        self._topic = topic
        self._custom_on_message = on_message

    def _on_connect(self, client, userdata, flags, rc) -> None:
        if rc == 0:
            log(f'MQTT Client [{self._id}]: Connected successfully')
            client.subscribe(self._topic)
        else:
            log(f'MQTT Client [{self._id}]: Failed to connect, return code {rc}')

    # TODO Maybe cleaner?
    def _on_message(self, client, userdata, msg):
        self._custom_on_message(msg.payload.decode())

    def connect(self) -> None:
        try:
            log(f'MQTT Client [{self._id}]: Connecting...')
            client = mqtt.Client()

            client.connect(self._host, self._port)

            client.on_connect = self._on_connect
            client.on_message = self._on_message

            thread = Thread(target= client.loop_forever)
            thread.start()
        except:
            log(f'MQTT Client [{self._id}]: Failed to connect')
