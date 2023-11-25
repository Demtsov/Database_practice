import sys
from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QCalendarWidget, QComboBox, QTableWidget, QTableWidgetItem
import sqlite3
class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Форма регистрации')
        self.label_username = QLabel('Имя:')
        self.entry_username = QLineEdit()
        self.label_surname = QLabel('Фамилия:')
        self.entry_surname = QLineEdit()
        self.label_password = QLabel('Пароль:')
        self.entry_password = QLineEdit()
        self.entry_password.setEchoMode(QLineEdit.Password)
        self.label_calendar =  QLabel('Дата рождения')
        self.entry_calendar = QCalendarWidget()
        self.label_combo = QLabel('Пол:')
        self.entry_combo = QComboBox()
        self.entry_combo.addItem("Мужской")
        self.entry_combo.addItem("Женский")
        self.register_button = QPushButton('Регистрация')
        self.register_button.clicked.connect(self.register)
        self.search_input = QLineEdit()
        self.search_button = QPushButton("Поиск")
        self.search_button.clicked.connect(self.search)
        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.delete)
        self.edit_button = QPushButton("Редактировать")
        self.edit_button.clicked.connect(self.edit)
        self.button = QPushButton("Вывести/Обновить таблицу", self)
        self.button.clicked.connect(self.show_data)
        self.table = QTableWidget()



        layout = QVBoxLayout()
        layout.addWidget(self.label_username)
        layout.addWidget(self.entry_username)
        layout.addWidget(self.label_surname)
        layout.addWidget(self.entry_surname)
        layout.addWidget(self.label_password)
        layout.addWidget(self.entry_password)
        layout.addWidget(self.label_calendar)
        layout.addWidget(self.entry_calendar)
        layout.addWidget(self.label_combo)
        layout.addWidget(self.entry_combo)
        layout.addWidget(self.register_button)
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.button)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def register(self):
        username = self.entry_username.text()
        surname = self.entry_surname.text()
        password = self.entry_password.text()
        calendar = self.entry_calendar.selectedDate().toString('yyyy-MM-dd')
        combobox = self.entry_combo.currentText()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("INSERT INTO users (username, surname, password, date, gender) VALUES (?, ?, ?, ?, ?)", (username, surname,password, calendar,combobox))
        connection.commit()
        connection.close()

        QMessageBox.information(self, 'Registration', 'Регистрация прошла успешно!')


    def show_data(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()

        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data[0]))

        for i in range(len(data)):
            for j in range(len(data[0])):
                item = QTableWidgetItem(str(data[i][j]))
                self.table.setItem(i, j, item)


        connection.close()

    def search(self):
        search= self.search_input.text()

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username LIKE ?", (f'%{search}%',))
        data = cursor.fetchall()

        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data[0]))

        for i in range(len(data)):
            for j in range(len(data[0])):
                item = QTableWidgetItem(str(data[i][j]))
                self.table.setItem(i, j, item)

    def delete(self):

        delete = self.search_input.text()
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM users WHERE username = ?", (delete,))
        conn.commit()

        QMessageBox.information(self, 'Registration', 'Удалено!')

    def edit(self):
        username = self.entry_username.text()
        surname = self.entry_surname.text()
        password = self.entry_password.text()
        calendar = self.entry_calendar.selectedDate().toString('yyyy-MM-dd')
        combobox = self.entry_combo.currentText()
        edit = self.search_input.text()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("UPDATE users SET username = ? , surname = ? , password = ? , date = ? , gender = ?   WHERE username = ?", (username, surname, password, calendar , combobox, edit))
        connection.commit()
        QMessageBox.information(self, 'Registration', 'Отредактировано!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RegistrationWindow()
    window.show()
    sys.exit(app.exec_())

