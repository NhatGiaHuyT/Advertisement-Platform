from typing import Any

from infrastructure.database.interfaces import IEntity, IMapperFactory


class Metadata:
    def __init__(self, table_name: str, columns: dict[str, type[Any]]):
        self._table_name = table_name
        self._columns = columns


class MapperFactory(IMapperFactory):
    def __init__(self):
        self._registry = {}  # Dict[Type, Metadata]

    def register(self, cls: type, table_name: str, columns: dict[str, type[Any]]) -> None:
        self._registry[cls] = Metadata(table_name, columns)

    def extract(self, entity: IEntity) -> tuple[str, dict[str, Any]]:
        entity_type = type(entity)

        if entity_type not in self._registry:
            raise ValueError(f"Entity type {entity_type.__name__} is not registered in the mapper factory.")

        metadata = self._registry[entity_type]

        db_data = {}

        for entity_field, db_column in metadata._columns.items():
            if hasattr(entity, entity_field):
                db_data[db_column] = getattr(entity, entity_field)
            else:
                raise ValueError(f"Entity {entity_type.__name__} does not have the field '{entity_field}'.")
