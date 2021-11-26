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
from typing import List, TYPE_CHECKING, Optional, Dict, Tuple
import pandas as pd
import numpy as np

from tables.table_2_location import LocationTable
from tables.table_1_id import IdentificationTable
from tables.table_3_time import TimeTable
from tables.table_4_sample import SampleTable
from tables.table_5_analysis import AnalysisTable
from tables.table_6_monitoring import MonitoringTable
from tables.table_7_particle import ParticleTable, ParticleColumnMapping
from dataimport.readXLS import XLSReader

if TYPE_CHECKING:
    from dataimport.domeCodes import DomeCode


class TableConverter:
    """
    Class for a collection of tables needed to write the new excel file format.
    """
    def __init__(self):
        self._xlsReader: XLSReader = XLSReader()
        self._idTable: IdentificationTable = IdentificationTable()
        self._locationTable: LocationTable = LocationTable()
        self._timeTable: TimeTable = TimeTable()
        self._sampleTable: SampleTable = SampleTable()
        self._monitoringTable: MonitoringTable = MonitoringTable()
        self._analysisTable: AnalysisTable = AnalysisTable()
        self._particleColMapping: ParticleColumnMapping = ParticleColumnMapping()
        self._particleTables: List[ParticleTable] = []

    def _allTablesComplete(self) -> Tuple[bool, str]:
        """
        Checks, if all tables were set correctly.
        :return:
        """
        ok, msg = True, ""

        for table in [self._idTable, self._locationTable, self._timeTable, self._sampleTable, self._analysisTable,
                                                       self._monitoringTable, self._particleColMapping]:
            if not table.correctlySet():
                msg += f"Table {table.name} not correctly set.\n"
                ok = False

        if msg:
            msg += ""

        return ok, msg

    def createFinalDataFrame(self) -> pd.DataFrame:
        """
        Compiles all data into a dataframe.
        :return:
        """
        dframe: pd.DataFrame = pd.DataFrame()
        ok, errmsg = self._allTablesComplete()
        assert ok, errmsg

        self._createParticleTablesFromXLS()

        assert len(self._particleTables) > 0, "No Particles were created."
        assert all([table.correctlySet() for table in self._particleTables]), "Not all of the particle tables are correct."
        numParticles: int = len(self._particleTables)

        # First fill in all the data that is not per-particle
        for table in [self._idTable, self._locationTable, self._timeTable, self._sampleTable, self._analysisTable,
                      self._monitoringTable]:
            for colName, entry in table.getCorrectlySetCodes().items():
                dframe[colName] = [entry]*numParticles

        # Then add in all the per-particle data
        for colName in self._particleTables[0].getPossibleColumns():
            dframe[colName] = ""  # initializes empty columns for these possible entries

        for i, ptable in enumerate(self._particleTables):
            for colName, entry in ptable.getCorrectlySetCodes().items():
                dframe[colName][i] = entry

        return dframe

    def getXLSReader(self) -> XLSReader:
        return self._xlsReader

    def getIDTable(self) -> IdentificationTable:
        return self._idTable

    def getLocationTable(self) -> LocationTable:
        return self._locationTable

    def getTimeTable(self) -> TimeTable:
        return self._timeTable

    def getSampleTable(self) -> SampleTable:
        return self._sampleTable

    def getAnalysisTable(self) -> AnalysisTable:
        return self._analysisTable

    def getMonitoringTable(self) -> MonitoringTable:
        return self._monitoringTable

    def getParticleColumnAssignmentsTable(self) -> ParticleColumnMapping:
        return self._particleColMapping

    def _createParticleTablesFromXLS(self) -> None:
        """
        Uses the information from the particleColumnAssignments and populates the list of particleTables.
        :return:
        """
        self._particleTables = []
        assert self._particleColMapping.getSizeColumn() is not None, "Size Column not yet set!"
        activeDF: pd.DataFrame = self._xlsReader.getActiveSheet()

        sizes: pd.Series = activeDF[self._particleColMapping.getSizeColumn().code]
        types: Optional[pd.Series] = None
        if self._particleColMapping.getPolymTypeColumn():
            types = activeDF[self._particleColMapping.getPolymTypeColumn().code]
            assert len(types) == len(sizes), "Number of entries in Type column does not equal number of entries in Size column"
        colors: Optional[pd.Series] = None
        if self._particleColMapping.getColorColumn():
            colors = activeDF[self._particleColMapping.getColorColumn().code]
            assert len(colors) == len(sizes), "Number of entries in Color column does not equal number of entries in Size column"
        shapes: Optional[pd.Series] = None
        if self._particleColMapping.getShapeColumn():
            shapes = activeDF[self._particleColMapping.getShapeColumn().code]
            assert len(shapes) == len(sizes), "Number of entries in Shape column does not equal number of entries in Size column"

        mapColor: Dict[str, DomeCode] = self._particleColMapping.getColorMapping()
        mapType: Dict[str, DomeCode] = self._particleColMapping.getTypeMapping()
        mapShape: Dict[str, DomeCode] = self._particleColMapping.getShapeMapping()

        numParticles: int = activeDF.shape[0]
        for i in range(numParticles):
            partTable: ParticleTable = ParticleTable()
            partTable.setSize(sizes[i])
            if colors is not None and self._notEmpty(colors[i]):
                partTable.setColor(mapColor[colors[i]])
            if types is not None and self._notEmpty(types[i]):
                partTable.setPolymType(mapType[types[i]])
            if shapes is not None and self._notEmpty(shapes[i]):
                partTable.setShape(mapShape[shapes[i]])

            assert partTable.correctlySet()
            self._particleTables.append(partTable)

    def _notEmpty(self, entry) -> bool:
        notEmpty: bool = True
        if type(entry) == np.float64 or type(entry) == float:
            if np.isnan(entry):
                notEmpty = False
        return notEmpty
