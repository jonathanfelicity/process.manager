import pytest
import psutil
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from main import TaskManager


@pytest.fixture
def app(qtbot):
    test_app = QApplication([])
    tm = TaskManager()
    qtbot.addWidget(tm)
    yield test_app
    test_app.quit()


def test_populateTable(app, qtbot):
    # populate the table
    qtbot.mouseClick(tm.refreshBtn, Qt.LeftButton)
    qtbot.waitUntil(lambda: tm.tableWidget.rowCount() > 0)

    # check that each row in the table corresponds to a valid process
    for row in range(tm.tableWidget.rowCount()):
        pid = int(tm.tableWidget.item(row, 0).text())
        try:
            proc = psutil.Process(pid)
            assert tm.tableWidget.item(row, 1).text() == proc.name()
            assert float(tm.tableWidget.item(row, 2).text().replace(' MB', '')) == proc.memory_info().rss / (1024 ** 2)
            assert float(tm.tableWidget.item(row, 3).text().replace(' %', '')) == proc.cpu_percent()
            assert tm.tableWidget.item(row, 4).text() == proc.status()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
