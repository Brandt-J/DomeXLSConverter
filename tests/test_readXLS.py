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


from typing import List
import pandas as pd
import pytest
import os

from dataimport.readXLS import XLSReader


def test_read_xls_file():
    if os.getcwd().endswith("tests"):
        os.chdir(os.path.dirname(os.getcwd()))

    testFilePath: str = r"data\exampledata.xlsx"
    assert os.path.exists(testFilePath)
    reader: XLSReader = XLSReader()
    assert reader._dataframes is None
    reader.readXlsFile(testFilePath)
    assert type(reader._dataframes) == dict

    sheetNames: List[str] = reader.getSheetNames()
    expectedSheetsNames: List[str] = ["P1 info", "P1 results", "p3 unprocessed", "G1 tims doc", "G1 info max"]
    assert sorted(sheetNames) == sorted(expectedSheetsNames)

    with pytest.raises(AssertionError):
        particlesSheet: pd.DataFrame = reader.getSheet("NonExistentSheet")

    expectedColumns: List[str] = ["Sample_SizeFraction_Tray_Well", "Zoom", "Area µ", "Perimeter µ", "MajorEllipse µ",
                                  "MinorEllipse µ", "Feret µ", "MinFeret µ","Comments", "EllipseAngle", "FeretX",
                                  "FeretY", "FeretAngle"]
    reader.setActiveSheet("P1 results")
    assert reader.getColumnsOfActiveSheet() == expectedColumns
