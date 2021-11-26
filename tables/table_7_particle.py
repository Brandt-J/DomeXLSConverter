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

from typing import Union, Dict, List
from dataclasses import dataclass, field

from dataimport.domeCodes import DomeCode, getLitterSizes
from tables.tableItem import TableItem, Field


class ParticleColumnMapping(TableItem):
    """
    Class for storing which particle relevant fields are read from which column in the imported excel sheet.
    The class reuses the table Item base class and stores assigned sheet names in DomeCodes, just to reuse
    existing code structure.
    """
    def __init__(self):
        super(ParticleColumnMapping, self).__init__("Particle Column Assignments")
        self._sizeColumn: Field = Field("Litter size column")
        self._polymTypeColumn: Field = Field("Polymer type column", mandatory=False)
        self._shapeColumn: Field = Field("Polymer shape column", mandatory=False)
        self._colorColumn: Field = Field("Polymer color column", mandatory=False)
        self._codeMappings: CodeMappings = CodeMappings()

        self._fields = [self._sizeColumn, self._polymTypeColumn, self._shapeColumn, self._colorColumn]

    def setTypeMapping(self, mapping: Dict[str, 'DomeCode']) -> None:
        for val in mapping.values():
            assert type(val) == DomeCode
        self._codeMappings.polymType2Code = mapping

    def setColorMapping(self, mapping: Dict[str, 'DomeCode']) -> None:
        for val in mapping.values():
            assert type(val) == DomeCode
        self._codeMappings.color2Code = mapping

    def setShapeMapping(self, mapping: Dict[str, 'DomeCode']) -> None:
        for val in mapping.values():
            assert type(val) == DomeCode
        self._codeMappings.shape2Code = mapping

    def getTypeMapping(self) -> Dict[str, 'DomeCode']:
        return self._codeMappings.polymType2Code

    def getColorMapping(self) -> Dict[str, 'DomeCode']:
        return self._codeMappings.color2Code

    def getShapeMapping(self) -> Dict[str, 'DomeCode']:
        return self._codeMappings.shape2Code

    def setSizeColumn(self, columnCode: Union[DomeCode, None]) -> None:
        self._sizeColumn.content = columnCode

    def setPolymTypeColumn(self, columnCode: Union[DomeCode, None]) -> None:
        self._polymTypeColumn.content = columnCode

    def setShapeColumn(self, columnCode: Union[DomeCode, None]) -> None:
        self._shapeColumn.content = columnCode

    def setColorColumn(self, columnCode: Union[DomeCode, None]) -> None:
        self._colorColumn.content = columnCode

    def getSizeColumn(self) -> Union[DomeCode, None]:
        return self._sizeColumn.content

    def getPolymTypeColumn(self) -> Union[DomeCode, None]:
        return self._polymTypeColumn.content

    def getColorColumn(self) -> Union[DomeCode, None]:
        return self._colorColumn.content

    def getShapeColumn(self) -> Union[DomeCode, None]:
        return self._shapeColumn.content

    def correctlySet(self) -> bool:
        fieldsCorrect: bool = super(ParticleColumnMapping, self).correctlySet()
        maps: CodeMappings = self._codeMappings
        mappingsCorrect: bool = True
        if self._colorColumn.content is not None:
            if len(maps.color2Code) == 0:
                mappingsCorrect = False
        if self._shapeColumn.content is not None:
            if len(maps.shape2Code) == 0:
                mappingsCorrect = False
        if self._polymTypeColumn.content is not None:
            if len(maps.polymType2Code) == 0:
                mappingsCorrect = False

        return fieldsCorrect and mappingsCorrect


@dataclass
class CodeMappings:
    """
    Struct for storing mapping of strings in the excel file to corresponding DOME codes.
    """
    polymType2Code: Dict[str, DomeCode] = field(default_factory=dict)
    shape2Code: Dict[str, DomeCode] = field(default_factory=dict)
    color2Code: Dict[str, DomeCode] = field(default_factory=dict)


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
        self._value: Field = Field("Value")
        self._typpl: Field = Field("Polmymer Type", mandatory=False)
        self._ltprp: Field = Field("Litter Properties", mandatory=False)

        # Set some defaults
        self._param.content = DomeCode("LTT-249", "Litter - <5mm plastic particle")
        self._munit.content = DomeCode("items", "Measurement unit")
        self._value.content = DomeCode("1", "Value")

        self._litterSizes: List['DomeCode'] = getLitterSizes()

        self._fields = [self._param, self._size, self._munit, self._value, self._typpl, self._ltprp]

    def getCorrectlySetCodes(self) -> Dict[str, Union[str, float, int]]:
        assert self.correctlySet()
        retDict: Dict[str, Union[str, float, int]] = {"PARAM": self._param.content.code,
                                                      "LTSZC": self._size.content.code,
                                                      "MUNIT": self._munit.content.code,
                                                      "VALUE": self._value.content.code}
        optFields: Dict[str, Field] = {"TYPPL": self._typpl,
                                       "LTPRP": self._ltprp}
        for colName, field in optFields.items():
            if field.content is not None:
                retDict[colName] = field.content.code
        return retDict

    def getPossibleColumns(self) -> List[str]:
        """
        Returns a list of column names that are possible to be set. I.e., all mandatory and optional ones.
        :return:
        """
        return ["PARAM", "LTSZC", "MUNIT", "VALUE", "TYPPL", "LTPRP"]

    def setParam(self, paramCode: Union[DomeCode, None]) -> None:
        self._param.content = paramCode

    def setSize(self, size: float) -> None:
        self._size.content = self._getSizeCodeOfSize(size)

    def setPolymType(self, code: Union[DomeCode, None]) -> None:
        self._typpl.content = code

    def setColor(self, code: Union[DomeCode, None]) -> None:
        self._ltprp.content = code

    def setShape(self, code: Union[DomeCode, None]) -> None:
        self._param.content = code

    def _getSizeCodeOfSize(self, size: float) -> DomeCode:
        code: Union[DomeCode, None] = None
        for sizeCode in self._litterSizes:
            if sizeCode.descr.find("<=100 um") > 0:
                if size <= 100:
                    code = sizeCode
                    break
            else:
                factor: float = 1.0  # i.e., startswith "micron"
                if sizeCode.descr.startswith("mm"):
                    factor = 1000
                elif sizeCode.descr.startswith("cm"):
                    factor = 10000

                limitString: str = sizeCode.descr.split(" ")[1]
                low, high = float(limitString.split("-")[0])*factor, float(limitString.split("-")[1])*factor
                if low <= round(size) <= high:
                    code = sizeCode
                    break
        assert code is not None, f"Code for size {size} could not be found."
        return code
