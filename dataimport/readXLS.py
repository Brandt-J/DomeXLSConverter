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


from typing import *

import numpy as np
import pandas as pd


class XLSReader:
    """
    Class for reading excel files and associating excel contents to the database structures.
    """
    def __init__(self):
        self._dataframes: Union[dict[str, pd.DataFrame], None] = None  # Dict with keys: Sheet names, values: data frames
        self._activeSheet: str = ""  # Name of the sheet to use for reading in particle data

    def readXlsFile(self, fname: str) -> None:
        """
        Reads the indicated file.
        :param fname: absolute path to xls file
        :return:
        """
        self._dataframes = pd.read_excel(fname, sheet_name=None)

    def setActiveSheet(self, sheetName: str) -> None:
        """
        Sets which sheet will be used for reading particle data.
        :param sheetName:
        :return:
        """
        assert sheetName in self._dataframes.keys(), f"Sheet {sheetName} not existent in available sheets: {self._dataframes.keys()}"
        self._activeSheet = sheetName

    def getSheetNames(self) -> List[str]:
        """
        Returns the sheet names of the currently loaded excel sheet.
        :return:
        """
        return list(self._dataframes.keys())

    def getColumnsOfActiveSheet(self) -> List[str]:
        """
        Returns the column names of the indicated sheet.
        :return: list of column names
        """
        assert self._activeSheet != "", "Active sheet not yet set!"
        return list(self._dataframes[self._activeSheet].columns)

    def getUniqueColumnContentsAsString(self, colName: str) -> Set[str]:
        """
        Returns a list of (string) entries of the indicated column (of the active sheet).
        Empty entries in the dataframe are "nan", these are included as "Empty".
        Other numberic entries are skipped.
        :return:
        """
        assert self._activeSheet != "", "Active sheet not yet set!"
        uniqueEntries: List[str] = []
        for entry in self._dataframes[self._activeSheet][colName]:
            if type(entry) == float:
                if np.isnan(np.float(entry)):
                    uniqueEntries.append("Empty")
            elif type(entry) == str:
                uniqueEntries.append(entry)

        return set(uniqueEntries)

    def getSheet(self, sheetName: str) -> pd.DataFrame:
        """
        Returns the dataframe of the given sheet name.
        :param sheetName: Name of the datasheet
        :return: pd.DataFrame
        """
        assert sheetName in self._dataframes.keys(), f"Sheet {sheetName} does not exist in opened file."
        return self._dataframes[sheetName]

    def getActiveSheet(self) -> pd.DataFrame:
        assert self._activeSheet in self._dataframes.keys()
        return self._dataframes[self._activeSheet]
