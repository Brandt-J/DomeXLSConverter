from dataclasses import dataclass
from typing import *


@dataclass
class TableItem:
    """
    Container class for storing fields for a specific table.
    """
    name: str
    _fields: Union[None, dict] = None

    def correctlySet(self) -> bool:
        """
        Returns, if all values of the contents dict are set correctly.
        :return:
        """
        correct: bool = False
        if self._fields is not None:
            correct = None not in self._fields.values()
        return correct


class InstitutionTable(TableItem):
    def __init__(self):
        super(InstitutionTable, self).__init__("Institution")
        self._fields = {"Facility Name": None,
                        "Country": None}