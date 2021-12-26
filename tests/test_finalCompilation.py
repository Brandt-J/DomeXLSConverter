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


import os
import tempfile
import pandas as pd
from PyQt6 import QtCore
from typing import TYPE_CHECKING

from dataimport.domeCodes import DomeCode
from gui.wizard import ParticleUploadWizard
from dataimport.readXLS import XLSReader

if TYPE_CHECKING:
    from gui.pages.page_0_intro import IntroPage
    from tables.table_1_id import IdentificationTable
    from tables.table_2_location import LocationTable
    from tables.table_3_time import TimeTable
    from tables.table_4_sample import SampleTable
    from tables.table_5_analysis import AnalysisTable
    from tables.table_6_monitoring import MonitoringTable
    from tables.table_7_particle import ParticleTable, ParticleColumnMapping


def test_complete_compilation(tmpdir, qtbot):
    if os.getcwd().endswith("tests"):
        os.chdir(os.path.dirname(os.getcwd()))  # Otherwise path to testdata doesn't work

    wizard: ParticleUploadWizard = ParticleUploadWizard()
    qtbot.addWidget(wizard)
    wizard.show()
    qtbot.waitForWindowShown(wizard)

    # Load file:
    introPage: IntroPage = wizard._introPage
    introPage._getXLSFileName = lambda: r"data\exampledata.xlsx"  # now take a valid file
    assert os.path.exists(introPage._getXLSFileName())
    introPage._btnLoadXLS.pressed.disconnect()
    introPage._btnLoadXLS.pressed.connect(lambda: introPage._loadXLSFile(preferredSheetName="p3 unprocessed"))
    qtbot.mousePress(introPage._btnLoadXLS, QtCore.Qt.MouseButton.LeftButton)
    assert introPage._xlsLoaded
    assert introPage._xlsReader._activeSheet == "p3 unprocessed"

    idTable: IdentificationTable = wizard._idPage._tableItem
    idTable.setReportingLab(DomeCode("TestLab", "TestCode"))
    idTable.setYear(DomeCode("2021", "TestCode"))
    idTable.setCruise(DomeCode("Summer Cruise", "TestCode"))
    idTable.setStation(DomeCode("TestStation", "TestCode"))
    idTable.setShipCode(DomeCode("NCC1701", "TestCode"))
    assert idTable.correctlySet()

    locTable: LocationTable = wizard._locPage._tableItem
    locTable.setLongitude(50)
    locTable.setLatitude(30)
    locTable.setStationName(DomeCode("TestStationName", "TestCode"))
    assert locTable.correctlySet()

    timeTable: TimeTable = wizard._timePage._tableItem
    timeTable.setSamplingDate(DomeCode("20210810", "TestCode"))
    assert timeTable.correctlySet()

    sampleTable: SampleTable = wizard._samplePage._tableItem
    sampleTable.setDType(DomeCode("Test-DTYPE", "TestCode"))
    sampleTable.setMatrix(DomeCode("Sediment", "TestCode"))
    sampleTable.setSampleNumber(DomeCode("2", "TestCode"))
    assert sampleTable.correctlySet()

    analysisTable: AnalysisTable = wizard._analysisPage._tableItem
    analysisTable.setLab(DomeCode("TestLab", "TestCode"))
    analysisTable.setLitterRefList(DomeCode("LitterList0815", "TestCode"))
    analysisTable.setMethodAnalysis(DomeCode("µFTIR", "TestCode"))
    analysisTable.setMethPretreat(DomeCode("Digestion", "TestCode"))
    analysisTable.setMethodPurification(DomeCode("Filtration", "TestCode"))
    assert analysisTable.correctlySet()

    monitoringTable: 'MonitoringTable' = wizard._monitoringPage._tableItem
    monitoringTable.setMonitoringPurpose(DomeCode("TestPurpose", "TestCode"))
    monitoringTable.setProgramme(DomeCode("TestProgram", "TestCode"))
    assert monitoringTable.correctlySet()

    partColumns: ParticleColumnMapping = wizard._particlesPage._tableItem
    partColumns.setSizeColumn(DomeCode("MajorEllipse µ", "TestCode"))
    partColumns.setColorColumn(DomeCode("Colour", "TestCode"))
    partColumns.setShapeColumn(DomeCode("Shape 2D", "TestCode"))
    partColumns.setPolymTypeColumn(DomeCode("Chemical ID", "TestCode"))

    partColumns.setTypeMapping({"Empty": DomeCode("Inconclusive", "TestCode")})
    partColumns.setColorMapping({"White": DomeCode("White", "TestCode"),
                                 "Black": DomeCode("Black", "TestCode"),
                                 "Green": DomeCode("Green", "TestCode"),
                                 "Blue": DomeCode("Blue", "TestCode"),
                                 "Brown": DomeCode("Brown", "TestCode"),
                                 "Yellow": DomeCode("Yellow", "TestCode"),
                                 "Grey": DomeCode("Grey", "TestCode")})
    partColumns.setShapeMapping({"Triangle": DomeCode("Triangle", "TestCode"),
                                 "Oval": DomeCode("Oval", "TestCode"),
                                 "Rectangle": DomeCode("Rectangle", "TestCode"),
                                 "Square": DomeCode("Square", "TestCode"),
                                 "Fiber": DomeCode("Fiber", "TestCode"),
                                 "Irregular": DomeCode("Irregular", "TestCode"),
                                 "Circular": DomeCode("Circular", "TestCode")})

    assert partColumns.correctlySet()
    with tempfile.TemporaryDirectory() as tmpDirName:
        resultFileName: str = os.path.join(tmpDirName, "testExport.csv")
        wizard._particlesPage._getSaveFileName = lambda: resultFileName
        wizard._particlesPage.validatePage()  # this is called by pressing the "Finish" Button

        assert os.path.exists(resultFileName)

        savedDF: pd.DataFrame = pd.read_csv(resultFileName)
        assert savedDF.shape[0] == 133
        assert savedDF.columns[-1] == "MPROG"
