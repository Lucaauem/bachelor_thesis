from __future__ import annotations
from typing import TYPE_CHECKING
from database.callbacks.Events import Events as CallEvent
from typing import Callable

if TYPE_CHECKING:
    from database.DBFramework import DBFramework

class CallbackHandler:
    _callbacks: dict[CallEvent, list[Callable]]
    _fw: DBFramework

    def __init__(self, fw_instance: DBFramework) -> None:
        self._callbacks = {}
        self._fw = fw_instance

        for event in CallEvent:
            self._callbacks[event] = []

        # Default events
        self._callbacks[CallEvent.INVALID_DATASET].append(lambda data: self._fw.DB.active_graphdb.add_invalid_dataset(data))

    def add(self, function: Callable, event: CallEvent) -> None:
        self._callbacks[event].append(function)

    def trigger(self, event: CallEvent, *args, **kwargs) -> None:
        for callable in self._callbacks[event]:
            callable(*args, **kwargs)
