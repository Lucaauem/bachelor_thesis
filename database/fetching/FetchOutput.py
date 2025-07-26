from __future__ import annotations
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from database.fetching.FetchStatus import FetchStatus

class FetchOutput:
    _data: Any
    _status: FetchStatus
    
    def __init__(self, data: Any, status: FetchStatus) -> None:
        self._data = data
        self._status = status

    @property
    def data(self) -> Any:
        return self._data
    
    @property
    def status(self) -> FetchStatus:
        return self._status

    def serialize(self) -> dict:
        return {'data': self._data, 'status': self._status}
