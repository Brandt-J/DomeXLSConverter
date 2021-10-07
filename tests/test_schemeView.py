from typing import *
from PyQt6 import QtGui, QtCore

from gui.schemeView import SchemeView

if TYPE_CHECKING:
    from gui.schemeView import TableGUIElement


def test_scheme_view_andMouseevents(qtbot, tmpdir):
    view: SchemeView = SchemeView()
    qtbot.addWidget(view)
    assert len(view._tableCollection.getTableItems()) > 0
    assert len(view._guiElements) == len(view._tableCollection.getTableItems())

    lastTableElement: TableGUIElement = view._guiElements[-1]
    assert not lastTableElement.isUnderMouse()
    centerPos: QtCore.QPoint = QtCore.QPoint(lastTableElement.pos().x() + lastTableElement.size.width() / 2,
                                             lastTableElement.pos().y() + lastTableElement.size.height() / 2)
    qtbot.mouseMove(view, centerPos, delay=50)
    assert lastTableElement.isUnderMouse()
