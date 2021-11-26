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

from typing import Union

from dataimport.domeCodes import DomeCode
from tables.tableItem import TableItem, Field


class ParticleColumnAssignments(TableItem):
    """
    Class for storing which particle relevant fields are read from which column in the imported excel sheet.
    The class reuses the table Item base class and stores assigned sheet names in DomeCodes, just to reuse
    existing code structure.
    """
    def __init__(self):
        super(ParticleColumnAssignments, self).__init__("Particle Column Assignments")
        self._sizeColumn: Field = Field("Litter size column")
        self._polymTypeColumn: Field = Field("Polymer type column", mandatory=False)
        self._shapeColumn: Field = Field("Polymer shape column", mandatory=False)
        self._colorColumn: Field = Field("Polymer color column", mandatory=False)

        self._fields = [self._sizeColumn, self._polymTypeColumn, self._shapeColumn, self._colorColumn]

    def setSizeColumn(self, columnCode: Union[DomeCode, None]) -> None:
        self._sizeColumn.content = columnCode

    def setPolymTypeColumn(self, columnCode: Union[DomeCode, None]) -> None:
        self._polymTypeColumn.content = columnCode

    def setShapeColumn(self, columnCode: Union[DomeCode, None]) -> None:
        self._shapeColumn.content = columnCode

    def setColorColumn(self, columnCode: Union[DomeCode, None]) -> None:
        self._colorColumn.content = columnCode


class ParticleTable(TableItem):
    """
    Table for storing information about each individual particle.
    LTREF	Litter reference list	https://vocab.ices.dk/?ref=1381  -> dependent on Param?
    PARAM	Parameter	https://vocab.ices.dk/?ref=78  -> shape dependent
    LTSZC	Litter size	https://vocab.ices.dk/?ref=1380
    MUNIT	Measurement unit	https://vocab.ices.dk/?ref=155  -> "items"
    QFLAG	Qualifier flag	https://vocab.ices.dk/?ref=180  -> Not needed.
    VALUE	Value measured  -> "1"  i.e., one item per line
    LTSRC 	Litter source	https://vocab.ices.dk/?ref=1382  -> Usually not known from the particle measurement... But could be implemented.
    TYPPL	Type of polymer	https://vocab.ices.dk/?ref=1385
    LTPRP	Litter properties (including polymer shapes and colours)	https://vocab.ices.dk/?ref=1403
    """
    def __init__(self):
        super(ParticleTable, self).__init__("Particle")
        self._param: Field = Field("Parameter")
        self._size: Field = Field("Litter size")
        self._munit: Field = Field("Measurement unit")
        self._munit.content = DomeCode("items", "Measurement unit")
        self._value: Field = Field("Value")
        self._value.content = DomeCode("1", "Value")
        self._typpl: Field = Field("Polmymer Type")
        self._ltprp: Field = Field("Litter Properties")

        self._fields = [self._param, self._size, self._munit, self._value]
