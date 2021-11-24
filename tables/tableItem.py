"""
DomeExcelConverter
Copyright (C) 2021 Josef Brandt, University of Gothenburg <josef.brandt@gu.se>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program, see COPYING.
If not, see <https://www.gnu.org/licenses/>.
"""


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
