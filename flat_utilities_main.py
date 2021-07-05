from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem as twi
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QFont
from flat_utilities_design import Ui_MainWindow
import sqlite3
from sqlite3 import Error
from datetime import datetime
import sys
 
def connect_to_db(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Error as e:
        print(f"The error '{e}' occurred")
        sys.exit(1)
    return connection
connection = connect_to_db('/Users/username/flat_utilities.db')

def select_request(connection, request):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(request)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
        sys.exit(1)

def change_request(connection, request):
    cursor = connection.cursor()
    try:
        cursor.execute(request)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")
        sys.exit(1)

select_tar = """SELECT cold_wat, hot_wat, drin_wat, t1, t2, t3,
wi_fi FROM tariffs WHERE date = (SELECT MAX(date) FROM tariffs);"""
last_tar = [str(y) for x in select_request(connection, select_tar) for y in x]

select_counters = """SELECT cold_wat, hot_wat, t1, t2, t3
FROM counters WHERE date = (SELECT MAX(date) FROM counters);"""
last_counter = [str(y) for x in select_request(connection, select_counters) for y in x]

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.t_cold_wat.setText(last_tar[0])
        self.ui.t_hot_wat.setText(last_tar[1])
        self.ui.t_drin_wat.setText(last_tar[2])
        self.ui.t_t1.setText(last_tar[3])
        self.ui.t_t2.setText(last_tar[4])
        self.ui.t_t3.setText(last_tar[5])
        self.ui.t_wifi.setText(last_tar[6])
        self.ui.s_cold_wat.setText(last_counter[0])
        self.ui.s_hot_wat.setText(last_counter[1])
        self.ui.s_t1.setText(last_counter[2])
        self.ui.s_t2.setText(last_counter[3])
        self.ui.s_t3.setText(last_counter[4])
        self.ui.table.setHorizontalHeaderLabels(['Service', 'Price'])
        self.ui.save_button.setEnabled(False)
        self.ui.calc_button.clicked.connect(self.Calculate)
        self.ui.reset_button.clicked.connect(self.Reset)
        self.ui.save_button.clicked.connect(self.Save)

    def Calculate(self):
        try:
            t_cold_wat = float(self.ui.t_cold_wat.text())
            s_cold_wat = float(self.ui.s_cold_wat.text())
            n_cold_wat = float(self.ui.n_cold_wat.text())
            cold_wat = (n_cold_wat-s_cold_wat)*t_cold_wat
            self.ui.table.setItem(0, 0, twi('Cold water'))
            self.ui.table.setItem(0, 1, twi(str(cold_wat)))
        
            t_hot_wat = float(self.ui.t_hot_wat.text())
            s_hot_wat = float(self.ui.s_hot_wat.text())
            n_hot_wat = float(self.ui.n_hot_wat.text())
            hot_wat = (n_hot_wat-s_hot_wat)*t_hot_wat
            self.ui.table.setItem(1, 0, twi('Hot water'))
            self.ui.table.setItem(1, 1, twi(str(hot_wat)))
        
            t_drin_wat = float(self.ui.t_drin_wat.text())
            drin_wat = t_drin_wat*((n_cold_wat-s_cold_wat)+(n_hot_wat-s_hot_wat))
            self.ui.table.setItem(2, 0, twi('Drinage water'))
            self.ui.table.setItem(2, 1, twi(str(drin_wat)))
        
            t_t1 = float(self.ui.t_t1.text())
            s_t1 = float(self.ui.s_t1.text())
            n_t1 = float(self.ui.n_t1.text())
            t1 = (n_t1-s_t1)*t_t1
            self.ui.table.setItem(3, 0, twi('T1'))
            self.ui.table.setItem(3, 1, twi(str(t1)))
        
            t_t2 = float(self.ui.t_t2.text())
            s_t2 = float(self.ui.s_t2.text())
            n_t2 = float(self.ui.n_t2.text())
            t2 = (n_t2-s_t2)*t_t2
            self.ui.table.setItem(4, 0, twi('T2'))
            self.ui.table.setItem(4, 1, twi(str(t2)))
        
            t_t3 = float(self.ui.t_t3.text())
            s_t3 = float(self.ui.s_t3.text())
            n_t3 = float(self.ui.n_t3.text())
            t3 = (n_t3-s_t3)*t_t3
            self.ui.table.setItem(5, 0, twi('T3'))
            self.ui.table.setItem(5, 1, twi(str(t3)))

            wi_fi = float(self.ui.t_wifi.text())
            self.ui.table.setItem(6, 0, twi('Wi-fi'))
            self.ui.table.setItem(6, 1, twi(str(wi_fi)))
        
            total = cold_wat+hot_wat+drin_wat+t1+t2+t3+wi_fi
            self.ui.table.setItem(7, 0, twi('Total'))
            self.ui.table.setItem(7, 1, twi(str(total)))
            bold_font = QFont()
            bold_font.setBold(True)
            self.ui.table.item(7, 0).setFont(bold_font)
            self.ui.table.item(7, 1).setFont(bold_font)
            self.ui.save_button.setEnabled(True)
        except ValueError:
            QMessageBox.critical(self,
                                 "Error", "Arguments must be digits",
                                 QMessageBox.Ok)
            sys.exit(1)

    def Reset(self):
        self.ui.t_cold_wat.clear()
        self.ui.t_hot_wat.clear()
        self.ui.t_drin_wat.clear()
        self.ui.t_t1.clear()
        self.ui.t_t2.clear()
        self.ui.t_t3.clear()
        self.ui.t_wifi.clear()
        self.ui.s_cold_wat.clear()
        self.ui.s_hot_wat.clear()
        self.ui.s_t1.clear()
        self.ui.s_t2.clear()
        self.ui.s_t3.clear()
        self.ui.n_cold_wat.clear()
        self.ui.n_hot_wat.clear()
        self.ui.n_t1.clear()
        self.ui.n_t2.clear()
        self.ui.n_t3.clear()
        self.ui.table.clear()
        self.ui.save_button.setEnabled(False)

    def Save(self):
        current_date = datetime.now().date()
        tariffs = (float(self.ui.t_cold_wat.text()), float(self.ui.t_hot_wat.text()),
                   float(self.ui.t_drin_wat.text()), float(self.ui.t_t1.text()),
                   float(self.ui.t_t2.text()), float(self.ui.t_t3.text()),
                   float(self.ui.t_wifi.text()), str(current_date))
        insert_tar = """
INSERT INTO tariffs (cold_wat, hot_wat, drin_wat, t1, t2, t3, wi_fi, date)
VALUES"""
        send_tar = insert_tar + str(tariffs) + ';'
        change_request(connection, send_tar)

        counters = (float(self.ui.n_cold_wat.text()), float(self.ui.n_hot_wat.text()),
                    float(self.ui.n_t1.text()), float(self.ui.n_t2.text()),
                    float(self.ui.n_t3.text()), str(current_date))
        insert_counters = """
INSERT INTO counters (cold_wat, hot_wat, t1, t2, t3, date)
VALUES"""
        send_counters = insert_counters + str(counters) + ';'
        change_request(connection, send_counters)

        receipt_l = [float(self.ui.table.item(i, 1).text()) for i in range(8)]
        receipt_l.append(str(current_date))
        receipt_t = tuple(receipt_l)
        insert_receipt = """
INSERT INTO receipt (cold_wat, hot_wat, drin_wat, t1, t2, t3, wi_fi, total, date)
VALUES"""
        send_receipt = insert_receipt + str(receipt_t) + ';'
        change_request(connection, send_receipt)

        QMessageBox.information(self, "Ready", "Data has been saved",
                                     QMessageBox.Ok)
        self.ui.save_button.setEnabled(False)
    
app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())
