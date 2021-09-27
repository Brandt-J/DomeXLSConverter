from gui.schemeView import SchemeView


def test_scheme_view(qtbot, tmpdir):
    view: SchemeView = SchemeView()
    qtbot.addWidget(view)
    assert True
