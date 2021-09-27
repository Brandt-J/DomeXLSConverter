from tableItems import TableItem


def test_correctly_set():
    correctDict: dict = {"attr1": "something",
                         "attr2": 2,
                         "attr3": True}
    incorrectDict: dict = {"attr1": "something",
                           "attr2": None,
                           "attr3": True}

    correctTableItem = TableItem("test", correctDict)
    incorrectTableItem = TableItem("test", incorrectDict)
    assert correctTableItem.correctlySet()
    assert not incorrectTableItem.correctlySet()
