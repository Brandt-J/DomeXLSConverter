from tableItems import *
from dataimport.domeCodes import DomeCode


def test_idTable():
    table: IdentificationTable = IdentificationTable()
    assert not table.correctlySet()

    table.setReportingLab(DomeCode("RLABO", "Laboratory Code", "None"))
    assert not table.correctlySet()
