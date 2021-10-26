from dataclasses import dataclass, field
from typing import *

from dataimport.domeCodes import DomeCode


@dataclass
class Field:
    """
    Class for storing information to each field, especially if it was set (content != None) and if the field is mandatory
    """
    name: str
    content: Optional['DomeCode'] = None
    mandatory: bool = True

    def isComplete(self) -> bool:
        """
        Returns if the field is completed or still needs to be set.
        :return:
        """
        return type(self.content) == DomeCode if self.mandatory else True


@dataclass
class TableItem:
    """
    Container class for storing fields for a specific table.
    """
    name: str
    _fields: List[Field] = field(default_factory=list)

    def correctlySet(self) -> bool:
        """
        Returns, if all values of the contents dict are set correctly.
        :return:
        """
        fieldsSet: List[bool] = [field.isComplete() for field in self._fields]
        return all(fieldsSet)


class IdentificationTable(TableItem):
    """
    Table for storing information about the ID of the entry.
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


