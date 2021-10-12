from typing import *

from tableItems import TableItem


def test_correctly_set():
    correctDict: dict = {"attr1": "something",
                         "attr2": 2,
                         "attr3": True}
    incorrectDict: dict = {"attr1": "something",
                           "attr2": None,
                           "attr3": True}

    tableItem: TableItem = TableItem("test")
    assert not tableItem.correctlySet()

    tableItem._fields = correctDict
    assert tableItem.correctlySet()

    tableItem._fields = incorrectDict
    assert not tableItem.correctlySet()