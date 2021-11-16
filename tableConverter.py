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


from tables.table_2_location import LocationTable
from tables.table_1_id import IdentificationTable
from tables.table_3_time import TimeTable
from dataimport.readXLS import XLSReader


class TableConverter:
    """
    Class for a collection of tables needed to write the new excel file format.
    """
    def __init__(self):
        self._xlsReader: XLSReader = XLSReader()
        self._idTable: IdentificationTable = IdentificationTable()
        self._locationTable: LocationTable = LocationTable()
        self._timeTable: TimeTable = TimeTable()

    def getXLSReader(self) -> XLSReader:
        return self._xlsReader

    def getIDTable(self) -> IdentificationTable:
        return self._idTable

    def getLocationTable(self) -> LocationTable:
        return self._locationTable

    def getTimeTable(self) -> TimeTable:
        return self._timeTable
