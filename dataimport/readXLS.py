from typing import *
import pandas as pd


class XLSReader:
    """
    Class for reading excel files and associating excel contents to the database structures.
    """
    def __init__(self):
        self._dataframes: Union[dict[str, pd.DataFrame], None] = None  # Dict with keys: Sheet names, values: data frames

    def readXlsFile(self, fname: str) -> None:
        """
        Reads the indicated file.
        :param fname: absolute path to xls file
        :return:
        """
        self._dataframes = pd.read_excel(fname, sheet_name=None)

    def getSheetNames(self) -> List[str]:
        """
        Returns the sheet names of the currently loaded excel sheet.
        :return:
        """
        return list(self._dataframes.keys())

    def getColumnsOfSheet(self, sheetName) -> List[str]:
        """
        Returns the column names of the indicated sheet.
        :param sheetName: name of the sheet
        :return: list of column names
        """
        assert sheetName in self._dataframes.keys(), f"Sheet {sheetName} does not exist in opened file."
        return list(self._dataframes[sheetName].columns)

    def getSheet(self, sheetName: str) -> pd.DataFrame:
        """
        Returns the dataframe of the given sheet name.
        :param sheetName: Name of the datasheet
        :return: pd.DataFrame
        """
        assert sheetName in self._dataframes.keys(), f"Sheet {sheetName} does not exist in opened file."
        return self._dataframes[sheetName]
