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
        self._alabo: Field = Field("Reporting Laboratory")
        self._metpt: Field = Field("Method of Pretreatment")
        self._metps: Field = Field("Method of Purification/Separation")
        self._metoa: Field = Field("Method of Analysis")
        self._ltref: Field = Field("Litter Reference List")
        self._refsk: Field = Field("Reference Source", mandatory=False)

        self._ltref.content = DomeCode("RECO-LT", "LTREF")  # Quote Anna Osypchuk: "If you are using litter codes LTxxx from CodeType ‘PARAM’, the LTREF code should be ‘RECO-LT’." We are using LTXXX params for describing shape, so we use that here.

        self._fields = [self._alabo, self._refsk, self._metpt, self._metps, self._metoa, self._ltref]

    def getCorrectlySetCodes(self) -> Dict[str, Union[str, float, int]]:
        assert self.correctlySet()
        retDict: Dict[str, Union[str, float, int]] = {"ALABO": self._alabo.content.code,
                                                      "METPT": self._metpt.content.code,
                                                      "METPS": self._metps.content.code,
                                                      "METOA": self._metoa.content.code,
                                                      "LTREF": self._ltref.content.code}
        if self._refsk.content is not None:
            retDict["REFSK"] = self._refsk.content.code
        return retDict

    def setLab(self, code: Union[None, DomeCode]) -> None:
        self._alabo.content = code

    def setLitterRefList(self, code: Union[None, DomeCode]) -> None:
        self._ltref.content = code

    def setRefSource(self, code: Union[None, DomeCode]) -> None:
        self._refsk.content = code

    def setMethPretreat(self, code: Union[None, DomeCode]) -> None:
        self._metpt.content = code

    def setMethodPurification(self, code: Union[None, DomeCode]) -> None:
        self._metps.content = code

    def setMethodAnalysis(self, code: Union[None, DomeCode]) -> None:
        self._metoa.content = code
