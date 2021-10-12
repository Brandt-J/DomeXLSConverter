from typing import *

from tableItems import InstitutionTable
from dataimport.readXLS import XLSReader


class TableCollection:
    """
        Class for a collection of tables, representing a certain database structure.
        """
    def __init__(self):
        self._xlsReader: XLSReader = XLSReader()

        self._institutionTable: InstitutionTable = InstitutionTable()

    def getInstitutionTable(self) -> InstitutionTable:
        return self._institutionTable
