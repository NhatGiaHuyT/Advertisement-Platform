from typing import Any

from pypika import Table, Query, Field
from pypika.terms import EmptyCriterion, Term
from .interfaces import IQueryBuilder

class QueryBuilder(IQueryBuilder):
    def __init__(self, table_name: str):
        self._table_name = table_name
        self._table = Table(table_name)
        self._query = None
    
    def create_table(self, *cols) -> IQueryBuilder:
        self._query = Query.create_table(self._table_name)
        if cols:
            for field in cols:
                self._query = self._query.columns(field)
        else:
            self._query = f'CREATE TABLE "{self._table_name}" ()'
            
        return self

    def drop_table(self) -> IQueryBuilder:
        self._query = Query.drop_table(self._table_name)
        return self

    def select(self, *cols) -> IQueryBuilder:
        self._query = Query.from_(self._table)

        if cols:
            for field in cols:
                self._query = self._query.select(self._table[field])
        else:
            self._query = self._query.select("*")
                
        return self

    def insert(self, *cols) -> IQueryBuilder:
        self._query = Query.into(self._table)
     
        self._query = self._query.insert(cols)
 
        return self

    def where(self, criterion) -> IQueryBuilder:
        self._query = self._query.where(criterion)
        return self
    
    def update(self, row, value) -> IQueryBuilder:
        self._query = Query.update(self._table).set(row, value)
        if not row or not value:
            raise ValueError("Row and value must be provided for update operation.")
        return self

    def build(self) -> str:
            return str(self._query)

    def __str__(self) -> str:
        return str(self._query)