import sys
from PyQt6 import uic
from PyQt6.QtWidgets import *
from db_connect import db, cursor


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("phone.ui", self)

        # ปุ่ม
        self.btn_add.clicked.connect(self.add_data)
        self.btn_update.clicked.connect(self.update_data)
        self.btn_delete.clicked.connect(self.delete_data)
        self.btn_clear.clicked.connect(self.clear_data)
        self.btn_search.clicked.connect(self.search_data)

        # คลิก table
        self.tb_phone.cellClicked.connect(self.get_row)

        self.show_data()


    def show_data(self):

        self.tb_phone.setRowCount(0)

        cursor.execute(
            "SELECT id,brand,model,price,ram,storage FROM phone"
        )

        data = cursor.fetchall()

        for row_number, row_data in enumerate(data):

            self.tb_phone.insertRow(row_number)

            # คอลัมน์ #
            self.tb_phone.setItem(
                row_number,
                0,
                QTableWidgetItem(str(row_number + 1))
            )

            # ข้อมูลจริง
            self.tb_phone.setItem(row_number,1,QTableWidgetItem(str(row_data[1])))
            self.tb_phone.setItem(row_number,2,QTableWidgetItem(str(row_data[2])))
            self.tb_phone.setItem(row_number,3,QTableWidgetItem(str(row_data[3])))
            self.tb_phone.setItem(row_number,4,QTableWidgetItem(str(row_data[4])))
            self.tb_phone.setItem(row_number,5,QTableWidgetItem(str(row_data[5])))


    def add_data(self):

        brand = self.txt_brand.text()
        model = self.txt_model.text()
        price = self.txt_price.text()
        ram = self.txt_ram.text()
        storage = self.txt_storage.text()

        cursor.execute(
            "INSERT INTO phone (brand,model,price,ram,storage) VALUES (?,?,?,?,?)",
            (brand, model, price, ram, storage)
        )

        db.commit()

        self.show_data()
        self.clear_data()


    def update_data(self):

        row = self.tb_phone.currentRow()

        brand = self.txt_brand.text()
        model = self.txt_model.text()
        price = self.txt_price.text()
        ram = self.txt_ram.text()
        storage = self.txt_storage.text()

        id = self.get_id(row)

        cursor.execute(
            """UPDATE phone
               SET brand=?,model=?,price=?,ram=?,storage=?
               WHERE id=?""",
            (brand, model, price, ram, storage, id)
        )

        db.commit()
        self.show_data()


    def delete_data(self):

        row = self.tb_phone.currentRow()

        id = self.get_id(row)

        cursor.execute(
            "DELETE FROM phone WHERE id=?",
            (id,)
        )

        db.commit()
        self.show_data()


    def clear_data(self):

        self.txt_brand.clear()
        self.txt_model.clear()
        self.txt_price.clear()
        self.txt_ram.clear()
        self.txt_storage.clear()


    def search_data(self):

        keyword = self.txt_search.text()

        self.tb_phone.setRowCount(0)

        cursor.execute(
            """SELECT id,brand,model,price,ram,storage 
               FROM phone
               WHERE brand LIKE ? OR model LIKE ?""",
            ('%' + keyword + '%', '%' + keyword + '%')
        )

        data = cursor.fetchall()

        for row_number, row_data in enumerate(data):

            self.tb_phone.insertRow(row_number)

            self.tb_phone.setItem(
                row_number,
                0,
                QTableWidgetItem(str(row_number + 1))
            )

            self.tb_phone.setItem(row_number,1,QTableWidgetItem(str(row_data[1])))
            self.tb_phone.setItem(row_number,2,QTableWidgetItem(str(row_data[2])))
            self.tb_phone.setItem(row_number,3,QTableWidgetItem(str(row_data[3])))
            self.tb_phone.setItem(row_number,4,QTableWidgetItem(str(row_data[4])))
            self.tb_phone.setItem(row_number,5,QTableWidgetItem(str(row_data[5])))


    def get_row(self, row, column):

        self.txt_brand.setText(self.tb_phone.item(row,1).text())
        self.txt_model.setText(self.tb_phone.item(row,2).text())
        self.txt_price.setText(self.tb_phone.item(row,3).text())
        self.txt_ram.setText(self.tb_phone.item(row,4).text())
        self.txt_storage.setText(self.tb_phone.item(row,5).text())


    def get_id(self, row):

        cursor.execute("SELECT id FROM phone LIMIT 1 OFFSET ?", (row,))
        data = cursor.fetchone()

        return data[0]


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())