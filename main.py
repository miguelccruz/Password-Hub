import sys
import os
from search_results import ResultsWindow
from pathlib import Path
from add_new_password import FormWindow
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
    QCompleter,
    QLabel,
    )
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Password Hub')
        self.setWindowIcon(QIcon('cat.ico'))
        self.setGeometry(760, 440, 500, 150)

        accounts_list = self.read_account_names('accounts_data/account_names.txt')

        completer = QCompleter()
        model = QStandardItemModel()
        for account in accounts_list:
            item = QStandardItem(account)
            model.appendRow(item)
        completer.setModel(model)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        # title
        self.heading = QLabel('Password Hub', alignment=Qt.AlignmentFlag.AlignHCenter)
        self.heading.setObjectName('heading')

        # subheading
        self.subheading = QLabel('Search for an account name or add an account', alignment=Qt.AlignmentFlag.AlignHCenter)
        self.subheading.setObjectName('subheading')

        # search line entry
        self.search_entry = QLineEdit(self, placeholderText='Enter type of account...', clearButtonEnabled=True)
        self.search_entry.returnPressed.connect(self.search_button_clicked)
        self.search_entry.setCompleter(completer)

        #search button
        search_button = QPushButton('Search')
        search_button.clicked.connect(self.search_button_clicked)

        # add password button
        addpass_button = QPushButton('Add Account')
        addpass_button.clicked.connect(self.addpass_button_clicked)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        main_layout.addWidget(self.heading)
        main_layout.addWidget(self.subheading)
        main_layout.addWidget(self.search_entry)
        main_layout.addWidget(search_button)
        main_layout.addWidget(addpass_button)
        
        self.show()

    def search_button_clicked(self):
        search_text = self.search_entry.text()
        self.results_window = ResultsWindow(search_text=search_text)
        self.results_window.show()

    def addpass_button_clicked(self):
        self.new_account_window = FormWindow()
        self.new_account_window.show()

    def read_account_names(self, file_path):
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write("")
        try: 
            with open(file_path, 'r') as file:
                accounts = [line.strip() for line in file.readlines()]
            return accounts
        except FileNotFoundError:
            print('file not found')
            return []



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(Path('style/style.qss').read_text())
    window = MainWindow()

    sys.exit(app.exec())