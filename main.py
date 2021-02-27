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


class Form(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.btn_update.clicked.connect(self.update)
        self.btn_cancel.clicked.connect(self.cancel)

    def add_bd(self):
        for i in range(7):
            eval(f"self.lineEdit_{i + 1}.setText('')")
        ex.hide()
        self.show()

    def update(self):
        self.con = sqlite3.connect("coffee.sqlite")
        cur = self.con.cursor()
        n = []
        for i in range(7):
            n.append(eval(f"self.lineEdit_{i + 1}.text()"))
        if n[3] == 'в зернах':
            n[3] = '1'
        elif n[3] == 'молотый':
            n[3] = '2'
        else:
            print("Вы ввели неверные значения!")
            self.cancel()
            return
        m = cur.execute('SELECT id FROM tastes WHERE taste = ?', (n[4],)).fetchone()
        if m:
            n[4] = str(m[0])
        else:
            cur.execute(f"INSERT INTO tastes(taste) VALUES ('{n[4]}')")
            n[4] = str(cur.execute('SELECT id FROM tastes WHERE taste = ?', (n[4],)).fetchone()[0])

        n[1] = '"' + n[1] + '"'
        m = cur.execute('SELECT id FROM coffee').fetchall()
        if len(m) < 0 and n[0] == '':
            n[0] = '1'
        elif n[0] == '':
            n[0] = str(m[-1][0] + 1)
        elif n[0] in [str(el[0]) for el in m]:
            print('Кофе с таким ID уже существует ')
            return
        if not n[2].isdigit() or not n[-1].isdigit() or not n[-2].isdigit():
            print("Вы ввели неверные значения")
            return
        cur.execute(f"INSERT INTO coffee VALUES({', '.join(n)})")
        self.con.commit()
        self.con.close()
        self.hide()
        ex.table_update()
        ex.show()

    def cancel(self):
        self.hide()
        ex.show()

    def change_bd(self):
        self.con = sqlite3.connect("coffee.sqlite")
        ex.hide()
        self.show()
        if len(ex.tableWidget.selectedItems()) > 0:
            row = list(set([i.row() for i in ex.tableWidget.selectedItems()]))[0]
            for i in range(7):
                eval(f"self.lineEdit_{i + 1}.setText(ex.tableWidget.item(row, i).text())")
            cur = self.con.cursor()
            cur.execute("DELETE FROM coffee WHERE id = ?", (ex.tableWidget.item(row, 0).text(),))
            self.con.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    con = sqlite3.connect("coffee.sqlite")
    cur = con.cursor()
    sys.exit(app.exec())
