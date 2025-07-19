import paho.mqtt.client as mqtt
from threading import Thread

class Client():
    _host: str
    _port: int
    _topic: str

    def __init__(self, host: str, port: int, topic: str) -> None:
        self._host = host
        self._port = port
        self._topic = topic

    def _on_connect(self, client, userdata, flags, rc) -> None:
        if rc == 0:
            print('MQTT-Client: Connected to MQTT Broker!')
            client.subscribe(self._topic)
        else:
            print(f'MQTT-Client: Failed to connect, return code {rc}')

    def _on_message(self, client, userdata, msg):
        print(f'MQTT-Client: Message received: {msg.topic} -> {msg.payload.decode()}')

    def connect(self) -> None:
        client = mqtt.Client()
        client.connect(self._host, self._port)

        client.on_connect = self._on_connect
        client.on_message = self._on_message

        thread = Thread(target= client.loop_forever)
        thread.start()
