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

from tables.tableItem import TableItem, Field


class IdentificationTable(TableItem):
    """
    Table for storing information about the ID of the entry.
    RLABO	Reporting laboratory
    MYEAR	Monitoring Year
    SHIPC	Ship or platform code
    CRUIS	Cruise identifier (series of sampling occasions)
    STNNO	Station identification /Sampling event ID
    """
    def __init__(self):
        super(IdentificationTable, self).__init__("ID")
        self._lab: Field = Field("Reporting Laboratory")
        self._year: Field = Field("Monitoring Year", mandatory=False)
        self._cruise: Field = Field("Cruise")
        self._ship: Field = Field("Ship")
        self._station: Field = Field("Station ")

        self._fields = [self._lab, self._year, self._cruise, self._ship, self._station]

    def setReportingLab(self, labCode: Union['DomeCode', None]) -> None:
        self._lab.content = labCode

    def setShipCode(self, shipCode: Union['DomeCode', None]) -> None:
        self._ship.content = shipCode

    def setCruise(self, cruiseCode: Union['DomeCode', None]) -> None:
        self._cruise.content = cruiseCode

    def setStation(self, stationCode: Union['DomeCode', None]) -> None:
        self._station.content = stationCode

    def setYear(self, yearCode: Union['DomeCode', None]) -> None:
        self._year.content = yearCode