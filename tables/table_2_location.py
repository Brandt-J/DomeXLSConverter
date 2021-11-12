from typing import Union

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

    def setLongitude(self, longitude: float) -> None:
        self._long.content = DomeCode(str(longitude), "Longitude", "No further infos available")

    def setLatitude(self, latitude: float) -> None:
        self._lat.content = DomeCode(str(latitude), "Latitude", "No further infos available")

    def setPosSystem(self, posSysCode: Union[None, 'DomeCode']) -> None:
        self._posys.content = posSysCode

    def setStationName(self, stationName: Union[None, 'DomeCode']) -> None:
        self._station.content = stationName

    def setWaterDepth(self, depth: float) -> None:
        self._waterDepth.content = DomeCode(str(depth), "Water depth", "Sounding in meters")

    def setMinDepth(self, minDepth: float) -> None:
        self._minDepth.content = DomeCode(str(minDepth), "Min Water Depth of Sample", "No furhter infos available")

    def setMaxDepth(self, maxDepth: Union[None, 'DomeCode']) -> None:
        self._maxDepth.content = DomeCode(str(maxDepth), "Max Water Depth of Sample", "No furhter infos available")

    def setSubstrateType(self, substType: Union[None, 'DomeCode']) -> None:
        self._subst.content = substType

    def setPercentCovered(self, prCov: int) -> None:
        self._prSub.content = DomeCode(str(prCov), "Percent covered", "Percent of bottom covered with the particular bottom substrate type")