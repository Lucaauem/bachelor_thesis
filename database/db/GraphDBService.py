from __future__ import annotations
from typing import TYPE_CHECKING
from neo4j import GraphDatabase

if TYPE_CHECKING:
    from neo4j import Driver

class GraphDBService:
    _driver: Driver

    def __init__(self, uri: str, user: str, password: str) -> None:
        self._driver = GraphDatabase.driver(uri, auth=(user, password))