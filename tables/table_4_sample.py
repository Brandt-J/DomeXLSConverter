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


from typing import Union, Dict

from dataimport.domeCodes import DomeCode
from tables.tableItem import TableItem, Field


class SampleTable(TableItem):
    """
    Table for storing information about sample.
    DTYPE	Data type
    SMPNO	Sample number / Sample identification for haul or group of individuals/cores/bottles collected at that time/place
    NOAGG	Number of aggregated samples (hauls, sediment cores or grabs) taken to comprise sample
    FINFL	Factors potentially influencing guideline compliance and interpretation of data
    SUBNO	Sub-sample number
    MATRX	Matrix
    """
    def __init__(self):
        super(SampleTable, self).__init__("Sample")
        self._dtype: Field = Field("Data Type")
        self._smpno: Field = Field("Sample Number")
        self._matrx: Field = Field("Matrix")
        self._sarea: Field = Field("Sample Area (cm^2)")
        self._noagg: Field = Field("Number of Aggregated Samples", mandatory=False)
        self._finfl: Field = Field("Influencing Factors", mandatory=False)
        self._subno: Field = Field("Subsample Number", mandatory=False)

        self._fields = [self._dtype, self._smpno, self._matrx, self._noagg, self._finfl, self._subno, self._sarea]

    def getCorrectlySetCodes(self) -> Dict[str, Union[str, float, int]]:
        assert self.correctlySet()
        retDict: Dict[str, Union[str, float, int]] = {"DTYPE": self._dtype.content.code,
                                                      "SMPNO": self._smpno.content.code,
                                                      "MATRX": self._matrx.content.code,
                                                      "SAREA": self._sarea.content.code}
        optFields: Dict[str, Field] = {"NOAGG": self._noagg,
                                       "FINFL": self._finfl,
                                       "SUBNO": self._subno}
        for colName, field in optFields.items():
            if field.content is not None:
                retDict[colName] = field.content.code
        return retDict

    def setDType(self, code: Union[None, DomeCode]) -> None:
        self._dtype.content = code

    def setSampleNumber(self, code: Union[None, DomeCode]) -> None:
        self._smpno.content = code

    def setMatrix(self, code: Union[None, DomeCode]) -> None:
        self._matrx.content = code

    def setNumberAggregations(self, code: Union[None, DomeCode]) -> None:
        self._noagg.content = code

    def setInfluencingFactors(self, code: Union[None, DomeCode]) -> None:
        self._finfl.content = code

    def setSubsampleNumber(self, code: Union[None, DomeCode]) -> None:
        self._subno.content = code

    def setSampleArea(self, area_cm2: int) -> None:
        self._sarea.content = DomeCode(str(area_cm2), "SAREA")
