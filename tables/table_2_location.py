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


from typing import Union, Dict

from dataimport.domeCodes import DomeCode
from tables.tableItem import TableItem, Field


class LocationTable(TableItem):
    """
    Table for storing information about sampling location.
    LATIT	Latitude (degrees/minutes/decimal minutes or as decimal degrees). Report as WGS84
    LONGI	Longitude (degrees/minutes/decimal minutes or as decimal degrees). Report as WGS84.
    POSYS	Position system
    STATN	Station name
    WADEP	Water depth (sounding in meters)
    MNDEP	Minimum depth of sample (metre)
    MXDEP	Maximum depth of sample (metre)
    SUBST	Bottom substrate type
    PRSUB	Percent of bottom covered with the particular bottom substrate type
    """
    def __init__(self):
        super(LocationTable, self).__init__("Location")
        self._long: Field = Field("Longitude")
        self._lat: Field = Field("Latitude")
        self._station: Field = Field("Station Name")
        self._posys: Field = Field("PositioningSystem", mandatory=False)
        self._waterDepth: Field = Field("Water Depth", mandatory=False)
        self._minDepth: Field = Field("Min Depth", mandatory=False)
        self._maxDepth: Field = Field("Max Depth", mandatory=False)
        self._subst: Field = Field("Substrate Type", mandatory=False)
        self._prSub: Field = Field("Percent Covered", mandatory=False)

        self._fields = [self._long, self._lat, self._posys, self._station, self._waterDepth,
                        self._minDepth, self._maxDepth, self._subst, self._prSub]

    def getCorrectlySetCodes(self) -> Dict[str, Union[str, float, int]]:
        assert self.correctlySet()
        retDict: Dict[str, Union[str, float, int]] = {"LATIT": self._lat.content.code,
                                                      "LONGI": self._long.content.code,
                                                      "STATN": self._station.content.code}
        optFields: Dict[str, Field] = {"POSYS": self._posys,
                                       "WADEP": self._waterDepth,
                                       "MNDEP": self._minDepth,
                                       "MXDEP": self._maxDepth,
                                       "SUBST": self._subst,
                                       "PRSUB": self._prSub}
        for colName, field in optFields.items():
            if field.content is not None:
                retDict[colName] = field.content.code
        return retDict

    def setLongitude(self, longitude: float) -> None:
        self._long.content = DomeCode(str(longitude), "Longitude")

    def setLatitude(self, latitude: float) -> None:
        self._lat.content = DomeCode(str(latitude), "Latitude")

    def setPosSystem(self, posSysCode: Union[None, 'DomeCode']) -> None:
        self._posys.content = posSysCode

    def setStationName(self, stationName: Union[None, 'DomeCode']) -> None:
        self._station.content = stationName

    def setWaterDepth(self, depth: Union[None, 'DomeCode']) -> None:
        self._waterDepth.content = depth

    def setMinDepth(self, minDepth: Union[None, 'DomeCode']) -> None:
        self._minDepth.content = minDepth

    def setMaxDepth(self, maxDepth: Union[None, 'DomeCode']) -> None:
        self._maxDepth.content = maxDepth

    def setSubstrateType(self, substType: Union[None, 'DomeCode']) -> None:
        self._subst.content = substType

    def setPercentCovered(self, prCov: Union[None, 'DomeCode']) -> None:
        self._prSub.content = prCov
