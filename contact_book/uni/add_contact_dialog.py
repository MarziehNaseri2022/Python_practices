from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton

class AddContactDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Contact")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.name_input)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def get_data(self):
        return {
            "name": self.name_input.text(),
            "phone": self.phone_input.text(),
            "email": self.email_input.text()
        }
