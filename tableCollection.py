from typing import *

from tableItems import TableItem


class TableCollection:
    """
    Class for a collection of tables, representing a certain database structure.
    """
    def __init__(self):
        self._particlesTable: TableItem = TableItem("Particle Data")
        self._sampleTable: TableItem = TableItem("Sample Info")
        self._metaTable: TableItem = TableItem("Meta Data")

    def getTableItems(self) -> List[TableItem]:
        return [self._particlesTable, self._sampleTable, self._metaTable]
