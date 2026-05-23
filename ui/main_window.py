from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QComboBox,
    QMessageBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QTableWidget,       
    QTableWidgetItem
)

from backend.credential_service import (
    save_credential,
    get_all_websites,
    get_credential_by_website,
    delete_credential,
    update_credential
)
from PyQt6.QtGui import QGuiApplication



class AddCredentialDialog(QDialog):
    from PyQt6.QtWidgets import QTableWidget
    from PyQt6.QtWidgets import QTableWidgetItem
    def __init__(
        self,
        website="",
        username="",
        password="",
        metadata=None
    ):
        super().__init__()

        self.setWindowTitle("Add New Credential")
        self.setGeometry(300, 300, 550, 400)

        # Inputs
        self.website_input = QLineEdit()
        self.website_input.setText(website)
        self.website_input.setPlaceholderText(
            "Enter website or portal"
        )

        self.username_input = QLineEdit()
        self.username_input.setText(username)
        self.username_input.setPlaceholderText(
            "Enter username"
        )

        self.password_input = QLineEdit()
        self.password_input.setText(password)
        self.password_input.setPlaceholderText(
            "Enter password"
        )

        self.metadata_table = QTableWidget()

        self.metadata_table.setColumnCount(2)

        self.metadata_table.setHorizontalHeaderLabels([
            "Key",
            "Value"
        ])

        self.metadata_table.setRowCount(0)
        # Populate metadata if editing
        if metadata:
            for key, value in metadata.items():
                row = self.metadata_table.rowCount()

                self.metadata_table.insertRow(row)

                self.metadata_table.setItem(
                    row,
                    0,
                    QTableWidgetItem(str(key))
                )

                self.metadata_table.setItem(
                    row,
                    1,
                    QTableWidgetItem(str(value))
                )

        # Empty row for new credential
        else:
            self.add_metadata_row()

        
        #self.add_metadata_row()
        

        self.password_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        # Buttons
        self.save_button = QPushButton("Save")
        self.reset_button = QPushButton("Reset")
        self.show_password_button = QPushButton("Show Password")
        self.add_metadata_button = QPushButton("Add Metadata")
        self.remove_metadata_button = QPushButton("Remove Metadata")

        # Layout
        form_layout = QFormLayout()

        form_layout.addRow(
            "Website",
            self.website_input
        )

        form_layout.addRow(
            "Username",
            self.username_input
        )

        form_layout.addRow(
            "Password",
            self.password_input
        )

        form_layout.addRow(
            "Metadata",
            self.metadata_table
        )

        button_layout = QHBoxLayout()

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.show_password_button)
        button_layout.addWidget(self.add_metadata_button)
        button_layout.addWidget(self.remove_metadata_button)

        main_layout = QVBoxLayout()

        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Button actions
        self.reset_button.clicked.connect(
            self.reset_fields
        )

        self.save_button.clicked.connect(
            self.accept
        )

        self.add_metadata_button.clicked.connect(
            self.add_metadata_row
        )
        
        self.remove_metadata_button.clicked.connect(
            self.remove_metadata_row
        )

        self.show_password_button.clicked.connect(
            self.toggle_password
        )


    def add_metadata_row(self):
        row = self.metadata_table.rowCount()

        self.metadata_table.insertRow(row)

        self.metadata_table.setItem(
            row,
            0,
            QTableWidgetItem("")
        )

        self.metadata_table.setItem(
            row,
            1,
            QTableWidgetItem("")
        )

    def remove_metadata_row(self):
        current_row = (
            self.metadata_table.currentRow()
        )

        if current_row >= 0:
            self.metadata_table.removeRow(
                current_row
            )


    def get_metadata(self):
        metadata = {}

        rows = self.metadata_table.rowCount()

        for row in range(rows):
            key_item = self.metadata_table.item(row, 0)
            value_item = self.metadata_table.item(row, 1)

            if key_item and value_item:
                key = key_item.text().strip()
                value = value_item.text().strip()

                if key:
                    metadata[key] = value

        return metadata

    def reset_fields(self):
        self.website_input.clear()
        self.username_input.clear()
        self.password_input.clear()

    def toggle_password(self):
        if (
            self.password_input.echoMode()
            == QLineEdit.EchoMode.Password
        ):
            self.password_input.setEchoMode(
                QLineEdit.EchoMode.Normal
            )

            self.show_password_button.setText(
                "Hide Password"
            )

        else:
            self.password_input.setEchoMode(
                QLineEdit.EchoMode.Password
            )

            self.show_password_button.setText(
                "Show Password"
            )


