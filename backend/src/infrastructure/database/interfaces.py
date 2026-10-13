# interfaces.py

from typing import Dict, Any, Protocol, runtime_checkable
from types import TracebackType

class ICursor(Protocol):
    async def execute(
        self,
        query: str,
        params: tuple | dict | None = None,
    ) -> None:
        ...

    async def fetch_one(self) -> dict[str, Any] | None:
        ...

    async def fetch_many(self, size: int) -> list[dict[str, Any]]:
        ...

    async def close(self) -> None:
        ...


class ITransactionManager(Protocol):
    async def __aenter__(self) -> "ITransactionManager":
        ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        ...


class IConnection(Protocol):
    async def create_cursor(self) -> ICursor:
        ...

    async def create_transaction(self) -> ITransactionManager:
        ...

    async def close(self) -> None:
        ...


class IConnectionPool(Protocol):
    async def acquire(self) -> IConnection:
        ...

    async def release(self, connection: IConnection) -> None:
        ...

    async def close(self) -> None:
        ...

class IUnitOfWork(Protocol):
    """
    The job of a unit of work bound to a session is to track all business operations and 
    data changes in-memory during a single interaction and 
    commit them to the database as one single atomic transaction
    """

    def register_new(self, entity) -> None:
        ...

    def register_dirty(self, entity) -> None:
        ...

    def register_deleted(self, entity) -> None:
        ...

    async def commit(self) -> None:
        ...

    

@runtime_checkable
class IQueryBuilder(Protocol):
    def __str__(self) -> str:
        ...
    def create_table(self) -> "IQueryBuilder":
        ...
    
    def drop_table(self) -> "IQueryBuilder":
        ...
    
    def insert(self, *cols) -> "IQueryBuilder":
        ...

    def update(self) -> "IQueryBuilder":
        ...
    
    def from_(self) -> "IQueryBuilder":
        ...
    
    def select(self) -> "IQueryBuilder":
        ...

    def set(self, *rows) -> "IQueryBuilder":
        ...

    def where(self, criterion: type) -> "IQueryBuilder":
        ...

    def groupby(self, *fields) -> "IQueryBuilder":
        ...
    
    def having(self, criterion) -> "IQueryBuilder":
        ...
    
    def orderby(self, *fields, **kwargs) -> "IQueryBuilder":
        ...

class ISession:
    async def __aenter__(self) -> "ISession":
        ...
    
    async def __aexit__( 
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None
        ) -> None:
        ...

    async def _cleanup(self) -> None:
        ...

    async def execute(
        self,
        query: str,
        params: tuple | dict | None = None
        ) -> None:
        ...

class IEntity:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class IMapperFactory:
    def register(self, table_name: str, columns: dict[str, Any]) -> None:
        ...

    def extract(self, entity: IEntity) -> tuple[str, Dict[str, Any]]:
        ...