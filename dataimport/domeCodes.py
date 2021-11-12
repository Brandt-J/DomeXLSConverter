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
    long_descr: str  # Long Description


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
                codeList.append(DomeCode(row[1], row[2], "No further infos available"))
    return codeList
