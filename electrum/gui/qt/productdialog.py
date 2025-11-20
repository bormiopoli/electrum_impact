from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, QDoubleSpinBox,
    QPushButton, QHBoxLayout, QWidget, QMessageBox, QCompleter
)
from PyQt6.QtCore import Qt


class ProductDialog(QDialog):
    def __init__(self, countries, products, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Product Impact")
        self.countries = countries
        self.products = products
        self.rows = []  # store row widgets

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel("Add one or more product entries:"))

        # container for rows
        self.rows_container = QVBoxLayout()
        self.layout.addLayout(self.rows_container)

        # buttons
        add_button = QPushButton("Add Product")
        add_button.clicked.connect(self.add_row)
        self.layout.addWidget(add_button)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.on_accept)
        self.layout.addWidget(ok_button)

        # start with one row
        self.add_row()

    def add_row(self):
        """Add a new row with country, product, amount"""
        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)

        # Country combo with search
        country_combo = QComboBox()
        country_combo.addItems(self.countries)
        country_combo.setEditable(True)
        country_completer = QCompleter(self.countries, self)
        country_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        country_completer.setFilterMode(Qt.MatchFlag.MatchContains)
        country_combo.setCompleter(country_completer)

        # Product combo with search
        product_combo = QComboBox()
        product_combo.addItems(self.products)
        product_combo.setEditable(True)
        product_completer = QCompleter(self.products, self)
        product_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        product_completer.setFilterMode(Qt.MatchFlag.MatchContains)
        product_combo.setCompleter(product_completer)

        # Amount spin
        amount_spin = QDoubleSpinBox()
        amount_spin.setRange(0.0, 1.0)
        amount_spin.setSingleStep(0.01)

        row_layout.addWidget(QLabel("Country:"))
        row_layout.addWidget(country_combo)
        row_layout.addWidget(QLabel("Product:"))
        row_layout.addWidget(product_combo)
        row_layout.addWidget(QLabel("Amount:"))
        row_layout.addWidget(amount_spin)

        self.rows_container.addWidget(row_widget)
        self.rows.append((country_combo, product_combo, amount_spin))

    def on_accept(self):
        """Validate sum of amounts ≤ 1 before closing"""
        total = sum(spin.value() for _, _, spin in self.rows)
        if total > 1.0:
            QMessageBox.warning(self, "Invalid total",
                                f"Total amount {total:.2f} exceeds 1.0")
            return
        self.accept()

    def get_selection(self):
        """Return list of dicts for each row"""
        selections = []
        for country_combo, product_combo, amount_spin in self.rows:
            selections.append({
                "country": country_combo.currentText(),
                "product": product_combo.currentText(),
                "amount": amount_spin.value()
            })
        return selections
