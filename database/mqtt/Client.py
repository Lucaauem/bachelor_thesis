import paho.mqtt.client as mqtt
from threading import Thread
from typing import Callable

class Client():
    _host: str
    _port: int
    _topic: str
    _custom_on_message: Callable

    def __init__(self, host: str, port: int, topic: str, on_message: Callable) -> None:
        self._host = host
        self._port = port
        self._topic = topic
        self._custom_on_message = on_message

    def _on_connect(self, client, userdata, flags, rc) -> None:
        if rc == 0:
            print('MQTT-Client: Connected to MQTT Broker!')
            client.subscribe(self._topic)
        else:
            print(f'MQTT-Client: Failed to connect, return code {rc}')


    # TODO Maybe cleaner?
    def _on_message(self, client, userdata, msg):
        self._custom_on_message(msg.payload.decode())

    def connect(self) -> None:
        client = mqtt.Client()
        client.connect(self._host, self._port)

        client.on_connect = self._on_connect
        client.on_message = self._on_message

        thread = Thread(target= client.loop_forever)
        thread.start()
