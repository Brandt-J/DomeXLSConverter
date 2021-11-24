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


class AnalysisTable(TableItem):
    """
    Table for storing information about the analysis.
    ALABO	Analytical laboratory  -> Not listed here, it's the same as ReportingLab (RLABO) from ID Page
    REFSK	Reference source or key
    METFP	Method of chemical fixation/preservation  -> Not relevant for plastic litter
    METPT	Method of pretreatment
    METCX	Method of chemical extraction  -> Not relevant for plastic litter
    METPS	Method of purification/separation
    METOA	Method of analysis
    """
    def __init__(self):
        super(AnalysisTable, self).__init__("Analysis")
        self._metpt: Field = Field("Method of Pretreatment")
        self._metps: Field = Field("Method of Purification/Seperation")
        self._metoa: Field = Field("Method of Analysis")
        self._refsk: Field = Field("Reference Source", mandatory=False)

        self._fields = [self._refsk, self._metpt, self._metps, self._metoa]

    def setRefSource(self, code: Union[None, DomeCode]) -> None:
        self._refsk.content = code

    def setMethPretreat(self, code: Union[None, DomeCode]) -> None:
        self._metpt.content = code

    def setMethodPurification(self, code: Union[None, DomeCode]) -> None:
        self._metps.content = code

    def setMethodAnalysis(self, code: Union[None, DomeCode]) -> None:
        self._metoa.content = code
