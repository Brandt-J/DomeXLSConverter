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


from gui.pages.page_3_time import TimePage
from tables.table_3_time import TimeTable
from dataimport.domeCodes import DomeCode


def test_is_complete(qtbot, tmpdir):
    table: TimeTable = TimeTable()
    timePage: TimePage = TimePage(table)
    qtbot.addWidget(timePage)
    timePage.show()
    qtbot.waitForWindowShown(timePage)
    assert timePage.isComplete()

    def test_checkBox_taleElement(checkbox, tableElement):
        checkbox.toggle()
        assert type(tableElement.content) == DomeCode
        assert tableElement.content.code == "1234"  # 12:34 is the default time. Adjust here if it was changed in the page script file.
        assert timePage.isComplete()
        checkbox.toggle()
        assert tableElement.content is None
        assert timePage.isComplete()

    test_checkBox_taleElement(timePage._checkSamplingTime, table._stime)
    test_checkBox_taleElement(timePage._checkActualTime, table._atime)
    test_checkBox_taleElement(timePage._checkEndTime, table._etime)
