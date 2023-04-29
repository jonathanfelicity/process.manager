import subprocess
from PyQt5.QtWidgets import ( 
    QWidget, 
    QTableWidget, 
    QTableWidgetItem, 
    QVBoxLayout, 
    QPushButton, 
    QHBoxLayout,
    QLabel
)
import psutil
from PyQt5.QtGui import QIcon

class TaskManager(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Process Manager')
        self.setWindowIcon(QIcon('icon.png'))

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(['PID', 'Name', 'Memory', 'CPU', 'Status'])

        self.refreshBtn = QPushButton('Refresh')
        self.refreshBtn.clicked.connect(self.populateTable)

        self.killBtn = QPushButton('Kill')
        self.killBtn.clicked.connect(self.killProcess)

        self.startBtn = QPushButton('Start')
        self.startBtn.clicked.connect(self.startProcess)

        hbox = QHBoxLayout()
        hbox.addWidget(self.refreshBtn)
        hbox.addWidget(self.killBtn)
        hbox.addWidget(self.startBtn)

        vbox = QVBoxLayout()
        vbox.addWidget(self.tableWidget)
        vbox.addLayout(hbox)


        self.setLayout(vbox)

        self.populateTable()

    def populateTable(self):
        self.tableWidget.setRowCount(0)

        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent', 'status']):
            try:
                name = proc.info['name']
                pid = proc.info['pid']
                mem = proc.info['memory_info'].rss / (1024 ** 2)
                cpu = proc.info['cpu_percent']
                status = proc.info['status']

                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)

                self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(str(pid)))
                self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(name))
                self.tableWidget.setItem(rowPosition, 2, QTableWidgetItem('{:.2f} MB'.format(mem)))
                self.tableWidget.setItem(rowPosition, 3, QTableWidgetItem('{:.2f} %'.format(cpu)))
                self.tableWidget.setItem(rowPosition, 4, QTableWidgetItem(status))

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def killProcess(self):
        rows = sorted(set(index.row() for index in self.tableWidget.selectedIndexes()))
        for row in rows:
            pid = self.tableWidget.item(row, 0).text()
            try:
                process = psutil.Process(int(pid))
                process.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        self.populateTable()

    def startProcess(self):
        filename, _ = filedialog.getOpenFileName(self, 'Open file', '.', 'Executable files (*.exe)')
        if filename:
            try:
                process = subprocess.Popen(filename)
            except OSError:
                pass

        self.populateTable()
