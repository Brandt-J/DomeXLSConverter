from typing import *
from dataimport import domeCodes as dc


def test_readLitterSource():
    ltrsrc: List[dc.DomeCode] = dc.getLitterSource()
    assert len(ltrsrc) == 16
    assert all([type(code) == dc.DomeCode for code in ltrsrc])
    for code in ltrsrc:
        assert type(code.code) == str
        assert type(code.descr) == str
        assert type(code.long_descr) == str
