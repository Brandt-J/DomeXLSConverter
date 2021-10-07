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


def test_initialize_fields():
    tableItem: TableItem = TableItem("test")
    fieldNames1: List[str] = ["field1", "field2", "field3"]
    tableItem.initializeFields(fieldNames1)
    assert list(tableItem._fields.keys()) == fieldNames1
    for name in fieldNames1:
        assert tableItem._fields[name] is None
    assert not tableItem.correctlySet()

    fieldNames2: List[str] = ["newField1", "newField2", "newField3"]
    tableItem.initializeFields(fieldNames2)
    assert list(tableItem._fields.keys()) == fieldNames2
    for name in fieldNames2:
        assert tableItem._fields[name] is None
    assert not tableItem.correctlySet()