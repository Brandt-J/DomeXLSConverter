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


class TimeTable(TableItem):
    """
    Table for storing information about sampling time.
    SDATE	Sampling date
    EDATE	Sampling end date
    STIME	Sampling time/start (UTC)
    ATIME	Actual time of sampling (UTC)
    ETIME	Sampling end time (UTC)
    """
    def __init__(self):
        super(TimeTable, self).__init__("Time")
        self._sdate: Field = Field("Sampling Date")
        self._edate: Field = Field("Sampling End Date", mandatory=False)
        self._stime: Field = Field("Sampling Time/Start", mandatory=False)
        self._atime: Field = Field("Actual Time of Sampling", mandatory=False)
        self._etime: Field = Field("Sampling End Time", mandatory=False)

        self._fields = [self._sdate, self._edate, self._stime, self._atime, self._etime]

    def getCorrectlySetCodes(self) -> Dict[str, Union[str, float, int]]:
        assert self.correctlySet()
        retDict: Dict[str, Union[str, float, int]] = {"SDATE": self._sdate.content.code}
        optFields: Dict[str, Field] = {"EDATE": self._edate,
                                       "STIME": self._stime,
                                       "ATIME": self._atime,
                                       "ETIME": self._etime}
        for colName, field in optFields.items():
            if field.content is not None:
                retDict[colName] = field.content.code
        return retDict

    def setSamplingDate(self, sampleCode: Union[None, 'DomeCode']) -> None:
        self._sdate.content = sampleCode

    def setSamplingEndDate(self, sampleCode: Union[None, 'DomeCode']) -> None:
        self._edate.content = sampleCode

    def setSamplingTime(self, sampleCode: Union[None, 'DomeCode']) -> None:
        self._stime.content = sampleCode

    def setActualTime(self, sampleCode: Union[None, 'DomeCode']) -> None:
        self._atime.content = sampleCode

    def setEndTime(self, sampleCode: Union[None, 'DomeCode']) -> None:
        self._etime.content = sampleCode
