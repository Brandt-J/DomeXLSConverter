from dataclasses import dataclass
from typing import *


@dataclass
class TableItem:
    """
    Container class for storing fields for a specific table.
    """
    name: str
    _fields: Union[None, dict] = None

    def initializeFields(self, fieldnames: List[str]) -> None:
        """
        Initializes the fields dictionary with the given field names.
        :param fieldnames:
        :return:
        """
        self._fields = {}
        for name in fieldnames:
            self._fields[name] = None

    def correctlySet(self) -> bool:
        """
        Returns, if all values of the contents dict are set correctly.
        :return:
        """
        correct: bool = False
        if self._fields is not None:
            correct = None not in self._fields.values()
        return correct