class MainWindow(QWidget):

    def copy_username(self):
        username = self.username_input.text()

        if username:
            clipboard = QGuiApplication.clipboard()

            clipboard.setText(username)

            QMessageBox.information(
                self,
                "Copied",
                "Username copied to clipboard"
            )
    
    def copy_password(self):
        password = self.password_input.text()

        if password:
            clipboard = QGuiApplication.clipboard()

            clipboard.setText(password)

            QMessageBox.information(
                self,
                "Copied",
                "Password copied to clipboard"
            )

    def edit_selected_credential(self):
        selected_website = (
            self.website_dropdown.currentText()
        )

        if (
            not selected_website
            or selected_website ==
            "-- Select Website --"
        ):
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a website"
            )
            return

        credential = get_credential_by_website(
            selected_website
        )

        if not credential:
            QMessageBox.warning(
                self,
                "Not Found",
                "Credential not found"
            )
            return

        username, password, metadata = credential

        dialog = AddCredentialDialog(
            selected_website,
            username,
            password,
            metadata
        )


        if dialog.exec():
            new_website = (
                dialog.website_input.text().strip()
            )

            new_username = (
                dialog.username_input.text().strip()
            )

            new_password = (
                dialog.password_input.text().strip()
            )

            new_metadata = dialog.get_metadata()

            if (
                not new_website
                or not new_username
                or not new_password
            ):
                QMessageBox.warning(
                    self,
                    "Missing Data",
                    "All fields are required"
                )
                return

            try:
                update_credential(
                    selected_website,
                    new_website,
                    new_username,
                    new_password,
                    new_metadata
                )

                QMessageBox.information(
                    self,
                    "Updated",
                    f"Credentials updated for {new_website}"
                )

                # Reload dropdown
                self.load_websites()

                # Re-select updated website
                self.website_dropdown.setCurrentText(
                    new_website
                )

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    str(e)
                )



    def delete_selected_credential(self):
        website = self.website_dropdown.currentText()

        if (
            not website
            or website == "-- Select Website --"
        ):
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a website"
            )
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Delete credentials for {website}?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                delete_credential(website)

                QMessageBox.information(
                    self,
                    "Deleted",
                    f"Credentials deleted for {website}"
                )

                # Reload dropdown
                self.load_websites()

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    str(e)
                )

    def load_websites(self):
        self.website_dropdown.clear()

        # Empty default item
        self.website_dropdown.addItem(
        "-- Select Website --"
        )

        websites = get_all_websites()

        self.website_dropdown.addItems(websites)

        # No data visible at launch
        self.username_input.clear()
        self.password_input.clear()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Credential Manager")
        self.setGeometry(200, 200, 900, 700)

        # Temporary credential storage
        self.credentials = {}

        # Dropdown
        self.website_dropdown = QComboBox()

        # Username field
        self.username_input = QLineEdit()
        self.username_input.setReadOnly(True)

        # Password field
        self.password_input = QLineEdit()
        self.password_input.setReadOnly(True)

        self.metadata_table = QTableWidget()

        self.metadata_table.setColumnCount(2)

        self.metadata_table.setHorizontalHeaderLabels([
            "Metadata Key",
            "Metadata Value"
        ])

        self.password_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        # Buttons
        self.show_button = QPushButton(
            "Show Password"
        )

        self.copy_username_button = QPushButton(
            "Copy Username"
        )

        self.copy_password_button = QPushButton(
            "Copy Password"
        )

        self.delete_button = QPushButton(
            "Delete Credential"
        )

        self.edit_button = QPushButton(
            "Edit Credential"
        )

        self.add_website_button = QPushButton(
            "Add Website / Portal"
        )

        # Actions
        self.show_button.clicked.connect(
            self.toggle_password
        )

        self.copy_username_button.clicked.connect(
            self.copy_username
        )

        self.copy_password_button.clicked.connect(
            self.copy_password
        )

        self.delete_button.clicked.connect(
            self.delete_selected_credential
        )

        self.edit_button.clicked.connect(
            self.edit_selected_credential
        )

        self.add_website_button.clicked.connect(
            self.open_add_dialog
        )

        self.website_dropdown.currentTextChanged.connect(
            self.load_credentials
        )

        # Layout
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Select Website"))
        layout.addWidget(self.website_dropdown)

        layout.addWidget(self.add_website_button)

        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.username_input)

        layout.addWidget(self.copy_username_button)

        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.copy_password_button)

        layout.addWidget(QLabel("Metadata"))
        layout.addWidget(self.metadata_table)


        layout.addWidget(self.show_button)

        layout.addWidget(self.delete_button)

        layout.addWidget(self.edit_button)

        self.setLayout(layout)
        self.load_websites()

    def open_add_dialog(self):
        dialog = AddCredentialDialog()

        if dialog.exec():
            website = dialog.website_input.text().strip()
            username = dialog.username_input.text().strip()
            password = dialog.password_input.text().strip()
            metadata = dialog.get_metadata()

            # Validation
            if not website or not username or not password:
                QMessageBox.warning(
                    self,
                    "Missing Data",
                    "All fields are required"
                )
                return

            try:
                # Save to database
                save_credential(
                    website,
                    username,
                    password,
                    metadata
                )


                # Add to dropdown
                self.load_websites()

                # Auto select saved item
                self.website_dropdown.setCurrentText(
                    website
                )

                QMessageBox.information(
                    self,
                    "Saved",
                    f"Credentials saved for {website}"
                )

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    str(e)
                )


    def load_credentials(self):
        website = self.website_dropdown.currentText()

        if (
            not website
            or website == "-- Select Website --"
        ):
            self.username_input.clear()
            self.password_input.clear()
            self.metadata_table.setRowCount(0)
            return

        credential = get_credential_by_website(website)

        if credential:
            username, password, metadata = credential

            self.username_input.setText(username)
            self.password_input.setText(password)
            # Populate metadata table
            self.metadata_table.setRowCount(0)

            for key, value in metadata.items():
                row = self.metadata_table.rowCount()

                self.metadata_table.insertRow(row)

                self.metadata_table.setItem(
                    row,
                    0,
                    QTableWidgetItem(key)
                )

                self.metadata_table.setItem(
                    row,
                    1,
                    QTableWidgetItem(value)
                )

        else:
            self.username_input.clear()
            self.password_input.clear()
            self.metadata_table.setRowCount(0)


    def toggle_password(self):
        if (
            self.password_input.echoMode()
            == QLineEdit.EchoMode.Password
        ):
            self.password_input.setEchoMode(
                QLineEdit.EchoMode.Normal
            )

            self.show_button.setText(
                "Hide Password"
            )

        else:
            self.password_input.setEchoMode(
                QLineEdit.EchoMode.Password
            )

            self.show_button.setText(
                "Show Password"
            )