from tables.table_2_location import LocationTable
from tables.table_1_id import IdentificationTable
from dataimport.readXLS import XLSReader


class TableConverter:
    """
    Class for a collection of tables needed to write the new excel file format.
    """
    def __init__(self):
        self._xlsReader: XLSReader = XLSReader()
        self._idTable: IdentificationTable = IdentificationTable()
        self._locationTable: LocationTable = LocationTable()

    def getXLSReader(self) -> XLSReader:
        return self._xlsReader

    def getIDTable(self) -> IdentificationTable:
        return self._idTable

    def getLocationTable(self) -> LocationTable:
        return self._locationTable
