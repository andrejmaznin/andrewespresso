import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget, QMessageBox
from PyQt5 import uic
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.show()
        uic.loadUi('main.ui', self)
        self.btn_update.clicked.connect(self.update)

    def update(self):
        self.tableWidget.setRowCount(0)
        found = cur.execute(f"""SELECT * FROM coffee""").fetchall()
        if found != []:
            self.tableWidget.setRowCount(len(found))
            self.tableWidget.setColumnCount(len(found[0]))
            for i in range(len(found)):
                self.tableWidget.setItem(i, 0, QTableWidgetItem(str(found[i][0])))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(found[i][1]))
                self.tableWidget.setItem(i, 2, QTableWidgetItem(found[i][4]))
                self.tableWidget.setItem(i, 3, QTableWidgetItem(str(found[i][3])))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    con = sqlite3.connect("coffee.sqlite")
    cur = con.cursor()
    sys.exit(app.exec())
