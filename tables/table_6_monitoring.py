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


class MonitoringTable(TableItem):
    """
    PURPM	Purpose of Monitoring
    MPROG	Monitoring Programme
    """
    def __init__(self):
        super(MonitoringTable, self).__init__("Monitoring Purpose")
        self._purpm: Field = Field("Purpose of Monitoring")
        self._mprog: Field = Field("Monitoring Programme")

        self._fields = [self._purpm, self._mprog]

    def getCorrectlySetCodes(self) -> Dict[str, Union[str, float, int]]:
        assert self.correctlySet()
        retDict: Dict[str, Union[str, float, int]] = {"PURPM": self._purpm.content.code,
                                                      "MPROG": self._mprog.content.code}
        return retDict

    def setMonitoringPurpose(self, code: Union[DomeCode, None]) -> None:
        self._purpm.content = code

    def setProgramme(self, code: Union[DomeCode, None]) -> None:
        self._mprog.content = code
