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

import pandas as pd
from typing import *
from dataclasses import dataclass
import numpy as np
import os
import csv

if os.getcwd().endswith("tests"):
    os.chdir(os.path.dirname(os.getcwd()))  # switch to parent directory to be able to find code files
codeFolder: str = os.path.join(os.getcwd(), "data", "DOME codes")


@dataclass
class DomeCode:
    """
    Dataclass for storing the info fields from the Dome Vocabulary.
    """
    code: str
    descr: str  # Description
    long_descr: str = "No further infos available"  # Long Description


def getLitterSource() -> List[DomeCode]:
    dframe: pd.DataFrame = pd.read_excel(os.path.join(codeFolder, "1382_LTSRC.xlsx"))
    sources: List[DomeCode] = []
    codes, desc, longdesc = dframe["Code"], dframe["Description"], dframe["LongDescription"]
    for i in range(len(codes)):
        name, descr, longdescr = codes[i], desc[i], longdesc[i]
        if type(longdescr) == float:
            assert np.isnan(longdescr)
            longdescr = "No further details available."

        assert all([type(i) == str for i in [name, descr, longdescr]])
        sources.append(DomeCode(name, descr, longdescr))

    return sources


def getPositioningSystems() -> List[DomeCode]:
    return _createCodesFromCSV("Posys.csv")


def getLabCode() -> List[DomeCode]:
    return _createCodesFromCSV("LabCode.csv")


def getShipCode() -> List[DomeCode]:
    return _createCodesFromCSV("ShipCode.csv")


def getSubstrateTypes() -> List[DomeCode]:
    return _createCodesFromCSV("SubstrateTypes.csv")


def getSampleDTypes() -> List[DomeCode]:
    return _createCodesFromCSV("SampleDType.csv")


def getInfluencingFactors() -> List[DomeCode]:
    return _createCodesFromCSV("InflFactors.csv")


def getMatrices() -> List[DomeCode]:
    return _createCodesFromCSV("Matrix.csv")


def getRefSources() -> List[DomeCode]:
    return _createCodesFromCSV("RefSources.csv")


def getPretreatments() -> List[DomeCode]:
    return _createCodesFromCSV("MethPretreat.csv")


def getPurifications() -> List[DomeCode]:
    return _createCodesFromCSV("MethPurSep.csv")


def getAnalyses() -> List[DomeCode]:
    return _createCodesFromCSV("MethAnalysis.csv")


def getLitterProperties() -> List[DomeCode]:
    return _createCodesFromCSV("LitterProp.csv")


def getPolymerTypes() -> List[DomeCode]:
    return _createCodesFromCSV("PolymType.csv")


def getShapeParams() -> List[DomeCode]:
    return _createCodesFromCSV("ShapeParam.csv")


def getLitterSizes() -> List[DomeCode]:
    return _createCodesFromCSV("LitterSize.csv")


def getMonitoringPurposes() -> List[DomeCode]:
    return _createCodesFromCSV("MonitoringPurposes.csv")


def getMonitoringProgrammes() -> List[DomeCode]:
    return _createCodesFromCSV("MonitoringProgrammes.csv")


def getLitterRefLists() -> List[DomeCode]:
    return _createCodesFromCSV("LitterRef.csv")


def _createCodesFromCSV(csvFileName) -> List[DomeCode]:
    """
    Reads a CSV file and returns a list of dome codes for each element.
    ASSUMES: First line is header
    ASSUMES: Of each other line: 2nd entry is the code, 3rd entry is the description
    :param csvFileName: filename relative to the domeCodeFolder
    :return: List of DomeCodes
    """
    with open(os.path.join(codeFolder, csvFileName)) as fp:
        csvReader = csv.reader(fp)
        codeList: List[DomeCode] = []
        for i, row in enumerate(csvReader):
            if i > 0:  # First line is header
                codeList.append(DomeCode(row[1], row[2]))
    return codeList
