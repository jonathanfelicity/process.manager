import sys
from main import TaskManager
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TaskManager()
    ex.show()
    sys.exit(app.exec_())
