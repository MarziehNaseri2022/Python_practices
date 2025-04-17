from PyQt5.QtWidgets import QMainWindow, QApplication, QTableView, QVBoxLayout, QWidget
from PyQt5.QtCore import QAbstractTableModel, Qt
from database.db_manager import session
from database.models import Contact
import sys
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QMessageBox
from uni.add_contact_dialog import AddContactDialog
from sqlalchemy.orm.exc import NoResultFound
from PyQt5.QtGui import QIcon
from database.models import Contact


# تعریف مدل جدول
class ContactTableModel(QAbstractTableModel):
    def __init__(self, contacts=None):
        super().__init__()
        self.contacts = contacts or []

    def rowCount(self, index):
        return len(self.contacts)

    def columnCount(self, index):
        return 3  # name, phone, email

    def data(self, index, role):
        if role == Qt.DisplayRole:
            contact = self.contacts[index.row()]
            column = index.column()
            if column == 0:
                return contact.name
            elif column == 1:
                return contact.phone
            elif column == 2:
                return contact.email

    def headerData(self, section, orientation, role):
        headers = ["Name", "Phone", "Email"]
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return headers[section]

# پنجره اصلی
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowTitle("Contact Book")
        self.setGeometry(100, 100, 600, 400)

        # خواندن اطلاعات از دیتابیس
        contacts = session.query(Contact).all()

        # ساخت جدول و مدل
        self.table = QTableView()
        self.model = ContactTableModel(contacts)
        self.table.setModel(self.model)

        # دکمه‌ها
        self.add_button = QPushButton("➕ Add")
        self.delete_button = QPushButton("🗑 Delete")
        self.edit_button = QPushButton("✏️ Edit")


     
        

        self.add_button.clicked.connect(self.add_contact)
        self.delete_button.clicked.connect(self.delete_contact)
        self.edit_button.clicked.connect(self.edit_contact)

        # لایه‌بندی دکمه‌ها
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        # لایه اصلی
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)



    def add_contact(self):
        dialog = AddContactDialog()
        if dialog.exec_():
            data = dialog.get_data()
            new_contact = Contact(name=data['name'], phone=data['phone'], email=data['email'])
            session.add(new_contact)
            session.commit()
            self.refresh_table()

    def delete_contact(self):
        selected = self.table.selectionModel().selectedRows()
        if selected:
            index = selected[0]
            contact = self.model.contacts[index.row()]
            session.delete(contact)
            session.commit()
            self.refresh_table()
        else:
            QMessageBox.warning(self, "No Selection", "Please select a contact to delete.")

    def edit_contact(self):
        selected = self.table.selectionModel().selectedRows()
        if selected:
            index = selected[0]
            contact = self.model.contacts[index.row()]

            dialog = AddContactDialog()
            dialog.name_input.setText(contact.name)
            dialog.phone_input.setText(contact.phone)
            dialog.email_input.setText(contact.email)

            if dialog.exec_():
                data = dialog.get_data()
                contact.name = data['name']
                contact.phone = data['phone']
                contact.email = data['email']
                session.commit()
                self.refresh_table()
        else:
            QMessageBox.warning(self, "No Selection", "Please select a contact to edit.")

    def refresh_table(self):
        self.model.contacts = session.query(Contact).all()
        self.model.layoutChanged.emit()

# فقط وقتی مستقیم اجرا بشه
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
