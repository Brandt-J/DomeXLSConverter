from dataclasses import dataclass, field
from typing import *

from dataimport.domeCodes import DomeCode


@dataclass
class Field:
    """
    Class for storing information to each field, especially if it was set (content != None) and if the field is mandatory
    """
    name: str
    content: Optional['DomeCode'] = None
    mandatory: bool = True

    def isComplete(self) -> bool:
        """
        Returns if the field is completed or still needs to be set.
        :return:
        """
        return type(self.content) == DomeCode if self.mandatory else True


@dataclass
class TableItem:
    """
    Container class for storing fields for a specific table.
    """
    name: str
    _fields: List[Field] = field(default_factory=list)

    def correctlySet(self) -> bool:
        """
        Returns, if all values of the contents dict are set correctly.
        :return:
        """
        assert len(self._fields) > 0, "No fields where set!"
        fieldsSet: List[bool] = [field.isComplete() for field in self._fields]
        return all(fieldsSet)