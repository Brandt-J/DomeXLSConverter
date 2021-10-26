from tableItems import IdentificationTable
from dataimport.readXLS import XLSReader


class TableConverter:
    """
    Class for a collection of tables needed to write the new excel file format.
    """
    def __init__(self):
        self._xlsReader: XLSReader = XLSReader()
        self._idTable: IdentificationTable = IdentificationTable()

    def getXLSReader(self) -> XLSReader:
        return self._xlsReader

    def getIDTable(self) -> IdentificationTable:
        return self._idTable
