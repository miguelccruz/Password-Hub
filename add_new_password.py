import sys
from openpyxl import Workbook
import openpyxl
from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QMessageBox,
    QHBoxLayout,
    QStyle
    )
from PyQt6.QtGui import QIcon

class FormWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Password Hub: Add New Account')
        self.setWindowIcon(QIcon('cat.ico'))
        self.setGeometry(760, 440, 500, 300)

        form_layout = QFormLayout()
        self.setLayout(form_layout)
    
        # ComboBox
        self.create_dropdown()
        self.account_name = QLineEdit(self)
        self.email_user = QLineEdit(self)
        self.password = QLineEdit(self, echoMode=QLineEdit.EchoMode.Password)
        self.note = QLineEdit(self)

        self.show_password_icon = QPushButton(self)
        pixmapi = QStyle.StandardPixmap.SP_VistaShield
        icon = self.style().standardIcon(pixmapi)
        self.show_password_icon.setIcon(QIcon(icon))
        self.show_password_icon.setCheckable(True)
        self.show_password_icon.clicked.connect(self.toggle_password_visibility)

        submit_button = QPushButton('Submit')
        submit_button.clicked.connect(self.create_new_row)

        form_layout.addRow('Category:', self.dropdown_menu)
        form_layout.addRow('Account Name:', self.account_name)
        form_layout.addRow('Email/Username:', self.email_user)

        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password)
        password_layout.addWidget(self.show_password_icon)
        form_layout.addRow('Password:', password_layout)

        form_layout.addRow('Note:', self.note)
        form_layout.addRow(submit_button)

    def create_new_row(self):
        data = [
            self.dropdown_menu.currentText(), 
            self.account_name.text(), 
            self.email_user.text(), 
            self.password.text(),
            self.note.text()
        ]

        txt_file_path = 'accounts_data/account_names.txt'
        file_path = 'accounts_data/accounts_data.xlsx'
        wb = openpyxl.load_workbook(file_path)
        ws1 = wb.active

        # data_validation flag
        found_clone = False

        # checks if account name already exists in database
        for row in ws1.iter_rows(min_col=2, max_col=2, min_row=2):
            for cell in row:
                if self.account_name.text() == str(cell.value).lower():
                    QMessageBox.critical(
                        self,
                        'Error',
                        'Account Name already exists in database'
                    )
                    found_clone = True
                    break
            if found_clone:
                break
                    
        if not found_clone:
            ws1.append(data)
            wb.save(filename=file_path)
            print("saved to xlsx file")
            self.close()

            # write in txt file for autocomplete
            with open(txt_file_path, 'a') as file:
                file.write(self.account_name.text() + '\n')

    def toggle_password_visibility(self, checked):
        if checked:
            self.password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password.setEchoMode(QLineEdit.EchoMode.Password)
        




        

    def create_dropdown(self):

        self.dropdown_menu = QComboBox(self)
        self.dropdown_menu.addItems([
            'Bank',
            'Browser',
            'E-mail',
            'Game',
            'Home',
            'Jobs',
            'Others',
            'School',
            'Social Media',
            'York'
        ])