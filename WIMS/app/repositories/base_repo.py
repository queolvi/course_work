from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic, Optional

from app.core.database import db

T = TypeVar("T")

class BaseRepository(ABC, Generic[T]):
    def __init__(self):
        self.db = db

    @abstractmethod
    def _map_row(self, row) -> T:
        pass

    def _execute(self, query: str, params: tuple = ()):
        return self.db.execute(query, params)

    def _fetch_all(self, query: str, params: tuple = ()) -> List[T]:
        cursor = self._execute(query, params)
        return [self._map_row(row) for row in cursor.fetchall()]

    def _fetch_one(self, query: str, params: tuple = ()) -> Optional[T]:
        cursor = self._execute(query, params)
        row = cursor.fetchone()
        return self._map_row(row) if row else None

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()