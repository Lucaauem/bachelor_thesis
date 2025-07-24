from database.callbacks.Events import Events as CallEvent
from typing import Callable

class CallbackHandler:
    _callbacks: dict[CallEvent, list[Callable]]

    def __init__(self) -> None:
        self._callbacks = {}

        for event in CallEvent:
            self._callbacks[event] = []

    def add(self, function: Callable, event: CallEvent) -> None:
        self._callbacks[event].append(function)

    def trigger(self, event: CallEvent, *args, **kwargs) -> None:
        for callable in self._callbacks[event]:
            callable(*args, **kwargs)
