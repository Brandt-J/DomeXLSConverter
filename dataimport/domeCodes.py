import pandas as pd
from typing import *
from dataclasses import dataclass
import numpy as np
import os

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
