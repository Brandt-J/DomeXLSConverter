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
    assert reader.getColumnsOfSheet("P1 results") == expectedColumns
